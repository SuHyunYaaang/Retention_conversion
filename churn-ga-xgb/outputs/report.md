# GA‑XGBoost Churn Report (DB Version)

- 생성일: 2025-08-15T07:43:45.238617
- 데이터 소스: DB 테이블 'ml_training_data'
- 타깃: everdelinquent  |  테스트비율: 0.2  |  KFold: 5

## 최적 하이퍼파라미터
```json
{
  "max_depth": 3,
  "learning_rate": 0.10116323451213473,
  "n_estimators": 387,
  "min_child_weight": 8,
  "subsample": 0.9630265895704372,
  "colsample_bytree": 1.0,
  "gamma": 2.0519146151781484,
  "reg_lambda": 16.590888637746204,
  "reg_alpha": 0.6552097647217688
}
```

## 테스트 성능
- roc_auc: 0.6082
- pr_auc: 0.6744
- brier: 0.2361
- f1: 0.6640
- precision: 0.6385
- recall: 0.6917
- precision_at_k: 0.7500
- recall_at_k: 0.1250
- Precision@10%: 0.7500
- Recall@10%: 0.1250

### 분류 리포트
```
              precision    recall  f1-score   support

           0     0.4714    0.4125    0.4400        80
           1     0.6385    0.6917    0.6640       120

    accuracy                         0.5800       200
   macro avg     0.5549    0.5521    0.5520       200
weighted avg     0.5716    0.5800    0.5744       200

```

## 시각화 파일
- PR Curve: pr_curve.png
- ROC Curve: roc_curve.png
- Confusion Matrix: confusion_matrix.png
- Feature Importance (CSV): feature_importance_xgb.csv
- SHAP Summary: shap_summary.png
- SHAP Waterfall(sample0): shap_waterfall_sample0.png
- Model Pipeline: model_pipeline.joblib
- GA History: ga_history.json

