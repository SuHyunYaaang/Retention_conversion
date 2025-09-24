from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import logging

from ..database import get_db
from .. import crud, schemas

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/refinance", tags=["재대출 관리"])

@router.post("/", response_model=schemas.Loan, status_code=status.HTTP_201_CREATED)
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

@router.get("/{loan_id}", response_model=schemas.Loan)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    """대출 ID로 대출 정보를 조회합니다."""
    db_loan = crud.get_loan(db, loan_id)
    if db_loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="대출을 찾을 수 없습니다."
        )
    return db_loan

@router.get("/customer/{customer_id}/", response_model=List[schemas.Loan])
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
        
        # 평균 대출 금액
        avg_loan_amount_query = text("SELECT AVG(loan_amount) FROM loans WHERE loan_amount IS NOT NULL")
        avg_loan_amount = db.execute(avg_loan_amount_query).scalar() or 0
        
        # 대출 상태별 통계
        status_stats_query = text("""
            SELECT 
                status,
                COUNT(*) as count
            FROM loans 
            GROUP BY status
        """)
        status_stats_result = db.execute(status_stats_query)
        status_stats = {}
        for row in status_stats_result:
            status_stats[row.status] = row.count
        
        # 대출 유형별 통계
        loan_type_stats_query = text("""
            SELECT 
                loan_type,
                COUNT(*) as count
            FROM loans 
            GROUP BY loan_type
        """)
        loan_type_stats_result = db.execute(loan_type_stats_query)
        loan_type_stats = {}
        for row in loan_type_stats_result:
            loan_type_stats[row.loan_type] = row.count
        
        return {
            "success": True,
            "data": {
                "total_customers": total_customers,
                "total_loans": total_loans,
                "avg_loan_amount": float(avg_loan_amount),
                "status_stats": status_stats,
                "loan_type_stats": loan_type_stats
            }
        }
        
    except Exception as e:
        logger.error(f"대출 통계 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"대출 통계 조회 중 오류가 발생했습니다: {str(e)}"
        )