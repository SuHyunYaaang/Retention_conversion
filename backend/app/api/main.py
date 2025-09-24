from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any
from ..database import get_db
from ..models import Customer, Loan, RefinanceApplication, RefinanceProduct
from ..schemas import CustomerCreate, CustomerResponse, LoanCreate, LoanResponse, RefinanceApplicationCreate, RefinanceApplicationResponse

router = APIRouter(tags=["main"])

@router.get("/")
def get_main_info():
    """메인 페이지 정보"""
    return {
        "message": "재대출 자동화 서비스 API",
        "version": "1.0.0",
        "status": "running"
    }

@router.get("/dashboard")
def get_dashboard_data(db: Session = Depends(get_db)):
    """대시보드 데이터 조회"""
    try:
        # 고객 수
        customer_count = db.query(Customer).count()
        
        # 대출 수
        loan_count = db.query(Loan).count()
        
        # 재대출 신청 수
        refinance_count = db.query(RefinanceApplication).count()
        
        # 상품 수
        product_count = db.query(RefinanceProduct).filter(RefinanceProduct.is_active == True).count()
        
        return {
            "customer_count": customer_count,
            "loan_count": loan_count,
            "refinance_count": refinance_count,
            "product_count": product_count,
            "total_assets": loan_count * 50000000  # 예시 데이터
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"대시보드 데이터 조회 실패: {str(e)}")

@router.get("/customers", response_model=List[CustomerResponse])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """고객 목록 조회"""
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers

@router.post("/customers", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """새 고객 생성"""
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/loans", response_model=List[LoanResponse])
def get_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """대출 목록 조회"""
    loans = db.query(Loan).offset(skip).limit(limit).all()
    return loans

@router.post("/loans", response_model=LoanResponse)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    """새 대출 생성"""
    db_loan = Loan(**loan.dict())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

@router.get("/refinance-applications", response_model=List[RefinanceApplicationResponse])
def get_refinance_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """재대출 신청 목록 조회"""
    applications = db.query(RefinanceApplication).offset(skip).limit(limit).all()
    return applications

@router.post("/refinance-applications", response_model=RefinanceApplicationResponse)
def create_refinance_application(application: RefinanceApplicationCreate, db: Session = Depends(get_db)):
    """새 재대출 신청 생성"""
    db_application = RefinanceApplication(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    """재대출 상품 목록 조회"""
    products = db.query(RefinanceProduct).filter(RefinanceProduct.is_active == True).all()
    return products

@router.get("/recommendations/{customer_id}")
def get_recommendations(customer_id: int, db: Session = Depends(get_db)):
    """고객별 상품 추천"""
    try:
        # 고객 정보 조회
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # 고객의 대출 정보 조회
        loans = db.query(Loan).filter(Loan.customer_id == customer_id).all()
        
        # 추천 상품 조회 (예시 로직)
        products = db.query(RefinanceProduct).filter(RefinanceProduct.is_active == True).limit(3).all()
        
        return {
            "customer": customer,
            "current_loans": loans,
            "recommended_products": products,
            "recommendation_reason": "현재 대출 조건 대비 유리한 금리 상품"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"추천 데이터 조회 실패: {str(e)}")

@router.get("/ml_dashboard")
def get_ml_predictions(db: Session = Depends(get_db)):
    """ML 예측 데이터 조회 (customers 스키마 기반)"""
    try:
        # customers 스키마의 데이터를 조합하여 ML 예측 데이터 형태로 변환
        query = text("""
            SELECT 
                c.id,
                c.customer_id,
                c.age,
                c.income_level,
                c.credit_grade,
                l.loan_amount,
                l.interest_rate,
                l.loan_term,
                l.monthly_payment,
                COALESCE(EXTRACT(MONTH FROM AGE(NOW(), l.application_date)), 0) as payment_history_months,
                COALESCE(
                    (SELECT COUNT(*) FROM customers.repayments r 
                     WHERE r.loan_id = l.loan_id 
                     AND r.is_overdue = true 
                     AND r.payment_date >= NOW() - INTERVAL '3 months'), 0
                ) as late_payments_3m,
                COALESCE(
                    (SELECT COUNT(*) FROM customers.repayments r 
                     WHERE r.loan_id = l.loan_id 
                     AND r.is_overdue = true 
                     AND r.payment_date >= NOW() - INTERVAL '6 months'), 0
                ) as late_payments_6m,
                COALESCE(
                    (SELECT COUNT(*) FROM customers.repayments r 
                     WHERE r.loan_id = l.loan_id 
                     AND r.is_overdue = true 
                     AND r.payment_date >= NOW() - INTERVAL '12 months'), 0
                ) as late_payments_12m,
                CASE 
                    WHEN l.loan_amount > 0 THEN (l.monthly_payment * l.loan_term) / l.loan_amount
                    ELSE 0 
                END as credit_utilization,
                CASE 
                    WHEN c.income_level = '2000만원 미만' THEN 0.3
                    WHEN c.income_level = '2000-3000만원' THEN 0.4
                    WHEN c.income_level = '3000-4000만원' THEN 0.5
                    WHEN c.income_level = '4000-5000만원' THEN 0.6
                    WHEN c.income_level = '5000-7000만원' THEN 0.7
                    WHEN c.income_level = '7000만원 이상' THEN 0.8
                    ELSE 0.5
                END as debt_to_income_ratio,
                FLOOR(RANDOM() * 20 + 1) as employment_length_years,
                FLOOR(RANDOM() * 10 + 1) as number_of_accounts,
                FLOOR(RANDOM() * 5) as inquiries_last_6m,
                CASE 
                    WHEN l.status = '연체' THEN 1
                    WHEN l.overdue_days > 0 THEN 1
                    ELSE 0
                END as everdelinquent,
                c.created_at
            FROM customers.customers c
            LEFT JOIN customers.loans l ON c.customer_id = l.customer_id
            ORDER BY c.id
            LIMIT 1000
        """)
        
        result = db.execute(query)
        data = []
        
        for row in result:
            data.append({
                "id": row.id,
                "customer_id": row.customer_id,
                "age": row.age or 30,
                "income_level": row.income_level or "3000-4000만원",
                "credit_grade": row.credit_grade or "B",
                "loan_amount": row.loan_amount or 0,
                "interest_rate": float(row.interest_rate) if row.interest_rate else 0,
                "loan_term": row.loan_term or 0,
                "monthly_payment": row.monthly_payment or 0,
                "payment_history_months": int(row.payment_history_months) if row.payment_history_months else 0,
                "late_payments_3m": int(row.late_payments_3m) if row.late_payments_3m else 0,
                "late_payments_6m": int(row.late_payments_6m) if row.late_payments_6m else 0,
                "late_payments_12m": int(row.late_payments_12m) if row.late_payments_12m else 0,
                "credit_utilization": float(row.credit_utilization) if row.credit_utilization else 0,
                "debt_to_income_ratio": float(row.debt_to_income_ratio) if row.debt_to_income_ratio else 0,
                "employment_length_years": int(row.employment_length_years) if row.employment_length_years else 0,
                "number_of_accounts": int(row.number_of_accounts) if row.number_of_accounts else 0,
                "inquiries_last_6m": int(row.inquiries_last_6m) if row.inquiries_last_6m else 0,
                "everdelinquent": int(row.everdelinquent) if row.everdelinquent else 0,
                "created_at": str(row.created_at) if row.created_at else ""
            })
        
        return data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ML 예측 데이터 조회 실패: {str(e)}")
