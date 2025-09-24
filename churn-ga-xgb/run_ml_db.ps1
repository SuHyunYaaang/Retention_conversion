# 머신러닝 서비스 실행 스크립트 (DB 버전 - PowerShell)
# 사용법: .\run_ml_db.ps1 [테이블명] [타겟컬럼]

param(
    [string]$TableName = "ml_training_data",
    [string]$TargetCol = "EverDelinquent"
)

$OutputDir = "outputs"

Write-Host "=== GA-XGBoost Churn Prediction Service (DB Version) ===" -ForegroundColor Green
Write-Host "테이블명: $TableName" -ForegroundColor Yellow
Write-Host "타겟 컬럼: $TargetCol" -ForegroundColor Yellow
Write-Host "출력 디렉토리: $OutputDir" -ForegroundColor Yellow
Write-Host ""

# 출력 디렉토리 생성
if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

# 머신러닝 서비스 실행
Write-Host "머신러닝 모델 학습을 시작합니다..." -ForegroundColor Cyan
docker-compose --profile ml run --rm ml-service `
    --table $TableName `
    --target $TargetCol `
    --id_col "index" `
    --date_col "Parsed_FirstPaymentDate" `
    --test_size 0.2 `
    --kfold 5 `
    --generations 20 `
    --population 36 `
    --precision_k 0.1 `
    --outdir "/app/outputs" `
    --scoring pr_auc `
    --threads 0

Write-Host ""
Write-Host "=== 학습 완료 ===" -ForegroundColor Green
Write-Host "결과 파일들이 $OutputDir 디렉토리에 저장되었습니다." -ForegroundColor Yellow
Write-Host ""
Write-Host "생성된 파일들:" -ForegroundColor Cyan
Get-ChildItem $OutputDir | Format-Table Name, Length, LastWriteTime
