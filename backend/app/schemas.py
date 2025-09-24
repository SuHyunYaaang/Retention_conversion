from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Customer 스키마
class CustomerBase(BaseModel):
    customer_id: str
    name: str
    phone: str
    email: Optional[str] = None
    birth_date: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[str] = None
    address: Optional[str] = None

class Customer(CustomerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CustomerResponse(Customer):
    pass

# Loan 스키마
class LoanBase(BaseModel):
    loan_id: str
    loan_type: str
    loan_amount: int
    loan_term: int
    interest_rate: float
    monthly_payment: int
    status: str
    application_date: Optional[datetime] = None
    approval_date: Optional[datetime] = None
    disbursement_date: Optional[datetime] = None
    overdue_days: Optional[int] = 0

class LoanCreate(LoanBase):
    customer_id: str

class LoanUpdate(BaseModel):
    loan_type: Optional[str] = None
    loan_amount: Optional[int] = None
    loan_term: Optional[int] = None
    interest_rate: Optional[float] = None
    monthly_payment: Optional[int] = None
    status: Optional[str] = None
    application_date: Optional[datetime] = None
    approval_date: Optional[datetime] = None
    disbursement_date: Optional[datetime] = None
    overdue_days: Optional[int] = None

class Loan(LoanBase):
    id: int
    customer_id: str

    class Config:
        from_attributes = True

class LoanResponse(Loan):
    pass

# RefinanceApplication 스키마
class RefinanceApplicationBase(BaseModel):
    requested_amount: float
    requested_interest_rate: Optional[float] = None

class RefinanceApplicationCreate(RefinanceApplicationBase):
    customer_id: int
    original_loan_id: int

class RefinanceApplicationUpdate(BaseModel):
    requested_amount: Optional[float] = None
    requested_interest_rate: Optional[float] = None
    application_status: Optional[str] = None
    approval_date: Optional[datetime] = None
    rejection_reason: Optional[str] = None

class RefinanceApplication(RefinanceApplicationBase):
    id: int
    application_number: str
    customer_id: int
    original_loan_id: int
    application_status: str
    application_date: datetime
    approval_date: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RefinanceApplicationResponse(RefinanceApplication):
    pass

# Document 스키마
class DocumentBase(BaseModel):
    document_type: str
    file_name: str
    file_path: str
    file_size: Optional[int] = None

class DocumentCreate(DocumentBase):
    application_id: int

class Document(DocumentBase):
    id: int
    application_id: int
    upload_date: datetime

    class Config:
        from_attributes = True

# RefinanceProduct 스키마
class RefinanceProductBase(BaseModel):
    product_name: str
    product_code: str
    min_interest_rate: float
    max_interest_rate: float
    min_loan_amount: float
    max_loan_amount: float
    loan_term_min: int
    loan_term_max: int
    eligibility_criteria: Optional[str] = None

class RefinanceProductCreate(RefinanceProductBase):
    pass

class RefinanceProductUpdate(BaseModel):
    product_name: Optional[str] = None
    min_interest_rate: Optional[float] = None
    max_interest_rate: Optional[float] = None
    min_loan_amount: Optional[float] = None
    max_loan_amount: Optional[float] = None
    loan_term_min: Optional[int] = None
    loan_term_max: Optional[int] = None
    eligibility_criteria: Optional[str] = None
    is_active: Optional[bool] = None

class RefinanceProduct(RefinanceProductBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# API 응답 스키마
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

# 재대출 신청 요청 스키마
class RefinanceRequest(BaseModel):
    customer_info: CustomerCreate
    loan_info: LoanCreate
    refinance_info: RefinanceApplicationBase
    documents: Optional[List[DocumentBase]] = None

# 재대출 상품 추천 요청 스키마
class ProductRecommendationRequest(BaseModel):
    customer_id: str
    current_loan_amount: float
    current_interest_rate: float
    desired_amount: Optional[float] = None
    credit_score: Optional[int] = None

# Settings 스키마
class SettingsBase(BaseModel):
    setting_key: str
    setting_value: Optional[str] = None
    description: Optional[str] = None

class SettingsCreate(SettingsBase):
    pass

class SettingsUpdate(BaseModel):
    setting_value: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class SettingsResponse(SettingsBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Retention 스키마
class RetentionBase(BaseModel):
    customer_id: int
    retention_type: str
    status: Optional[str] = "active"
    end_date: Optional[datetime] = None

class RetentionCreate(RetentionBase):
    pass

class RetentionUpdate(BaseModel):
    retention_type: Optional[str] = None
    status: Optional[str] = None
    end_date: Optional[datetime] = None

class RetentionResponse(RetentionBase):
    id: int
    start_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
