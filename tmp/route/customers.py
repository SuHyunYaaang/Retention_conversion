from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from ..database import get_db
from .. import crud, schemas

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/customers", tags=["고객 관리"])

@router.post("/", response_model=schemas.Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """새로운 고객 정보를 생성합니다."""
    try:
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

@router.get("/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    """고객 ID로 고객 정보를 조회합니다."""
    db_customer = crud.get_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="고객을 찾을 수 없습니다."
        )
    return db_customer

@router.get("/", response_model=List[schemas.Customer])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """모든 고객 목록을 조회합니다."""
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@router.put("/{customer_id}", response_model=schemas.Customer)
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