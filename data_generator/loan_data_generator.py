#!/usr/bin/env python3
"""
대출 금융 데이터 생성 및 DB 적재 스크립트
1000개의 대출 데이터를 생성하여 PostgreSQL 데이터베이스에 저장합니다.
"""

import json
import random
import psycopg2
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LoanDataGenerator:
    def __init__(self, db_config: Dict[str, str]):
        """
        대출 데이터 생성기 초기화
        
        Args:
            db_config: 데이터베이스 연결 설정
        """
        self.db_config = db_config
        
        # 대출 상품 유형
        self.loan_types = [
            "개인신용대출", "담보대출", "전세자금대출", "주택담보대출", 
            "사업자대출", "학자금대출", "자동차담보대출", "카드론"
        ]
        
        # 대출 상태
        self.loan_statuses = [
            "신청", "심사중", "승인", "대출실행", "상환중", "연체", "완료", "거절"
        ]
        
        # 직업 유형
        self.job_types = [
            "회사원", "자영업자", "프리랜서", "공무원", "전문직", 
            "학생", "주부", "무직", "기타"
        ]
        
        # 소득 수준
        self.income_levels = [
            "2000만원 미만", "2000-3000만원", "3000-4000만원", 
            "4000-5000만원", "5000-7000만원", "7000만원 이상"
        ]
        
        # 신용 등급
        self.credit_grades = ["A+", "A", "B+", "B", "C+", "C", "D"]

    def generate_customer_data(self, customer_id: int) -> Dict[str, Any]:
        """고객 데이터 생성"""
        first_names = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임"]
        last_names = ["민준", "서준", "도윤", "예준", "시우", "주원", "하준", "지호", "지후", "준서"]
        
        name = random.choice(first_names) + random.choice(last_names)
        age = random.randint(20, 65)
        
        return {
            "customer_id": f"CUST{customer_id:06d}",
            "name": name,
            "age": age,
            "phone": f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            "email": f"{name.lower()}{customer_id}@example.com",
            "job_type": random.choice(self.job_types),
            "income_level": random.choice(self.income_levels),
            "credit_grade": random.choice(self.credit_grades),
            "address": f"서울시 {random.choice(['강남구', '서초구', '마포구', '종로구', '중구'])} {random.randint(1, 100)}동 {random.randint(1, 1000)}호",
            "created_at": datetime.now().isoformat()
        }

    def generate_loan_data(self, loan_id: int, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """대출 데이터 생성"""
        # 대출 금액 (100만원 ~ 1억원)
        loan_amount = random.randint(1000000, 100000000)
        
        # 대출 기간 (12개월 ~ 84개월)
        loan_term = random.choice([12, 24, 36, 48, 60, 72, 84])
        
        # 이자율 (연 3% ~ 15%)
        interest_rate = round(random.uniform(3.0, 15.0), 2)
        
        # 월 상환금 계산
        monthly_rate = interest_rate / 12 / 100
        monthly_payment = int(loan_amount * (monthly_rate * (1 + monthly_rate)**loan_term) / ((1 + monthly_rate)**loan_term - 1))
        
        # 대출 신청일
        application_date = datetime.now() - timedelta(days=random.randint(1, 365))
        
        # 대출 상태에 따른 날짜 설정
        status = random.choice(self.loan_statuses)
        if status in ["신청", "심사중"]:
            approval_date = None
            disbursement_date = None
        elif status in ["승인", "대출실행", "상환중", "연체", "완료"]:
            approval_date = application_date + timedelta(days=random.randint(1, 30))
            if status in ["대출실행", "상환중", "연체", "완료"]:
                disbursement_date = approval_date + timedelta(days=random.randint(1, 7))
            else:
                disbursement_date = None
        else:  # 거절
            approval_date = application_date + timedelta(days=random.randint(1, 30))
            disbursement_date = None
        
        # 연체 정보
        overdue_days = 0
        overdue_amount = 0
        if status == "연체":
            overdue_days = random.randint(1, 90)
            overdue_amount = random.randint(0, monthly_payment)
        
        return {
            "loan_id": f"LOAN{loan_id:06d}",
            "customer_id": customer_data["customer_id"],
            "loan_type": random.choice(self.loan_types),
            "loan_amount": loan_amount,
            "loan_term": loan_term,
            "interest_rate": interest_rate,
            "monthly_payment": monthly_payment,
            "status": status,
            "application_date": application_date.isoformat(),
            "approval_date": approval_date.isoformat() if approval_date else None,
            "disbursement_date": disbursement_date.isoformat() if disbursement_date else None,
            "overdue_days": overdue_days,
            "overdue_amount": overdue_amount,
            "created_at": datetime.now().isoformat()
        }

    def generate_repayment_data(self, loan_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """상환 데이터 생성"""
        repayments = []
        
        if loan_data["status"] not in ["대출실행", "상환중", "연체", "완료"]:
            return repayments
        
        disbursement_date = datetime.fromisoformat(loan_data["disbursement_date"])
        monthly_payment = loan_data["monthly_payment"]
        
        # 상환 횟수 계산
        if loan_data["status"] == "완료":
            total_payments = loan_data["loan_term"]
        else:
            total_payments = min(
                (datetime.now() - disbursement_date).days // 30,
                loan_data["loan_term"]
            )
        
        for i in range(total_payments):
            payment_date = disbursement_date + timedelta(days=30 * (i + 1))
            
            # 연체 여부
            is_overdue = False
            if loan_data["status"] == "연체" and i >= total_payments - loan_data["overdue_days"] // 30:
                is_overdue = True
            
            repayment = {
                "payment_id": f"PAY{len(repayments) + 1:06d}",
                "loan_id": loan_data["loan_id"],
                "payment_date": payment_date.isoformat(),
                "payment_amount": monthly_payment,
                "principal_amount": int(monthly_payment * 0.7),  # 원금 70%
                "interest_amount": int(monthly_payment * 0.3),   # 이자 30%
                "is_overdue": is_overdue,
                "created_at": datetime.now().isoformat()
            }
            repayments.append(repayment)
        
        return repayments

    def create_tables(self, conn):
        """데이터베이스 테이블 생성"""
        with conn.cursor() as cursor:
            # 기존 테이블 삭제 (순서 주의)
            cursor.execute("DROP TABLE IF EXISTS repayments CASCADE")
            cursor.execute("DROP TABLE IF EXISTS loans CASCADE")
            cursor.execute("DROP TABLE IF EXISTS customers CASCADE")
            
            # 고객 테이블
            cursor.execute("""
                CREATE TABLE customers.customers (
                    id SERIAL PRIMARY KEY,
                    customer_id VARCHAR(20) UNIQUE NOT NULL,
                    name VARCHAR(50) NOT NULL,
                    age INTEGER,
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    job_type VARCHAR(20),
                    income_level VARCHAR(30),
                    credit_grade VARCHAR(5),
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 대출 테이블
            cursor.execute("""
                CREATE TABLE customers.loans (
                    id SERIAL PRIMARY KEY,
                    loan_id VARCHAR(20) UNIQUE NOT NULL,
                    customer_id VARCHAR(20) REFERENCES customers(customer_id),
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
            
            # 상환 테이블
            cursor.execute("""
                CREATE TABLE customers.repayments (
                    id SERIAL PRIMARY KEY,
                    payment_id VARCHAR(20) UNIQUE NOT NULL,
                    loan_id VARCHAR(20) REFERENCES loans(loan_id),
                    payment_date TIMESTAMP NOT NULL,
                    payment_amount INTEGER NOT NULL,
                    principal_amount INTEGER NOT NULL,
                    interest_amount INTEGER NOT NULL,
                    is_overdue BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            logger.info("데이터베이스 테이블이 생성되었습니다.")

    def insert_customer(self, conn, customer_data: Dict[str, Any]):
        """고객 데이터 삽입"""
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO customers.customers (customer_id, name, age, phone, email, job_type, 
                                     income_level, credit_grade, address, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (customer_id) DO NOTHING
            """, (
                customer_data["customer_id"], customer_data["name"], customer_data["age"],
                customer_data["phone"], customer_data["email"], customer_data["job_type"],
                customer_data["income_level"], customer_data["credit_grade"], 
                customer_data["address"], customer_data["created_at"]
            ))

    def insert_loan(self, conn, loan_data: Dict[str, Any]):
        """대출 데이터 삽입"""
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO customers.loans (loan_id, customer_id, loan_type, loan_amount, loan_term,
                                 interest_rate, monthly_payment, status, application_date,
                                 approval_date, disbursement_date, overdue_days, overdue_amount, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (loan_id) DO NOTHING
            """, (
                loan_data["loan_id"], loan_data["customer_id"], loan_data["loan_type"],
                loan_data["loan_amount"], loan_data["loan_term"], loan_data["interest_rate"],
                loan_data["monthly_payment"], loan_data["status"], loan_data["application_date"],
                loan_data["approval_date"], loan_data["disbursement_date"],
                loan_data["overdue_days"], loan_data["overdue_amount"], loan_data["created_at"]
            ))

    def insert_repayment(self, conn, repayment_data: Dict[str, Any]):
        """상환 데이터 삽입"""
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO customers.repayments (payment_id, loan_id, payment_date, payment_amount,
                                      principal_amount, interest_amount, is_overdue, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (payment_id) DO NOTHING
            """, (
                repayment_data["payment_id"], repayment_data["loan_id"],
                repayment_data["payment_date"], repayment_data["payment_amount"],
                repayment_data["principal_amount"], repayment_data["interest_amount"],
                repayment_data["is_overdue"], repayment_data["created_at"]
            ))

    def generate_and_save_data(self, num_records: int = 1000):
        """데이터 생성 및 저장"""
        conn = None
        try:
            # 데이터베이스 연결
            conn = psycopg2.connect(**self.db_config)
            conn.set_client_encoding('UTF8')
            logger.info("데이터베이스에 연결되었습니다.")
            
            # 테이블은 이미 create_schema.py에서 생성됨
            # self.create_tables(conn)
            
            # 데이터 생성 및 저장
            customers_created = 0
            loans_created = 0
            repayments_created = 0
            
            for i in range(num_records):
                # 고객 데이터 생성
                customer_data = self.generate_customer_data(i + 1)
                self.insert_customer(conn, customer_data)
                customers_created += 1
                
                # 대출 데이터 생성
                loan_data = self.generate_loan_data(i + 1, customer_data)
                self.insert_loan(conn, loan_data)
                loans_created += 1
                
                # 상환 데이터 생성
                repayment_data_list = self.generate_repayment_data(loan_data)
                for repayment_data in repayment_data_list:
                    self.insert_repayment(conn, repayment_data)
                    repayments_created += 1
                
                if (i + 1) % 100 == 0:
                    logger.info(f"진행률: {i + 1}/{num_records} ({((i + 1) / num_records * 100):.1f}%)")
                    conn.commit()
            
            conn.commit()
            logger.info(f"데이터 생성 완료!")
            logger.info(f"- 고객: {customers_created}건")
            logger.info(f"- 대출: {loans_created}건")
            logger.info(f"- 상환: {repayments_created}건")
            
        except Exception as e:
            logger.error(f"데이터 생성 중 오류 발생: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

def main():
    """메인 함수"""
    # 데이터베이스 연결 설정
    db_config = {
        "host": "localhost",
        "port": 5432,
        "database": "retention_db",
        "user": "retention_user",
        "password": "retention_password"
    }
    
    # 데이터 생성기 초기화
    generator = LoanDataGenerator(db_config)
    
    # 1000개의 대출 데이터 생성
    generator.generate_and_save_data(1000)

if __name__ == "__main__":
    main()
