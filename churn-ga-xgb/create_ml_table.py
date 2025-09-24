#!/usr/bin/env python3
"""
ML 서비스를 위한 테이블 생성 및 샘플 데이터 삽입 스크립트
"""

import psycopg2
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# 데이터베이스 연결 설정
DB_CONFIG = {
    'host': 'postgres',
    'port': 5432,
    'database': 'retention_db',
    'user': 'retention_user',
    'password': 'retention_password'
}

def create_ml_table():
    """ML 학습용 테이블 생성"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # 기존 테이블이 있으면 삭제
    cursor.execute("DROP TABLE IF EXISTS ml.ml_training_data")
    
    # ML 학습용 테이블 생성
    create_table_sql = """
    CREATE TABLE ml.ml_training_data (
        id SERIAL PRIMARY KEY,
        customer_id VARCHAR(50),
        age INTEGER,
        income_level VARCHAR(50),
        credit_grade VARCHAR(10),
        loan_amount DECIMAL(15,2),
        interest_rate DECIMAL(5,2),
        loan_term INTEGER,
        monthly_payment DECIMAL(15,2),
        payment_history_months INTEGER,
        late_payments_3m INTEGER,
        late_payments_6m INTEGER,
        late_payments_12m INTEGER,
        credit_utilization DECIMAL(5,2),
        debt_to_income_ratio DECIMAL(5,2),
        employment_length_years INTEGER,
        number_of_accounts INTEGER,
        inquiries_last_6m INTEGER,
        EverDelinquent INTEGER,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    cursor.execute(create_table_sql)
    conn.commit()
    print("ML 학습용 테이블이 생성되었습니다.")
    
    cursor.close()
    conn.close()

def main():
    """메인 함수"""
    print("ML 서비스용 테이블 및 데이터 준비를 시작합니다...")
    
    # 테이블 생성
    create_ml_table()
    
    print("ML 서비스 준비가 완료되었습니다!")
    print(f"- 테이블명: ml_training_data")
    print(f"- 타겟 컬럼: EverDelinquent")
    print(f"- 데이터 수: {len(df)}개")

if __name__ == "__main__":
    main()
