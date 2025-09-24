from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from ..database import get_db
from .. import crud, schemas

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/refinance", tags=["대환 관리"])


@router.post("/refinance-applications/", response_model=schemas.RefinanceApplication, status_code=status.HTTP_201_CREATED)
def create_refinance_application(application: schemas.RefinanceApplicationCreate, db: Session = Depends(get_db)):
    """새로운 대환 신청을 생성합니다."""
    try:
        db_application = crud.create_refinance_application(db, application)
        logger.info(f"새로운 대환 신청이 생성되었습니다: {db_application.application_number}")
        return db_application
    except Exception as e:
        logger.error(f"대환 신청 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="대환 신청 생성 중 오류가 발생했습니다."
        )

@router.get("/refinance-applications/{application_id}", response_model=schemas.RefinanceApplication)
def get_refinance_application(application_id: int, db: Session = Depends(get_db)):
    """대환 신청 ID로 신청 정보를 조회합니다."""
    db_application = crud.get_refinance_application(db, application_id)
    if db_application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="대환 신청을 찾을 수 없습니다."
        )
    return db_application

@router.get("/refinance-applications/number/{application_number}", response_model=schemas.RefinanceApplication)
def get_refinance_application_by_number(application_number: str, db: Session = Depends(get_db)):
    """신청 번호로 대환 신청 정보를 조회합니다."""
    db_application = crud.get_refinance_application_by_number(db, application_number)
    if db_application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="대환 신청을 찾을 수 없습니다."
        )
    return db_application

@router.get("/customers/{customer_id}/refinance-applications/", response_model=List[schemas.RefinanceApplication])
def get_customer_refinance_applications(customer_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """고객의 대환 신청 목록을 조회합니다."""
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
    """대환 신청 정보를 업데이트합니다."""
    db_application = crud.get_refinance_application(db, application_id)
    if db_application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="대환 신청을 찾을 수 없습니다."
        )
    
    updated_application = crud.update_refinance_application(db, application_id, application_update)
    return updated_application

@router.get("/refinance-applications/status/{status}", response_model=List[schemas.RefinanceApplication])
def get_applications_by_status(status: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """상태별로 대환 신청 목록을 조회합니다."""
    applications = crud.get_applications_by_status(db, status, skip=skip, limit=limit)
    return applications

# ==================== 통합 대환 신청 API ====================

@router.post("/refinance/apply/", response_model=schemas.APIResponse, status_code=status.HTTP_201_CREATED)
def apply_refinance(request: schemas.RefinanceRequest, db: Session = Depends(get_db)):
    """통합 대환 신청을 처리합니다."""
    try:
        result = crud.process_refinance_request(db, request)
        logger.info(f"대환 신청이 성공적으로 처리되었습니다: {result['application_number']}")
        return schemas.APIResponse(
            success=True,
            message="대환 신청이 성공적으로 처리되었습니다.",
            data=result
        )
    except Exception as e:
        logger.error(f"대환 신청 처리 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"대환 신청 처리 중 오류가 발생했습니다: {str(e)}"
        )

# ==================== 대환 상품 관련 API ====================

@router.post("/refinance-products/", response_model=schemas.RefinanceProduct, status_code=status.HTTP_201_CREATED)
def create_refinance_product(product: schemas.RefinanceProductCreate, db: Session = Depends(get_db)):
    """새로운 대환 상품을 생성합니다."""
    try:
        db_product = crud.create_refinance_product(db, product)
        logger.info(f"새로운 대환 상품이 생성되었습니다: {product.product_code}")
        return db_product
    except Exception as e:
        logger.error(f"대환 상품 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="대환 상품 생성 중 오류가 발생했습니다."
        )

@router.get("/refinance-products/", response_model=List[schemas.RefinanceProduct])
def get_active_refinance_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """활성화된 대환 상품 목록을 조회합니다."""
    products = crud.get_active_refinance_products(db, skip=skip, limit=limit)
    return products

@router.get("/refinance-products/{product_id}", response_model=schemas.RefinanceProduct)
def get_refinance_product(product_id: int, db: Session = Depends(get_db)):
    """대환 상품 ID로 상품 정보를 조회합니다."""
    db_product = crud.get_refinance_product(db, product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="대환 상품을 찾을 수 없습니다."
        )
    return db_product