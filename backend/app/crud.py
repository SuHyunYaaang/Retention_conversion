from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
import uuid
from datetime import datetime

from . import models, schemas

# Customer CRUD
def create_customer(db: Session, customer: schemas.CustomerCreate) -> models.Customer:
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customer(db: Session, customer_id: str) -> Optional[models.Customer]:
    return db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()

def get_customer_by_id(db: Session, customer_id: int) -> Optional[models.Customer]:
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Customer]:
    return db.query(models.Customer).offset(skip).limit(limit).all()

def update_customer(db: Session, customer_id: int, customer_update: schemas.CustomerUpdate) -> Optional[models.Customer]:
    db_customer = get_customer_by_id(db, customer_id)
    if db_customer:
        update_data = customer_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

# Loan CRUD
def create_loan(db: Session, loan: schemas.LoanCreate) -> models.Loan:
    db_loan = models.Loan(**loan.dict())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def get_loan(db: Session, loan_id: int) -> Optional[models.Loan]:
    return db.query(models.Loan).filter(models.Loan.id == loan_id).first()

def get_loans_by_customer(db: Session, customer_id: int, skip: int = 0, limit: int = 100) -> List[models.Loan]:
    return db.query(models.Loan).filter(models.Loan.customer_id == customer_id).offset(skip).limit(limit).all()

def get_active_loans_by_customer(db: Session, customer_id: int) -> List[models.Loan]:
    return db.query(models.Loan).filter(
        and_(models.Loan.customer_id == customer_id, models.Loan.is_active == True)
    ).all()

def update_loan(db: Session, loan_id: int, loan_update: schemas.LoanUpdate) -> Optional[models.Loan]:
    db_loan = get_loan(db, loan_id)
    if db_loan:
        update_data = loan_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_loan, field, value)
        db.commit()
        db.refresh(db_loan)
    return db_loan

# RefinanceApplication CRUD
def create_refinance_application(db: Session, application: schemas.RefinanceApplicationCreate) -> models.RefinanceApplication:
    # 고유한 신청 번호 생성
    application_number = f"REF-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    
    db_application = models.RefinanceApplication(
        application_number=application_number,
        **application.dict()
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_refinance_application(db: Session, application_id: int) -> Optional[models.RefinanceApplication]:
    return db.query(models.RefinanceApplication).filter(models.RefinanceApplication.id == application_id).first()

def get_refinance_application_by_number(db: Session, application_number: str) -> Optional[models.RefinanceApplication]:
    return db.query(models.RefinanceApplication).filter(
        models.RefinanceApplication.application_number == application_number
    ).first()

def get_refinance_applications_by_customer(db: Session, customer_id: int, skip: int = 0, limit: int = 100) -> List[models.RefinanceApplication]:
    return db.query(models.RefinanceApplication).filter(
        models.RefinanceApplication.customer_id == customer_id
    ).offset(skip).limit(limit).all()

def update_refinance_application(db: Session, application_id: int, application_update: schemas.RefinanceApplicationUpdate) -> Optional[models.RefinanceApplication]:
    db_application = get_refinance_application(db, application_id)
    if db_application:
        update_data = application_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_application, field, value)
        db.commit()
        db.refresh(db_application)
    return db_application

def get_applications_by_status(db: Session, status: str, skip: int = 0, limit: int = 100) -> List[models.RefinanceApplication]:
    return db.query(models.RefinanceApplication).filter(
        models.RefinanceApplication.application_status == status
    ).offset(skip).limit(limit).all()

# Document CRUD
def create_document(db: Session, document: schemas.DocumentCreate) -> models.Document:
    db_document = models.Document(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_documents_by_application(db: Session, application_id: int) -> List[models.Document]:
    return db.query(models.Document).filter(models.Document.application_id == application_id).all()

def get_document(db: Session, document_id: int) -> Optional[models.Document]:
    return db.query(models.Document).filter(models.Document.id == document_id).first()

# RefinanceProduct CRUD
def create_refinance_product(db: Session, product: schemas.RefinanceProductCreate) -> models.RefinanceProduct:
    db_product = models.RefinanceProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_refinance_product(db: Session, product_id: int) -> Optional[models.RefinanceProduct]:
    return db.query(models.RefinanceProduct).filter(models.RefinanceProduct.id == product_id).first()

def get_active_refinance_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.RefinanceProduct]:
    return db.query(models.RefinanceProduct).filter(
        models.RefinanceProduct.is_active == True
    ).offset(skip).limit(limit).all()

def update_refinance_product(db: Session, product_id: int, product_update: schemas.RefinanceProductUpdate) -> Optional[models.RefinanceProduct]:
    db_product = get_refinance_product(db, product_id)
    if db_product:
        update_data = product_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
    return db_product

# ApplicationLog CRUD
def create_application_log(db: Session, application_id: int, action: str, description: str = None, performed_by: str = None) -> models.ApplicationLog:
    db_log = models.ApplicationLog(
        application_id=application_id,
        action=action,
        description=description,
        performed_by=performed_by
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_application_logs(db: Session, application_id: int) -> List[models.ApplicationLog]:
    return db.query(models.ApplicationLog).filter(
        models.ApplicationLog.application_id == application_id
    ).order_by(models.ApplicationLog.performed_at.desc()).all()

# 통합 재대출 신청 처리
def process_refinance_request(db: Session, request: schemas.RefinanceRequest) -> dict:
    try:
        # 1. 고객 정보 저장 또는 업데이트
        existing_customer = get_customer(db, request.customer_info.customer_id)
        if existing_customer:
            customer = existing_customer
        else:
            customer = create_customer(db, request.customer_info)
        
        # 2. 대출 정보 저장
        loan_data = request.loan_info.dict()
        loan_data['customer_id'] = customer.id
        loan = create_loan(db, schemas.LoanCreate(**loan_data))
        
        # 3. 재대출 신청 생성
        application_data = request.refinance_info.dict()
        application_data['customer_id'] = customer.id
        application_data['original_loan_id'] = loan.id
        application = create_refinance_application(db, schemas.RefinanceApplicationCreate(**application_data))
        
        # 4. 문서 정보 저장 (있는 경우)
        documents = []
        if request.documents:
            for doc in request.documents:
                doc_data = doc.dict()
                doc_data['application_id'] = application.id
                document = create_document(db, schemas.DocumentCreate(**doc_data))
                documents.append(document)
        
        # 5. 로그 생성
        create_application_log(
            db, 
            application.id, 
            "created", 
            f"재대출 신청이 생성되었습니다. 신청번호: {application.application_number}",
            "system"
        )
        
        return {
            "success": True,
            "application_number": application.application_number,
            "customer_id": customer.customer_id,
            "application_id": application.id
        }
        
    except Exception as e:
        db.rollback()
        raise e
