#!/bin/bash

echo "=================================================="
echo "대출 금융 데이터 생성기"
echo "=================================================="

# 기본값 설정
DEFAULT_RECORDS=1000
RECORDS=${1:-$DEFAULT_RECORDS}

echo "생성할 대출 데이터 개수: $RECORDS"
echo ""

# Docker 이미지 빌드
echo "Docker 이미지를 빌드합니다..."
docker build -t loan-data-generator .

# 데이터 생성 실행
echo "데이터를 생성합니다..."
docker run --network host -e PYTHONUNBUFFERED=1 loan-data-generator python -c "
import sys
sys.path.append('/app')
from loan_data_generator import LoanDataGenerator

db_config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'retention_db',
    'user': 'retention_user',
    'password': 'retention_password'
}

generator = LoanDataGenerator(db_config)
generator.generate_and_save_data($RECORDS)
"

echo ""
echo "=================================================="
echo "데이터 생성이 완료되었습니다!"
echo "=================================================="
