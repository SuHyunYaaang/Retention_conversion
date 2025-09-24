# 간단한 머신러닝 실행 스크립트 (PowerShell)
# 사용법: .\run_simple_ml.ps1

Write-Host "=== 간단한 머신러닝 실행 ===" -ForegroundColor Green

# 먼저 데이터를 DB에 적재
Write-Host "1. 데이터를 DB에 적재하는 중..." -ForegroundColor Yellow
docker exec retention_postgres psql -U retention_user -d retention_db -c "
DROP TABLE IF EXISTS ml_training_data CASCADE;
CREATE TABLE ml_training_data (
    CreditScore FLOAT,
    FirstTimeHomebuyer INTEGER,
    MSA INTEGER,
    MIP INTEGER,
    Units INTEGER,
    Occupancy VARCHAR(10),
    OCLTV INTEGER,
    DTI FLOAT,
    OrigUPB INTEGER,
    LTV FLOAT,
    OrigInterestRate FLOAT,
    Channel VARCHAR(10),
    PPM INTEGER,
    PropertyState VARCHAR(50),
    PropertyType VARCHAR(10),
    LoanPurpose VARCHAR(10),
    OrigLoanTerm FLOAT,
    NumBorrowers INTEGER,
    SellerName VARCHAR(50),
    ServicerName VARCHAR(50),
    EverDelinquent FLOAT,
    MonthsDelinquent FLOAT,
    MonthsInRepayment FLOAT,
    FirstPayment_Year INTEGER,
    FirstPayment_Month VARCHAR(10),
    Parsed_FirstPaymentDate VARCHAR(20),
    Maturity_Year INTEGER,
    Maturity_Month INTEGER,
    Parsed_MaturityDate VARCHAR(20)
);
"

Write-Host "2. CSV 데이터를 테이블에 복사하는 중..." -ForegroundColor Yellow
docker exec retention_postgres psql -U retention_user -d retention_db -c "
\copy ml_training_data FROM '/tmp/Preprocessed_Data_Improved_cleaned.csv' WITH (FORMAT csv, HEADER true);
"

Write-Host "3. 데이터 적재 확인..." -ForegroundColor Yellow
docker exec retention_postgres psql -U retention_user -d retention_db -c "SELECT COUNT(*) FROM ml_training_data;"

Write-Host "4. 머신러닝 모델 학습 시작..." -ForegroundColor Yellow
docker-compose --profile ml run --rm --entrypoint python ml-service churn-ga-xgb-db.py `
    --table ml_training_data `
    --target EverDelinquent `
    --id_col "CreditScore" `
    --test_size 0.2 `
    --kfold 5 `
    --generations 10 `
    --population 20 `
    --precision_k 0.1 `
    --outdir "/app/outputs" `
    --scoring pr_auc `
    --threads 0

Write-Host "=== 완료 ===" -ForegroundColor Green
