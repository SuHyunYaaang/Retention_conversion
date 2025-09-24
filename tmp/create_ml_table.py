import psycopg2
import random
from datetime import datetime, timedelta

# 데이터베이스 연결 설정
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'retention_db',
    'user': 'retention_user',
    'password': 'retention_password',
    'client_encoding': 'utf8'
}

def create_ml_table():
    conn = None
    cursor = None
    try:
        # 데이터베이스 연결
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 기존 테이블 삭제
        cursor.execute("DROP TABLE IF EXISTS ml_training_data")
        
        # ML 훈련 데이터 테이블 생성
        create_table_sql = """
        CREATE TABLE ml_training_data (
            id SERIAL PRIMARY KEY,
            customer_id VARCHAR(50),
            age INTEGER,
            income_level VARCHAR(20),
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
            everdelinquent INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_sql)
        
        # 샘플 데이터 생성 및 삽입
        income_levels = ['low', 'medium', 'high']
        credit_grades = ['A', 'B', 'C', 'D']
        loan_terms = [12, 24, 36, 48, 60]
        
        for i in range(1, 1001):  # 1000개의 샘플 데이터
            age = random.randint(25, 65)
            income_level = random.choice(income_levels)
            credit_grade = random.choice(credit_grades)
            loan_amount = random.randint(10000000, 60000000)  # 1000만원-6000만원
            interest_rate = round(random.uniform(3.0, 11.0), 2)
            loan_term = random.choice(loan_terms)
            
            # 월 상환금 계산 (간단한 공식)
            monthly_rate = interest_rate / 100 / 12
            monthly_payment = int(loan_amount * monthly_rate * (1 + monthly_rate) ** loan_term / ((1 + monthly_rate) ** loan_term - 1))
            
            payment_history_months = random.randint(6, 60)
            late_payments_3m = random.randint(0, 3)
            late_payments_6m = random.randint(0, 5)
            late_payments_12m = random.randint(0, 8)
            credit_utilization = round(random.uniform(0, 100), 2)
            debt_to_income_ratio = round(random.uniform(0, 50), 2)
            employment_length_years = random.randint(1, 20)
            number_of_accounts = random.randint(1, 10)
            inquiries_last_6m = random.randint(0, 5)
            everdelinquent = 1 if random.random() > 0.7 else 0  # 30% 확률로 연체
            
            # 랜덤 생성 날짜 (최근 1년 내)
            days_ago = random.randint(0, 365)
            created_at = datetime.now() - timedelta(days=days_ago)
            
            insert_sql = """
            INSERT INTO ml_training_data (
                customer_id, age, income_level, credit_grade, loan_amount, 
                interest_rate, loan_term, monthly_payment, payment_history_months,
                late_payments_3m, late_payments_6m, late_payments_12m,
                credit_utilization, debt_to_income_ratio, employment_length_years,
                number_of_accounts, inquiries_last_6m, everdelinquent, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_sql, (
                f'CUST{str(i).zfill(4)}', age, income_level, credit_grade, loan_amount,
                interest_rate, loan_term, monthly_payment, payment_history_months,
                late_payments_3m, late_payments_6m, late_payments_12m,
                credit_utilization, debt_to_income_ratio, employment_length_years,
                number_of_accounts, inquiries_last_6m, everdelinquent, created_at
            ))
        
        # 변경사항 커밋
        conn.commit()
        print(f"ML training data table created successfully. (1000 records)")
        
        # 데이터 확인
        cursor.execute("SELECT COUNT(*) FROM ml_training_data")
        count = cursor.fetchone()[0]
        print(f"Total {count} records inserted.")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_ml_table()
