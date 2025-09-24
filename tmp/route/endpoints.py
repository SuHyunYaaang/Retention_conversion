from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from sqlalchemy import text

from ..database import get_db
from .. import crud, schemas, models

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# ==================== 고객 관련 API ====================

@router.post("/customers/", response_model=schemas.Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """새로운 고객 정보를 생성합니다."""
    try:
        # 기존 고객 확인
        existing_customer = crud.get_customer(db, customer.customer_id)
        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 존재하는 고객 ID입니다."
            )
        
        db_customer = crud.create_customer(db, customer)
        logger.info(f"새로운 고객이 생성되었습니다: {customer.customer_id}")
        return db_customer
    except Exception as e:
        logger.error(f"고객 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="고객 생성 중 오류가 발생했습니다."
        )

@router.get("/customers/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    """고객 ID로 고객 정보를 조회합니다."""
    db_customer = crud.get_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="고객을 찾을 수 없습니다."
        )
    return db_customer

@router.get("/customers/", response_model=List[schemas.Customer])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """모든 고객 목록을 조회합니다."""
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@router.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: str, customer_update: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    """고객 정보를 업데이트합니다."""
    db_customer = crud.get_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="고객을 찾을 수 없습니다."
        )
    
    updated_customer = crud.update_customer(db, db_customer.id, customer_update)
    return updated_customer

# ==================== 대출 관련 API ====================

@router.post("/loans/", response_model=schemas.Loan, status_code=status.HTTP_201_CREATED)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    """새로운 대출 정보를 생성합니다."""
    try:
        db_loan = crud.create_loan(db, loan)
        logger.info(f"새로운 대출이 생성되었습니다: {loan.loan_number}")
        return db_loan
    except Exception as e:
        logger.error(f"대출 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="대출 생성 중 오류가 발생했습니다."
        )

@router.get("/loans/{loan_id}", response_model=schemas.Loan)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    """대출 ID로 대출 정보를 조회합니다."""
    db_loan = crud.get_loan(db, loan_id)
    if db_loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="대출을 찾을 수 없습니다."
        )
    return db_loan

@router.get("/customers/{customer_id}/loans/", response_model=List[schemas.Loan])
def get_customer_loans(customer_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """고객의 대출 목록을 조회합니다."""
    db_customer = crud.get_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="고객을 찾을 수 없습니다."
        )
    
    loans = crud.get_loans_by_customer(db, db_customer.id, skip=skip, limit=limit)
    return loans

# ==================== 재대출 신청 관련 API ====================

@router.post("/refinance-applications/", response_model=schemas.RefinanceApplication, status_code=status.HTTP_201_CREATED)
def create_refinance_application(application: schemas.RefinanceApplicationCreate, db: Session = Depends(get_db)):
    """새로운 재대출 신청을 생성합니다."""
    try:
        db_application = crud.create_refinance_application(db, application)
        logger.info(f"새로운 재대출 신청이 생성되었습니다: {db_application.application_number}")
        return db_application
    except Exception as e:
        logger.error(f"재대출 신청 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="재대출 신청 생성 중 오류가 발생했습니다."
        )

@router.get("/refinance-applications/{application_id}", response_model=schemas.RefinanceApplication)
def get_refinance_application(application_id: int, db: Session = Depends(get_db)):
    """재대출 신청 ID로 신청 정보를 조회합니다."""
    db_application = crud.get_refinance_application(db, application_id)
    if db_application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="재대출 신청을 찾을 수 없습니다."
        )
    return db_application

@router.get("/refinance-applications/number/{application_number}", response_model=schemas.RefinanceApplication)
def get_refinance_application_by_number(application_number: str, db: Session = Depends(get_db)):
    """신청 번호로 재대출 신청 정보를 조회합니다."""
    db_application = crud.get_refinance_application_by_number(db, application_number)
    if db_application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="재대출 신청을 찾을 수 없습니다."
        )
    return db_application

@router.get("/customers/{customer_id}/refinance-applications/", response_model=List[schemas.RefinanceApplication])
def get_customer_refinance_applications(customer_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """고객의 재대출 신청 목록을 조회합니다."""
    db_customer = crud.get_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="고객을 찾을 수 없습니다."
        )
    
    applications = crud.get_refinance_applications_by_customer(db, db_customer.id, skip=skip, limit=limit)
    return applications

@router.put("/refinance-applications/{application_id}", response_model=schemas.RefinanceApplication)
def update_refinance_application(application_id: int, application_update: schemas.RefinanceApplicationUpdate, db: Session = Depends(get_db)):
    """재대출 신청 정보를 업데이트합니다."""
    db_application = crud.get_refinance_application(db, application_id)
    if db_application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="재대출 신청을 찾을 수 없습니다."
        )
    
    updated_application = crud.update_refinance_application(db, application_id, application_update)
    return updated_application

@router.get("/refinance-applications/status/{status}", response_model=List[schemas.RefinanceApplication])
def get_applications_by_status(status: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """상태별로 재대출 신청 목록을 조회합니다."""
    applications = crud.get_applications_by_status(db, status, skip=skip, limit=limit)
    return applications

# ==================== 통합 재대출 신청 API ====================

@router.post("/refinance/apply/", response_model=schemas.APIResponse, status_code=status.HTTP_201_CREATED)
def apply_refinance(request: schemas.RefinanceRequest, db: Session = Depends(get_db)):
    """통합 재대출 신청을 처리합니다."""
    try:
        result = crud.process_refinance_request(db, request)
        logger.info(f"재대출 신청이 성공적으로 처리되었습니다: {result['application_number']}")
        return schemas.APIResponse(
            success=True,
            message="재대출 신청이 성공적으로 처리되었습니다.",
            data=result
        )
    except Exception as e:
        logger.error(f"재대출 신청 처리 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"재대출 신청 처리 중 오류가 발생했습니다: {str(e)}"
        )

# ==================== 재대출 상품 관련 API ====================

@router.post("/refinance-products/", response_model=schemas.RefinanceProduct, status_code=status.HTTP_201_CREATED)
def create_refinance_product(product: schemas.RefinanceProductCreate, db: Session = Depends(get_db)):
    """새로운 재대출 상품을 생성합니다."""
    try:
        db_product = crud.create_refinance_product(db, product)
        logger.info(f"새로운 재대출 상품이 생성되었습니다: {product.product_code}")
        return db_product
    except Exception as e:
        logger.error(f"재대출 상품 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="재대출 상품 생성 중 오류가 발생했습니다."
        )

@router.get("/refinance-products/", response_model=List[schemas.RefinanceProduct])
def get_active_refinance_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """활성화된 재대출 상품 목록을 조회합니다."""
    products = crud.get_active_refinance_products(db, skip=skip, limit=limit)
    return products

@router.get("/refinance-products/{product_id}", response_model=schemas.RefinanceProduct)
def get_refinance_product(product_id: int, db: Session = Depends(get_db)):
    """재대출 상품 ID로 상품 정보를 조회합니다."""
    db_product = crud.get_refinance_product(db, product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="재대출 상품을 찾을 수 없습니다."
        )
    return db_product

# ==================== 문서 관련 API ====================

@router.post("/documents/", response_model=schemas.Document, status_code=status.HTTP_201_CREATED)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    """새로운 문서 정보를 생성합니다."""
    try:
        db_document = crud.create_document(db, document)
        logger.info(f"새로운 문서가 생성되었습니다: {document.file_name}")
        return db_document
    except Exception as e:
        logger.error(f"문서 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="문서 생성 중 오류가 발생했습니다."
        )

@router.get("/refinance-applications/{application_id}/documents/", response_model=List[schemas.Document])
def get_application_documents(application_id: int, db: Session = Depends(get_db)):
    """재대출 신청의 문서 목록을 조회합니다."""
    documents = crud.get_documents_by_application(db, application_id)
    return documents

# ==================== 상태 확인 API ====================

@router.get("/health/", response_model=schemas.APIResponse)
def health_check():
    """API 서버 상태를 확인합니다."""
    return schemas.APIResponse(
        success=True,
        message="API 서버가 정상적으로 작동 중입니다.",
        data={"status": "healthy"}
    )

@router.get("/", response_model=schemas.APIResponse)
def root():
    """API 루트 엔드포인트"""
    return schemas.APIResponse(
        success=True,
        message="재대출 자동화 API 서버에 오신 것을 환영합니다.",
        data={
            "version": "1.0.0",
            "service": "Retention Refinance Automation API"
        }
    )

# ==================== 대출 데이터 조회 API ====================

@router.get("/loan-data/", response_model=dict)
def get_loan_data(page: int = 1, limit: int = 50, db: Session = Depends(get_db)):
    """대출 데이터를 페이지네이션으로 조회합니다."""
    try:
        offset = (page - 1) * limit
        
        # 고객과 대출 정보를 조인하여 조회
        query = text("""
            SELECT 
                c.customer_id,
                c.name,
                c.age,
                c.phone,
                c.email,
                c.job_type,
                c.income_level,
                c.credit_grade,
                c.address,
                l.loan_id,
                l.loan_type,
                l.loan_amount,
                l.loan_term,
                l.interest_rate,
                l.monthly_payment,
                l.status,
                l.application_date,
                l.approval_date,
                l.disbursement_date,
                l.overdue_days,
                l.overdue_amount,
                l.created_at
            FROM customers c
            LEFT JOIN loans l ON c.customer_id = l.customer_id
            ORDER BY l.created_at DESC
            LIMIT :limit OFFSET :offset
        """)
        
        result = db.execute(query, {"limit": limit, "offset": offset})
        rows = result.fetchall()
        
        # 전체 개수 조회
        count_query = text("SELECT COUNT(*) FROM customers")
        total_count = db.execute(count_query).scalar()
        
        # 데이터 포맷팅
        loan_data = []
        for row in rows:
            loan_data.append({
                "customer_id": row.customer_id,
                "name": row.name,
                "age": row.age,
                "phone": row.phone,
                "email": row.email,
                "job_type": row.job_type,
                "income_level": row.income_level,
                "credit_grade": row.credit_grade,
                "address": row.address,
                "loan_id": row.loan_id,
                "loan_type": row.loan_type,
                "loan_amount": row.loan_amount,
                "loan_term": row.loan_term,
                "interest_rate": float(row.interest_rate) if row.interest_rate else None,
                "monthly_payment": row.monthly_payment,
                "status": row.status,
                "application_date": row.application_date.isoformat() if row.application_date else None,
                "approval_date": row.approval_date.isoformat() if row.approval_date else None,
                "disbursement_date": row.disbursement_date.isoformat() if row.disbursement_date else None,
                "overdue_days": row.overdue_days,
                "overdue_amount": row.overdue_amount,
                "created_at": row.created_at.isoformat() if row.created_at else None
            })
        
        return {
            "success": True,
            "data": loan_data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "total_pages": (total_count + limit - 1) // limit
            }
        }
        
    except Exception as e:
        logger.error(f"대출 데이터 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"대출 데이터 조회 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/loan-stats/", response_model=dict)
def get_loan_stats(db: Session = Depends(get_db)):
    """대출 통계 정보를 조회합니다."""
    try:
        # 전체 고객 수
        total_customers_query = text("SELECT COUNT(*) FROM customers")
        total_customers = db.execute(total_customers_query).scalar()
        
        # 전체 대출 수
        total_loans_query = text("SELECT COUNT(*) FROM loans")
        total_loans = db.execute(total_loans_query).scalar()
        
        # 대출 상태별 통계
        status_stats_query = text("""
            SELECT status, COUNT(*) as count
            FROM loans
            GROUP BY status
        """)
        status_stats_result = db.execute(status_stats_query)
        status_stats = {row.status: row.count for row in status_stats_result}
        
        # 대출 유형별 통계
        loan_type_stats_query = text("""
            SELECT loan_type, COUNT(*) as count
            FROM loans
            GROUP BY loan_type
        """)
        loan_type_stats_result = db.execute(loan_type_stats_query)
        loan_type_stats = {row.loan_type: row.count for row in loan_type_stats_result}
        
        # 평균 대출 금액
        avg_loan_amount_query = text("SELECT AVG(loan_amount) FROM loans")
        avg_loan_amount = db.execute(avg_loan_amount_query).scalar()
        
        return {
            "success": True,
            "data": {
                "total_customers": total_customers,
                "total_loans": total_loans,
                "status_stats": status_stats,
                "loan_type_stats": loan_type_stats,
                "avg_loan_amount": float(avg_loan_amount) if avg_loan_amount else 0
            }
        }
        
    except Exception as e:
        logger.error(f"대출 통계 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"대출 통계 조회 중 오류가 발생했습니다: {str(e)}"
        )
