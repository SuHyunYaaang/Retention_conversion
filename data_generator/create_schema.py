#!/usr/bin/env python3
"""
customers 스키마 생성 스크립트
"""

import psycopg2
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_customers_schema():
    """customers 스키마 및 테이블 생성"""
    
    # 데이터베이스 연결 설정 (Docker 환경)
    db_config = {
        "host": "postgres",  # Docker 서비스명
        "port": 5432,
        "database": "retention_db",
        "user": "retention_user",
        "password": "retention_password"
    }
    
    conn = None
    try:
        # 데이터베이스 연결
        conn = psycopg2.connect(**db_config)
        conn.set_client_encoding('UTF8')
        logger.info("데이터베이스에 연결되었습니다.")
        
        with conn.cursor() as cursor:
            # customers 스키마 생성
            cursor.execute("CREATE SCHEMA IF NOT EXISTS customers")
            logger.info("customers 스키마가 생성되었습니다.")
            
            # 고객 테이블 생성
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers.customers (
                    id SERIAL PRIMARY KEY,
                    customer_id VARCHAR(20) UNIQUE NOT NULL,
                    name VARCHAR(50) NOT NULL,
                    age INTEGER,
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    job_type VARCHAR(30),
                    income_level VARCHAR(50),
                    credit_grade VARCHAR(10),
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            logger.info("customers.customers 테이블이 생성되었습니다.")
            
            # 대출 테이블 생성
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers.loans (
                    id SERIAL PRIMARY KEY,
                    loan_id VARCHAR(20) UNIQUE NOT NULL,
                    customer_id VARCHAR(20) REFERENCES customers.customers(customer_id),
                    loan_type VARCHAR(30) NOT NULL,
                    loan_amount INTEGER NOT NULL,
                    loan_term INTEGER NOT NULL,
                    interest_rate DECIMAL(5,2) NOT NULL,
                    monthly_payment INTEGER NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    application_date TIMESTAMP,
                    approval_date TIMESTAMP,
                    disbursement_date TIMESTAMP,
                    overdue_days INTEGER DEFAULT 0,
                    overdue_amount INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            logger.info("customers.loans 테이블이 생성되었습니다.")
            
            # 상환 테이블 생성
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers.repayments (
                    id SERIAL PRIMARY KEY,
                    payment_id VARCHAR(20) UNIQUE NOT NULL,
                    loan_id VARCHAR(20) REFERENCES customers.loans(loan_id),
                    payment_date TIMESTAMP NOT NULL,
                    payment_amount INTEGER NOT NULL,
                    principal_amount INTEGER NOT NULL,
                    interest_amount INTEGER NOT NULL,
                    is_overdue BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            logger.info("customers.repayments 테이블이 생성되었습니다.")
            
            conn.commit()
            logger.info("모든 테이블이 성공적으로 생성되었습니다.")
            
    except Exception as e:
        logger.error(f"스키마 생성 중 오류 발생: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_customers_schema()
