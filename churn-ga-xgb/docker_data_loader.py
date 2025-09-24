#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import os
import sys
from datetime import datetime


# Kaffle CSV 파일 PostgreSQL DB 적재
def load_data_to_db(csv_file_path, schemas='ml', table_name='ml_training_data'):
    """
    Args:
        csv_file_path (str): CSV 파일 경로
        table_name (str): 테이블 이름
    """
    
    # Docker 네트워크 내에서의 데이터베이스 연결 설정
    DB_CONFIG = {
        'host': 'postgres',  # Docker 서비스명
        'port': 5432,
        'database': 'retention_db',
        'user': 'retention_user',
        'password': 'retention_password'
    }
    
    try:
        print(f"CSV 파일을 읽는 중: {csv_file_path}")
        
        # CSV 파일 읽기
        df = pd.read_csv(csv_file_path, encoding='utf-8')
        print(f"데이터 로드 완료: {len(df)} 행, {len(df.columns)} 컬럼")
        
        # 컬럼 정보 출력
        print("\n컬럼 정보:")
        for i, col in enumerate(df.columns):
            print(f"{i+1:2d}. {col} ({df[col].dtype})")
        
        # 데이터베이스 연결
        print(f"\n데이터베이스에 연결 중...")
        engine = create_engine(
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )
        
        # 기존 테이블이 있으면 삭제
        with engine.connect() as conn:
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
            conn.commit()
        
        print(f"테이블 '{table_name}' 생성 중...")
        
        # 데이터를 DB에 적재
        df.to_sql(
            schemas,
            table_name, 
            engine, 
            if_exists='replace', 
            index=False,
            method='multi',
            chunksize=1000
        )
        
        # 테이블 정보 확인
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            row_count = result.fetchone()[0]
            
            result = conn.execute(text(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position
            """))
            columns_info = result.fetchall()
        
        print(f"\n✅ 데이터 적재 완료!")
        print(f"테이블: {table_name}")
        print(f"행 수: {row_count:,}")
        print(f"컬럼 수: {len(columns_info)}")
        
        print(f"\n테이블 스키마:")
        for col_name, data_type, is_nullable in columns_info:
            print(f"  {col_name}: {data_type} ({'NULL' if is_nullable == 'YES' else 'NOT NULL'})")
        
        # 샘플 데이터 출력
        print(f"\n샘플 데이터 (처음 5행):")
        sample_df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5", engine)
        print(sample_df.to_string(index=False))
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

def create_ml_tables(engine):
    """
    머신러닝 관련 추가 테이블 생성
    """
    try:
        with engine.connect() as conn:
            # 모델 성능 기록 테이블
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ml.ml_model_performance (
                    id SERIAL PRIMARY KEY,
                    model_name VARCHAR(100) NOT NULL,
                    model_version VARCHAR(50),
                    training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    test_size DECIMAL(3,2),
                    kfold INTEGER,
                    roc_auc DECIMAL(6,4),
                    pr_auc DECIMAL(6,4),
                    f1_score DECIMAL(6,4),
                    precision_score DECIMAL(6,4),
                    recall_score DECIMAL(6,4),
                    brier_score DECIMAL(6,4),
                    precision_at_k DECIMAL(6,4),
                    recall_at_k DECIMAL(6,4),
                    best_params JSONB,
                    model_path VARCHAR(255),
                    report_path VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # 예측 결과 테이블
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ml.ml_predictions (
                    id SERIAL PRIMARY KEY,
                    customer_id VARCHAR(100),
                    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    churn_probability DECIMAL(6,4),
                    churn_prediction BOOLEAN,
                    model_version VARCHAR(50),
                    confidence_score DECIMAL(6,4),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            conn.commit()
            print("✅ 머신러닝 관련 테이블 생성 완료")
            
    except Exception as e:
        print(f"❌ 테이블 생성 오류: {str(e)}")

def main():
    csv_file = "/app/data/Preprocessed_Data_Improved_cleaned.csv"
    
    if not os.path.exists(csv_file):
        print(f"❌ 파일을 찾을 수 없습니다: {csv_file}")
        sys.exit(1)
    
    print("=== 머신러닝 데이터 적재 시작 (Docker) ===")
    print(f"시작 시간: {datetime.now()}")
    
    # 데이터 적재
    success = load_data_to_db(csv_file, 'ml_training_data')
    
    if success:
        # 머신러닝 관련 테이블 생성
        DB_CONFIG = {
            'host': 'postgres',
            'port': 5432,
            'database': 'retention_db',
            'user': 'retention_user',
            'password': 'retention_password'
        }
        
        engine = create_engine(
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )
        
        create_ml_tables(engine)
        
        print(f"\n🎉 모든 작업 완료!")
        print(f"완료 시간: {datetime.now()}")
    else:
        print(f"\n❌ 데이터 적재 실패")
        sys.exit(1)

if __name__ == "__main__":
    main()
