-- 재대출 자동화 서비스 데이터베이스 초기화 스크립트

-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS retention_db;

-- 사용자 생성 및 권한 부여
CREATE USER IF NOT EXISTS retention_user WITH PASSWORD 'retention_password';
GRANT ALL PRIVILEGES ON DATABASE retention_db TO retention_user;

-- 데이터베이스 연결
\c retention_db;

-- 스키마 생성
CREATE SCHEMA IF NOT EXISTS customers;

-- 고객 테이블
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    age INTEGER,
    job_type VARCHAR(20),
    income_level VARCHAR(30),
    credit_grade VARCHAR(5),
    address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 대출 테이블
CREATE TABLE IF NOT EXISTS loans (
    id SERIAL PRIMARY KEY,
    loan_id VARCHAR(20) UNIQUE NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 재대출 신청 테이블
CREATE TABLE IF NOT EXISTS refinance_applications (
    id SERIAL PRIMARY KEY,
    application_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id INTEGER NOT NULL,
    original_loan_id INTEGER NOT NULL,
    requested_amount DECIMAL(15,2) NOT NULL,
    requested_interest_rate DECIMAL(5,2),
    application_status VARCHAR(20) DEFAULT 'pending',
    application_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    approval_date TIMESTAMP WITH TIME ZONE,
    rejection_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (original_loan_id) REFERENCES loans(id)
);

-- 문서 테이블
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    application_id INTEGER NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES refinance_applications(id)
);

-- 재대출 상품 테이블
CREATE TABLE IF NOT EXISTS refinance_products (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    product_code VARCHAR(50) UNIQUE NOT NULL,
    min_interest_rate DECIMAL(5,2) NOT NULL,
    max_interest_rate DECIMAL(5,2) NOT NULL,
    min_loan_amount DECIMAL(15,2) NOT NULL,
    max_loan_amount DECIMAL(15,2) NOT NULL,
    loan_term_min INTEGER NOT NULL,
    loan_term_max INTEGER NOT NULL,
    eligibility_criteria TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 신청 로그 테이블
CREATE TABLE IF NOT EXISTS application_logs (
    id SERIAL PRIMARY KEY,
    application_id INTEGER NOT NULL,
    action VARCHAR(50) NOT NULL,
    description TEXT,
    performed_by VARCHAR(100),
    performed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES refinance_applications(id)
);

-- 시스템 설정 테이블
CREATE TABLE IF NOT EXISTS settings (
    id SERIAL PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 재고정 테이블
CREATE TABLE IF NOT EXISTS retentions (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    retention_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    start_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_customers_customer_id ON customers(customer_id);
CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone);
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_credit_grade ON customers(credit_grade);

CREATE INDEX IF NOT EXISTS idx_loans_loan_id ON loans(loan_id);
CREATE INDEX IF NOT EXISTS idx_loans_customer_id ON loans(customer_id);
CREATE INDEX IF NOT EXISTS idx_loans_status ON loans(status);

CREATE INDEX IF NOT EXISTS idx_refinance_applications_application_number ON refinance_applications(application_number);
CREATE INDEX IF NOT EXISTS idx_refinance_applications_customer_id ON refinance_applications(customer_id);
CREATE INDEX IF NOT EXISTS idx_refinance_applications_status ON refinance_applications(application_status);

CREATE INDEX IF NOT EXISTS idx_documents_application_id ON documents(application_id);
CREATE INDEX IF NOT EXISTS idx_refinance_products_product_code ON refinance_products(product_code);
CREATE INDEX IF NOT EXISTS idx_refinance_products_is_active ON refinance_products(is_active);

-- 샘플 데이터 삽입
INSERT INTO refinance_products (product_name, product_code, min_interest_rate, max_interest_rate, min_loan_amount, max_loan_amount, loan_term_min, loan_term_max, eligibility_criteria) VALUES
('우리집 대출', 'PROD001', 2.5, 4.5, 10000000, 100000000, 12, 60, '신용등급 A 이상, 소득증빙서류 필수'),
('행복한 대출', 'PROD002', 3.0, 5.0, 5000000, 50000000, 12, 36, '신용등급 B 이상, 직장인 한정'),
('스마트 대출', 'PROD003', 2.8, 4.8, 10000000, 80000000, 12, 48, '신용등급 A 이상, 자산증빙서류 필수'),
('프리미엄 대출', 'PROD004', 2.2, 4.2, 20000000, 200000000, 12, 60, '신용등급 A 이상, 고소득자 한정'),
('기본 대출', 'PROD005', 3.5, 5.5, 3000000, 30000000, 12, 24, '신용등급 C 이상, 기본 서류만 필요')
ON CONFLICT (product_code) DO NOTHING;

-- 시스템 설정 초기화
INSERT INTO settings (setting_key, setting_value, description) VALUES
('max_loan_amount', '100000000', '최대 대출 한도'),
('min_credit_grade', 'C', '최소 신용등급'),
('default_interest_rate', '4.5', '기본 금리'),
('application_timeout_days', '30', '신청 만료일'),
('auto_approval_threshold', '0.8', '자동 승인 임계값')
ON CONFLICT (setting_key) DO NOTHING;

-- 권한 설정
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO retention_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO retention_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO retention_user;

-- 완료 메시지
SELECT 'Database initialization completed successfully!' as message;

