# GA-XGBoost Churn Prediction Service

고객 이탈(Churn) 예측을 위한 GA-XGBoost 머신러닝 서비스입니다.

## 🚀 주요 기능

- **GA(Genetic Algorithm) 기반 하이퍼파라미터 최적화**
- **XGBoost 모델 학습 및 예측**
- **SHAP 기반 모델 해석**
- **다양한 성능 지표 평가** (ROC-AUC, PR-AUC, F1, Precision@k, Recall@k)
- **자동 리포트 생성** (Markdown, 시각화, 모델 저장)

## 📁 프로젝트 구조

```
churn-ga-xgb/
├── churn-ga-xgb.py      # 메인 머신러닝 스크립트
├── Dockerfile           # 컨테이너 설정
├── requirements.txt     # Python 의존성
├── run_ml.ps1          # Windows 실행 스크립트
├── run_ml.sh           # Linux/Mac 실행 스크립트
├── data/               # 데이터 파일 디렉토리
├── outputs/            # 결과 출력 디렉토리
└── README.md           # 이 파일
```

## 🛠️ 설치 및 실행

### 1. 데이터 준비
```bash
# data 디렉토리에 CSV 파일을 넣어주세요
# 예: data/churn_data.csv
```

### 2. 머신러닝 서비스 빌드
```bash
# Windows PowerShell
docker-compose --profile ml build ml-service

# Linux/Mac
docker-compose --profile ml build ml-service
```

### 3. 모델 학습 실행

#### Windows PowerShell:
```powershell
# 기본 실행
.\run_ml.ps1

# 커스텀 파라미터로 실행
.\run_ml.ps1 "data/my_data.csv" "target_column"
```

#### Linux/Mac:
```bash
# 기본 실행
./run_ml.sh

# 커스텀 파라미터로 실행
./run_ml.sh "data/my_data.csv" "target_column"
```

#### 직접 Docker 명령어:
```bash
docker-compose --profile ml run --rm ml-service \
    --csv /app/data/churn_data.csv \
    --target churn \
    --test_size 0.2 \
    --kfold 5 \
    --generations 20 \
    --population 36 \
    --precision_k 0.1 \
    --outdir /app/outputs \
    --scoring pr_auc
```

## 📊 입력 데이터 형식

### CSV 파일 요구사항:
- **타겟 컬럼**: 이진값 (0/1) - 이탈 여부
- **수치형 컬럼**: 자동으로 StandardScaler 적용
- **범주형 컬럼**: 자동으로 OneHotEncoder 적용
- **ID 컬럼**: 선택사항 (--id_col로 지정)
- **날짜 컬럼**: 선택사항 (--date_col로 지정, 시계열 분할용)

### 예시 데이터:
```csv
customer_id,age,income,tenure,contract_type,churn
CUST001,35,50000,24,monthly,0
CUST002,42,75000,12,yearly,1
CUST003,28,35000,6,monthly,0
...
```

## ⚙️ 주요 파라미터

| 파라미터 | 기본값 | 설명 |
|---------|--------|------|
| `--csv` | 필수 | 입력 CSV 파일 경로 |
| `--target` | 필수 | 타겟 컬럼명 |
| `--test_size` | 0.2 | 테스트 데이터 비율 |
| `--kfold` | 5 | 교차검증 폴드 수 |
| `--generations` | 20 | GA 세대 수 |
| `--population` | 36 | GA 개체 수 |
| `--precision_k` | 0.1 | Precision@k의 k 비율 |
| `--scoring` | pr_auc | GA 적합도 지표 (pr_auc/f1) |
| `--threads` | 0 | XGBoost 스레드 수 (0=자동) |

## 📈 출력 결과

### 생성되는 파일들:
- `model_pipeline.joblib`: 학습된 모델 파이프라인
- `report.md`: 상세 분석 리포트
- `run_meta.json`: 실행 메타데이터
- `ga_history.json`: GA 최적화 히스토리
- `pr_curve.png`: Precision-Recall 곡선
- `roc_curve.png`: ROC 곡선
- `confusion_matrix.png`: 혼동행렬
- `feature_importance_xgb.csv`: 특성 중요도
- `shap_summary.png`: SHAP 요약 플롯 (SHAP 설치 시)
- `shap_waterfall_sample0.png`: SHAP 워터폴 플롯 (SHAP 설치 시)

### 성능 지표:
- **ROC-AUC**: 전체적인 분류 성능
- **PR-AUC**: 불균형 데이터에 적합한 지표
- **F1-Score**: 정밀도와 재현율의 조화평균
- **Precision@k**: 상위 k%에서의 정밀도
- **Recall@k**: 상위 k%에서의 재현율
- **Brier Score**: 확률 예측의 정확도

## 🔧 고급 설정

### GA 하이퍼파라미터 검색 공간:
```python
@dataclass
class GASearchSpace:
    max_depth: tuple = (3, 10)          # 트리 깊이
    learning_rate: tuple = (0.01, 0.3)  # 학습률
    n_estimators: tuple = (200, 1200)   # 트리 개수
    min_child_weight: tuple = (1, 10)   # 최소 자식 가중치
    subsample: tuple = (0.6, 1.0)       # 샘플링 비율
    colsample_bytree: tuple = (0.5, 1.0)# 특성 샘플링 비율
    gamma: tuple = (0.0, 5.0)           # 분할 최소 손실 감소
    reg_lambda: tuple = (0.0, 20.0)     # L2 정규화
    reg_alpha: tuple = (0.0, 5.0)       # L1 정규화
```

### 불균형 데이터 처리:
- **scale_pos_weight**: 자동으로 계산되어 적용
- **StratifiedKFold**: 교차검증에서 클래스 비율 유지
- **PR-AUC**: 불균형 데이터에 적합한 평가 지표

## 🐛 문제 해결

### 일반적인 오류:
1. **메모리 부족**: `--population`과 `--generations` 줄이기
2. **SHAP 오류**: `shap` 패키지가 설치되지 않은 경우 (선택사항)
3. **데이터 형식 오류**: CSV 파일의 컬럼명과 타입 확인

### 로그 확인:
```bash
docker-compose --profile ml logs ml-service
```

## 📝 예시 사용법

### 1. 기본 실행:
```bash
# 데이터 파일을 data/ 디렉토리에 넣고
./run_ml.sh "data/customer_churn.csv" "churn"
```

### 2. 고급 설정:
```bash
docker-compose --profile ml run --rm ml-service \
    --csv /app/data/customer_churn.csv \
    --target churn \
    --id_col customer_id \
    --date_col snapshot_date \
    --test_size 0.3 \
    --kfold 10 \
    --generations 50 \
    --population 50 \
    --precision_k 0.05 \
    --scoring f1 \
    --threads 4 \
    --outdir /app/outputs
```

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
