-- 재대출 자동화 데이터베이스 초기화 스크립트

-- 고객 정보 테이블
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    birth_date VARCHAR(10),
    address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 대출 정보 테이블
CREATE TABLE IF NOT EXISTS loans (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
    loan_number VARCHAR(50) UNIQUE NOT NULL,
    loan_type VARCHAR(50) NOT NULL,
    loan_amount DECIMAL(15,2) NOT NULL,
    interest_rate DECIMAL(5,2) NOT NULL,
    remaining_amount DECIMAL(15,2) NOT NULL,
    monthly_payment DECIMAL(15,2) NOT NULL,
    loan_start_date TIMESTAMP WITH TIME ZONE,
    loan_end_date TIMESTAMP WITH TIME ZONE,
    bank_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 재대출 신청 테이블
CREATE TABLE IF NOT EXISTS refinance_applications (
    id SERIAL PRIMARY KEY,
    application_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
    original_loan_id INTEGER REFERENCES loans(id) ON DELETE CASCADE,
    requested_amount DECIMAL(15,2) NOT NULL,
    requested_interest_rate DECIMAL(5,2),
    application_status VARCHAR(20) DEFAULT 'pending',
    application_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    approval_date TIMESTAMP WITH TIME ZONE,
    rejection_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 문서 정보 테이블
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES refinance_applications(id) ON DELETE CASCADE,
    document_type VARCHAR(50) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
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
    application_id INTEGER REFERENCES refinance_applications(id) ON DELETE CASCADE,
    action VARCHAR(50) NOT NULL,
    description TEXT,
    performed_by VARCHAR(100),
    performed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_customers_customer_id ON customers(customer_id);
CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone);
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_loans_customer_id ON loans(customer_id);
CREATE INDEX IF NOT EXISTS idx_loans_loan_number ON loans(loan_number);
CREATE INDEX IF NOT EXISTS idx_applications_customer_id ON refinance_applications(customer_id);
CREATE INDEX IF NOT EXISTS idx_applications_number ON refinance_applications(application_number);
CREATE INDEX IF NOT EXISTS idx_applications_status ON refinance_applications(application_status);
CREATE INDEX IF NOT EXISTS idx_documents_application_id ON documents(application_id);
CREATE INDEX IF NOT EXISTS idx_products_code ON refinance_products(product_code);
CREATE INDEX IF NOT EXISTS idx_logs_application_id ON application_logs(application_id);

-- 업데이트 트리거 함수
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 업데이트 트리거 생성
CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_loans_updated_at BEFORE UPDATE ON loans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_applications_updated_at BEFORE UPDATE ON refinance_applications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON refinance_products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 샘플 데이터 삽입
INSERT INTO customers (customer_id, name, phone, email, birth_date, address) VALUES
('CUST001', '홍길동', '01012345678', 'hong@example.com', '1990-01-01', '서울시 강남구'),
('CUST002', '김철수', '01023456789', 'kim@example.com', '1985-05-15', '서울시 서초구'),
('CUST003', '이영희', '01034567890', 'lee@example.com', '1992-08-20', '서울시 마포구')
ON CONFLICT (customer_id) DO NOTHING;

INSERT INTO loans (customer_id, loan_number, loan_type, loan_amount, interest_rate, remaining_amount, monthly_payment, bank_name) VALUES
(1, 'LOAN001', '주택담보대출', 50000000, 3.5, 45000000, 250000, '신한은행'),
(2, 'LOAN002', '신용대출', 30000000, 5.0, 25000000, 180000, '국민은행'),
(3, 'LOAN003', '전세자금대출', 20000000, 4.2, 18000000, 120000, '우리은행')
ON CONFLICT (loan_number) DO NOTHING;

INSERT INTO refinance_products (product_name, product_code, min_interest_rate, max_interest_rate, min_loan_amount, max_loan_amount, loan_term_min, loan_term_max, eligibility_criteria) VALUES
('우리집 재대출', 'REF001', 2.8, 4.5, 10000000, 100000000, 12, 360, '신용등급 3등급 이상'),
('스마트 재대출', 'REF002', 3.2, 5.0, 5000000, 50000000, 6, 240, '소득증빙서류 필수'),
('프리미엄 재대출', 'REF003', 2.5, 4.0, 20000000, 200000000, 24, 480, '고소득자 전용')
ON CONFLICT (product_code) DO NOTHING;
