from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Customer(Base):
    """고객 정보 테이블"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100))
    age = Column(Integer)
    job_type = Column(String(20))
    income_level = Column(String(30))
    credit_grade = Column(String(5))
    address = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계 설정
    pass

class Loan(Base):
    """기존 대출 정보 테이블"""
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(String(20), unique=True, nullable=False)
    customer_id = Column(String(20), nullable=False)
    loan_type = Column(String(30), nullable=False)  # 주택담보대출, 신용대출 등
    loan_amount = Column(Integer, nullable=False)
    loan_term = Column(Integer, nullable=False)
    interest_rate = Column(Float, nullable=False)
    monthly_payment = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    application_date = Column(DateTime)
    approval_date = Column(DateTime)
    disbursement_date = Column(DateTime)
    overdue_days = Column(Integer, default=0)
    
    # 관계 설정
    pass

class RefinanceApplication(Base):
    """재대출 신청 정보 테이블"""
    __tablename__ = "refinance_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    application_number = Column(String(50), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    original_loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    requested_amount = Column(Float, nullable=False)
    requested_interest_rate = Column(Float)
    application_status = Column(String(20), default="pending")  # pending, approved, rejected, processing
    application_date = Column(DateTime(timezone=True), server_default=func.now())
    approval_date = Column(DateTime(timezone=True))
    rejection_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 관계 설정
    pass

class Document(Base):
    """문서 정보 테이블"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("refinance_applications.id"), nullable=False)
    document_type = Column(String(50), nullable=False)  # income_proof, identity_doc, etc.
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계 설정
    pass

class RefinanceProduct(Base):
    """재대출 상품 정보 테이블"""
    __tablename__ = "refinance_products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    product_code = Column(String(50), unique=True, nullable=False)
    min_interest_rate = Column(Float, nullable=False)
    max_interest_rate = Column(Float, nullable=False)
    min_loan_amount = Column(Float, nullable=False)
    max_loan_amount = Column(Float, nullable=False)
    loan_term_min = Column(Integer, nullable=False)  # 개월 단위
    loan_term_max = Column(Integer, nullable=False)  # 개월 단위
    eligibility_criteria = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ApplicationLog(Base):
    """신청 로그 테이블"""
    __tablename__ = "application_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("refinance_applications.id"), nullable=False)
    action = Column(String(50), nullable=False)  # created, updated, status_changed, etc.
    description = Column(Text)
    performed_by = Column(String(100))
    performed_at = Column(DateTime(timezone=True), server_default=func.now())

class Settings(Base):
    """시스템 설정 테이블"""
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String(100), unique=True, nullable=False)
    setting_value = Column(Text)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Retention(Base):
    """재고정 정보 테이블"""
    __tablename__ = "retentions"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    retention_type = Column(String(50), nullable=False)  # rate_lock, product_change, etc.
    status = Column(String(20), default="active")  # active, expired, cancelled
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
