#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GA‑XGBoost 기반 고객 이탈(Churn) 예측 + SHAP 해석 단일 스크립트 (DB 버전)
-----------------------------------------------------------------
- PostgreSQL DB에서 데이터를 읽어와서 학습
- 데이터 전처리(수치/범주), 불균형 대응(scale_pos_weight), 교차검증 기반 GA 튜닝
- 최적 모델 학습, 다양한 지표(F1, PR‑AUC, ROC‑AUC, Brier, Precision@k, Recall@k)
- PR/ROC 곡선, 혼동행렬, FI/SHAP 리포트(가능 시) 저장
- Markdown 리포트 자동 생성
- 학습 결과를 DB에 저장

사용법 예시:
$ python churn_ga_xgb_db.py --table ml_training_data --target EverDelinquent \
  --id_col index --date_col Parsed_FirstPaymentDate --test_size 0.2 \
  --kfold 5 --generations 20 --population 36 --precision_k 0.1 \
  --outdir outputs
"""

import argparse
import json
import os
import warnings
from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (average_precision_score, brier_score_loss,
                             classification_report, confusion_matrix,
                             precision_recall_curve, precision_score,
                             recall_score, roc_auc_score, roc_curve)
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from xgboost import XGBClassifier

try:
    import shap  # type: ignore
    _HAS_SHAP = True
except Exception:
    _HAS_SHAP = False
    warnings.warn("shap이 설치되지 않아 SHAP 리포트를 건너뜁니다. 'pip install shap' 후 사용하세요.")

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# 데이터베이스 연결 설정
DB_CONFIG = {
    'host': 'postgres',  # Docker 네트워크 내에서의 서비스명
    'port': 5432,
    'database': 'retention_db',
    'user': 'retention_user',
    'password': 'retention_password'
}

@dataclass
class GASearchSpace:
    max_depth: tuple = (3, 10)          # int
    learning_rate: tuple = (0.01, 0.3)  # float
    n_estimators: tuple = (200, 1200)   # int
    min_child_weight: tuple = (1, 10)   # int
    subsample: tuple = (0.6, 1.0)       # float
    colsample_bytree: tuple = (0.5, 1.0)# float
    gamma: tuple = (0.0, 5.0)           # float
    reg_lambda: tuple = (0.0, 20.0)     # float
    reg_alpha: tuple = (0.0, 5.0)       # float


def parse_args():
    p = argparse.ArgumentParser(description="GA‑XGBoost churn prediction (DB version)")
    p.add_argument('--table', required=True, help='DB 테이블명')
    p.add_argument('--target', required=True, help='타깃 컬럼명(0/1)')
    p.add_argument('--id_col', default=None, help='고객 ID 컬럼명(선택)')
    p.add_argument('--date_col', default=None, help='시계열 분할용 날짜 컬럼(선택)')
    p.add_argument('--test_size', type=float, default=0.2, help='테스트 비율(default 0.2)')
    p.add_argument('--kfold', type=int, default=5, help='교차검증 폴드')
    p.add_argument('--generations', type=int, default=20)
    p.add_argument('--population', type=int, default=36)
    p.add_argument('--elitism', type=int, default=2)
    p.add_argument('--cx_rate', type=float, default=0.8, help='교차율')
    p.add_argument('--mut_rate', type=float, default=0.15, help='돌연변이율')
    p.add_argument('--precision_k', type=float, default=0.1, help='Precision@k, k는 상위 비율(0~1)')
    p.add_argument('--outdir', default='outputs', help='결과 출력 폴더')
    p.add_argument('--scoring', default='pr_auc', choices=['pr_auc','f1'], help='GA 적합도 지표')
    p.add_argument('--threads', type=int, default=0, help='XGB n_jobs(0이면 자동)')
    return p.parse_args()


def load_data_from_db(table_name):
    """
    PostgreSQL DB에서 데이터 로드
    """
    try:
        # SQLAlchemy 엔진 생성
        engine = create_engine(
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )
        
        print(f"DB에서 데이터를 로드하는 중: {table_name}")
        
        # 데이터 로드
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        
        print(f"데이터 로드 완료: {len(df)} 행, {len(df.columns)} 컬럼")
        
        return df
        
    except Exception as e:
        print(f"❌ DB 데이터 로드 오류: {str(e)}")
        raise


def save_model_performance_to_db(metrics, best_params, model_path, report_path, args):
    """
    모델 성능을 DB에 저장
    """
    try:
        engine = create_engine(
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )
        
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO ml_model_performance (
                    model_name, model_version, test_size, kfold,
                    roc_auc, pr_auc, f1_score, precision_score, recall_score, brier_score,
                    precision_at_k, recall_at_k, best_params, model_path, report_path
                ) VALUES (
                    :model_name, :model_version, :test_size, :kfold,
                    :roc_auc, :pr_auc, :f1_score, :precision_score, :recall_score, :brier_score,
                    :precision_at_k, :recall_at_k, :best_params, :model_path, :report_path
                )
            """), {
                'model_name': 'GA-XGBoost-Churn',
                'model_version': datetime.now().strftime('%Y%m%d_%H%M%S'),
                'test_size': args.test_size,
                'kfold': args.kfold,
                'roc_auc': metrics.get('roc_auc', 0),
                'pr_auc': metrics.get('pr_auc', 0),
                'f1_score': metrics.get('f1', 0),
                'precision_score': metrics.get('precision', 0),
                'recall_score': metrics.get('recall', 0),
                'brier_score': metrics.get('brier', 0),
                'precision_at_k': metrics.get('precision_at_k', 0),
                'recall_at_k': metrics.get('recall_at_k', 0),
                'best_params': json.dumps(best_params),
                'model_path': model_path,
                'report_path': report_path
            })
            conn.commit()
            
        print("✅ 모델 성능이 DB에 저장되었습니다.")
        
    except Exception as e:
        print(f"❌ DB 저장 오류: {str(e)}")


def split_train_test(df, target, date_col=None, test_size=0.2):
    if date_col and date_col in df.columns:
        # 시간 기준 분할 (최근 test)
        df = df.sort_values(by=date_col)
        cutoff = int((1 - test_size) * len(df))
        train_df = df.iloc[:cutoff]
        test_df = df.iloc[cutoff:]
    else:
        train_df, test_df = train_test_split(df, test_size=test_size, stratify=df[target], random_state=RANDOM_STATE)
    return train_df, test_df


def build_preprocessor(df, target, id_col=None):
    feat_cols = [c for c in df.columns if c != target and c != id_col]
    num_cols = [c for c in feat_cols if pd.api.types.is_numeric_dtype(df[c])]
    cat_cols = [c for c in feat_cols if not pd.api.types.is_numeric_dtype(df[c])]

    num_pipe = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    cat_pipe = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    pre = ColumnTransformer(
        transformers=[
            ('num', num_pipe, num_cols),
            ('cat', cat_pipe, cat_cols)
        ], remainder='drop'
    )
    return pre, num_cols, cat_cols


def compute_scale_pos_weight(y):
    # neg/pos 비율
    pos = (y == 1).sum()
    neg = (y == 0).sum()
    if pos == 0:
        return 1.0
    return float(neg) / float(pos)


def sample_params(space: GASearchSpace):
    # 연속형은 균등샘플, 정수형은 반올림
    d = {
        'max_depth': int(np.random.randint(space.max_depth[0], space.max_depth[1] + 1)),
        'learning_rate': float(np.random.uniform(*space.learning_rate)),
        'n_estimators': int(np.random.randint(space.n_estimators[0], space.n_estimators[1] + 1)),
        'min_child_weight': int(np.random.randint(space.min_child_weight[0], space.min_child_weight[1] + 1)),
        'subsample': float(np.random.uniform(*space.subsample)),
        'colsample_bytree': float(np.random.uniform(*space.colsample_bytree)),
        'gamma': float(np.random.uniform(*space.gamma)),
        'reg_lambda': float(np.random.uniform(*space.reg_lambda)),
        'reg_alpha': float(np.random.uniform(*space.reg_alpha)),
    }
    return d


def mutate(params, space: GASearchSpace, rate=0.15):
    newp = params.copy()
    for k in newp:
        if np.random.rand() < rate:
            # 작은 노이즈 추가 후 경계 클리핑/반올림
            if k in ['max_depth','n_estimators','min_child_weight']:
                span = getattr(space, k)[1] - getattr(space, k)[0]
                step = max(1, int(0.1*span))
                newp[k] = int(np.clip(newp[k] + np.random.randint(-step, step+1), getattr(space,k)[0], getattr(space,k)[1]))
            else:
                lo, hi = getattr(space, k)
                noise = (hi - lo) * 0.1 * np.random.randn()
                newp[k] = float(np.clip(newp[k] + noise, lo, hi))
    return newp


def crossover(p1, p2):
    c1, c2 = {}, {}
    for k in p1:
        if np.random.rand() < 0.5:
            c1[k] = p1[k]
            c2[k] = p2[k]
        else:
            c1[k] = p2[k]
            c2[k] = p1[k]
    return c1, c2


def eval_params(params, X, y, preprocessor, kfold=5, scoring='pr_auc', threads=0):
    # 교차검증으로 적합도 계산
    skf = StratifiedKFold(n_splits=kfold, shuffle=True, random_state=RANDOM_STATE)
    pr_aucs, f1s = [], []
    for tr_idx, va_idx in skf.split(X, y):
        Xtr, Xva = X.iloc[tr_idx], X.iloc[va_idx]
        ytr, yva = y.iloc[tr_idx], y.iloc[va_idx]
        spw = compute_scale_pos_weight(ytr)
        clf = XGBClassifier(
            objective='binary:logistic',
            eval_metric='logloss',
            tree_method='hist',
            random_state=RANDOM_STATE,
            n_jobs=None if threads==0 else threads,
            **params,
            scale_pos_weight=spw
        )
        pipe = Pipeline(steps=[('pre', preprocessor), ('clf', clf)])
        pipe.fit(Xtr, ytr)
        proba = pipe.predict_proba(Xva)[:,1]
        pr_auc = average_precision_score(yva, proba)
        pr_aucs.append(pr_auc)
        # F1@0.5 threshold
        pred = (proba >= 0.5).astype(int)
        f1s.append(2 * (precision_score(yva, pred, zero_division=0) * recall_score(yva, pred, zero_division=0)) / max(1e-9, (precision_score(yva, pred, zero_division=0) + recall_score(yva, pred, zero_division=0))))
    score = np.mean(pr_aucs) if scoring=='pr_auc' else np.mean(f1s)
    return score, np.mean(pr_aucs), np.mean(f1s)


def ga_optimize(X, y, preprocessor, generations=20, population=36, elitism=2, cx_rate=0.8, mut_rate=0.15, kfold=5, scoring='pr_auc', threads=0):
    space = GASearchSpace()
    pop = [sample_params(space) for _ in range(population)]
    history = []
    for g in range(generations):
        fitness = []
        for params in pop:
            s, prauc, f1 = eval_params(params, X, y, preprocessor, kfold=kfold, scoring=scoring, threads=threads)
            fitness.append((s, prauc, f1, params))
        fitness.sort(key=lambda x: x[0], reverse=True)
        best = fitness[0]
        history.append({'gen': g, 'best_score': best[0], 'best_params': best[3]})
        print(f"[GA] gen {g:02d} best {scoring}={best[0]:.4f} (PR-AUC={best[1]:.4f}, F1={best[2]:.4f})")
        # 다음 세대 구성
        new_pop = [f[3] for f in fitness[:elitism]]  # elitism
        while len(new_pop) < population:
            # 토너먼트 선택
            def tournament():
                k = 3
                cand = [fitness[np.random.randint(0, len(fitness))] for _ in range(k)]
                cand.sort(key=lambda x: x[0], reverse=True)
                return cand[0][3]
            p1, p2 = tournament(), tournament()
            if np.random.rand() < cx_rate:
                c1, c2 = crossover(p1, p2)
            else:
                c1, c2 = p1.copy(), p2.copy()
            c1 = mutate(c1, space, rate=mut_rate)
            c2 = mutate(c2, space, rate=mut_rate)
            new_pop.extend([c1, c2])
        pop = new_pop[:population]
    # 최종 평가 후 최고 파라미터 반환
    final_fit = []
    for params in pop:
        s, prauc, f1 = eval_params(params, X, y, preprocessor, kfold=kfold, scoring=scoring, threads=threads)
        final_fit.append((s, prauc, f1, params))
    final_fit.sort(key=lambda x: x[0], reverse=True)
    return final_fit[0][3], history


def precision_recall_at_k(y_true, y_proba, k_ratio=0.1):
    n = len(y_true)
    k = max(1, int(n * k_ratio))
    order = np.argsort(-y_proba)
    topk = order[:k]
    y_pred_topk = np.zeros(n, dtype=int)
    y_pred_topk[topk] = 1
    prec = precision_score(y_true, y_pred_topk, zero_division=0)
    rec = recall_score(y_true, y_pred_topk, zero_division=0)
    return prec, rec


def train_best_model(train_df, test_df, target, id_col, pre, best_params, threads=0):
    X_tr = train_df.drop(columns=[target] + ([id_col] if id_col and id_col in train_df.columns else []))
    y_tr = train_df[target]
    X_te = test_df.drop(columns=[target] + ([id_col] if id_col and id_col in test_df.columns else []))
    y_te = test_df[target]

    spw = compute_scale_pos_weight(y_tr)
    clf = XGBClassifier(
        objective='binary:logistic',
        eval_metric='logloss',
        tree_method='hist',
        random_state=RANDOM_STATE,
        n_jobs=None if threads==0 else threads,
        **best_params,
        scale_pos_weight=spw
    )
    pipe = Pipeline(steps=[('pre', pre), ('clf', clf)])
    pipe.fit(X_tr, y_tr)

    proba = pipe.predict_proba(X_te)[:,1]
    pred = (proba >= 0.5).astype(int)

    metrics = {}
    metrics['roc_auc'] = float(roc_auc_score(y_te, proba))
    metrics['pr_auc'] = float(average_precision_score(y_te, proba))
    metrics['brier'] = float(brier_score_loss(y_te, proba))
    metrics['f1'] = float(2 * (precision_score(y_te, pred, zero_division=0) * recall_score(y_te, pred, zero_division=0)) / max(1e-9, (precision_score(y_te, pred, zero_division=0) + recall_score(y_te, pred, zero_division=0))))
    metrics['precision'] = float(precision_score(y_te, pred, zero_division=0))
    metrics['recall'] = float(recall_score(y_te, pred, zero_division=0))

    return pipe, proba, pred, y_te, metrics


def save_plots(y_true, proba, outdir):
    import matplotlib.pyplot as plt

    # PR curve
    precision, recall, _ = precision_recall_curve(y_true, proba)
    ap = average_precision_score(y_true, proba)
    plt.figure()
    plt.step(recall, precision, where='post')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title(f'Precision-Recall Curve (AP={ap:.3f})')
    pr_path = os.path.join(outdir, 'pr_curve.png')
    plt.savefig(pr_path, bbox_inches='tight', dpi=150)
    plt.close()

    # ROC curve
    fpr, tpr, _ = roc_curve(y_true, proba)
    auc = roc_auc_score(y_true, proba)
    plt.figure()
    plt.plot(fpr, tpr)
    plt.plot([0,1],[0,1],'--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve (AUC={auc:.3f})')
    roc_path = os.path.join(outdir, 'roc_curve.png')
    plt.savefig(roc_path, bbox_inches='tight', dpi=150)
    plt.close()

    return pr_path, roc_path


def save_confusion_matrix(y_true, y_pred, outdir):
    import matplotlib.pyplot as plt
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest')
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=np.arange(cm.shape[1]), yticks=np.arange(cm.shape[0]),
           xticklabels=['Pred 0','Pred 1'], yticklabels=['True 0','True 1'],
           ylabel='True label', xlabel='Predicted label', title='Confusion Matrix')
    # 값 표시
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'), ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    cm_path = os.path.join(outdir, 'confusion_matrix.png')
    fig.tight_layout()
    plt.savefig(cm_path, bbox_inches='tight', dpi=150)
    plt.close(fig)
    return cm_path


def save_feature_importance(pipeline, outdir):
    # XGB의 gain 기반 중요도 저장 (전처리 후 피처명 복원은 간단화)
    clf: XGBClassifier = pipeline.named_steps['clf']
    booster = clf.get_booster()
    fmap = booster.get_fscore()
    # 키가 f0,f1... 형식 → 정렬
    items = sorted(fmap.items(), key=lambda kv: kv[1], reverse=True)
    fi_df = pd.DataFrame(items, columns=['feature','importance'])
    fi_path = os.path.join(outdir, 'feature_importance_xgb.csv')
    fi_df.to_csv(fi_path, index=False)
    return fi_path


def save_shap_reports(pipeline, X_sample, outdir):
    if not _HAS_SHAP:
        return None, None
    try:
        explainer = shap.TreeExplainer(pipeline.named_steps['clf'])
        # 전처리 적용 후 SHAP 값을 계산해야 하므로, 전처리 변환행렬에 대해 계산
        X_trans = pipeline.named_steps['pre'].transform(X_sample)
        shap_values = explainer.shap_values(X_trans)
        # 요약 플롯
        shap.summary_plot(shap_values, X_trans, show=False)
        sum_path = os.path.join(outdir, 'shap_summary.png')
        import matplotlib.pyplot as plt
        plt.savefig(sum_path, bbox_inches='tight', dpi=150)
        plt.close()
        # 첫 샘플 waterfall
        shap.plots._waterfall.waterfall_legacy(explainer.expected_value, shap_values[0], show=False)
        wf_path = os.path.join(outdir, 'shap_waterfall_sample0.png')
        plt.savefig(wf_path, bbox_inches='tight', dpi=150)
        plt.close()
        return sum_path, wf_path
    except Exception as e:
        warnings.warn(f"SHAP 리포트 생성 중 오류: {e}")
        return None, None


def generate_markdown_report(outdir, args, metrics, k_prec, k_rec, paths, best_params, classif_report):
    report_md = os.path.join(outdir, 'report.md')
    with open(report_md, 'w', encoding='utf-8') as f:
        f.write(f"# GA‑XGBoost Churn Report (DB Version)\n\n")
        f.write(f"- 생성일: {datetime.now().isoformat()}\n")
        f.write(f"- 데이터 소스: DB 테이블 '{args.table}'\n")
        f.write(f"- 타깃: {args.target}  |  테스트비율: {args.test_size}  |  KFold: {args.kfold}\n\n")
        f.write("## 최적 하이퍼파라미터\n")
        f.write("```json\n" + json.dumps(best_params, indent=2) + "\n```\n\n")
        f.write("## 테스트 성능\n")
        for k,v in metrics.items():
            f.write(f"- {k}: {v:.4f}\n")
        f.write(f"- Precision@{args.precision_k*100:.0f}%: {k_prec:.4f}\n")
        f.write(f"- Recall@{args.precision_k*100:.0f}%: {k_rec:.4f}\n\n")
        f.write("### 분류 리포트\n")
        f.write("```\n" + classif_report + "\n```\n\n")
        f.write("## 시각화 파일\n")
        for name, p in paths.items():
            if p:
                f.write(f"- {name}: {os.path.basename(p)}\n")
        f.write("\n")
    return report_md


def main():
    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    # DB에서 데이터 로드
    df = load_data_from_db(args.table)
    assert args.target in df.columns, f"타깃 컬럼 {args.target} 이(가) 존재하지 않습니다."

    # 날짜 컬럼 파싱(있다면)
    if args.date_col and args.date_col in df.columns:
        try:
            df[args.date_col] = pd.to_datetime(df[args.date_col])
        except Exception:
            pass

    train_df, test_df = split_train_test(df, target=args.target, date_col=args.date_col, test_size=args.test_size)

    pre, num_cols, cat_cols = build_preprocessor(train_df, target=args.target, id_col=args.id_col)

    # GA 최적화(학습 데이터만 사용)
    X_train = train_df.drop(columns=[args.target] + ([args.id_col] if args.id_col and args.id_col in train_df.columns else []))
    y_train = train_df[args.target]

    best_params, history = ga_optimize(
        X_train, y_train, preprocessor=pre,
        generations=args.generations, population=args.population, elitism=args.elitism,
        cx_rate=args.cx_rate, mut_rate=args.mut_rate, kfold=args.kfold,
        scoring=args.scoring, threads=args.threads)

    with open(os.path.join(args.outdir, 'ga_history.json'), 'w', encoding='utf-8') as fp:
        json.dump(history, fp, ensure_ascii=False, indent=2)

    # 최적 파라미터로 최종 학습/평가
    pipeline, proba, pred, y_true, metrics = train_best_model(train_df, test_df, args.target, args.id_col, pre, best_params, threads=args.threads)

    # 지표 추가: Precision@k, Recall@k
    pk, rk = precision_recall_at_k(y_true.values, proba, k_ratio=args.precision_k)
    metrics['precision_at_k'] = pk
    metrics['recall_at_k'] = rk

    # 분류 리포트
    clf_rep = classification_report(y_true, pred, digits=4)

    # 아티팩트 저장
    import joblib
    model_path = os.path.join(args.outdir, 'model_pipeline.joblib')
    joblib.dump(pipeline, model_path)

    pr_path, roc_path = save_plots(y_true, proba, args.outdir)
    cm_path = save_confusion_matrix(y_true, pred, args.outdir)
    fi_path = save_feature_importance(pipeline, args.outdir)

    # SHAP 리포트(샘플 2k 제한)
    shap_sum, shap_wf = None, None
    try:
        X_sample = train_df.drop(columns=[args.target] + ([args.id_col] if args.id_col and args.id_col in train_df.columns else [])).sample(n=min(2000, len(train_df)), random_state=RANDOM_STATE)
        shap_sum, shap_wf = save_shap_reports(pipeline, X_sample, args.outdir)
    except Exception as e:
        warnings.warn(f"SHAP 샘플링/저장 실패: {e}")

    paths = {
        'PR Curve': pr_path,
        'ROC Curve': roc_path,
        'Confusion Matrix': cm_path,
        'Feature Importance (CSV)': fi_path,
        'SHAP Summary': shap_sum,
        'SHAP Waterfall(sample0)': shap_wf,
        'Model Pipeline': model_path,
        'GA History': os.path.join(args.outdir, 'ga_history.json')
    }

    report_md = generate_markdown_report(args.outdir, args, metrics, pk, rk, paths, best_params, clf_rep)

    # DB에 모델 성능 저장
    save_model_performance_to_db(metrics, best_params, model_path, report_md, args)

    # 메타 정보 저장
    meta = {
        'args': vars(args),
        'metrics': metrics,
        'precision_at_k': pk,
        'recall_at_k': rk,
        'best_params': best_params,
        'artifacts': paths,
        'report_md': report_md,
        'numeric_features': num_cols,
        'categorical_features': cat_cols
    }
    with open(os.path.join(args.outdir, 'run_meta.json'), 'w', encoding='utf-8') as fp:
        json.dump(meta, fp, ensure_ascii=False, indent=2)

    print("=== 완료 ===")
    print(json.dumps({'metrics': metrics, 'precision_at_k': pk, 'recall_at_k': rk, 'best_params': best_params, 'report': report_md}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
