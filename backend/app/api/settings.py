from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Settings
from ..schemas import SettingsCreate, SettingsResponse

router = APIRouter(prefix="/settings", tags=["settings"])

@router.get("/", response_model=List[SettingsResponse])
def get_settings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """설정 목록 조회"""
    settings = db.query(Settings).offset(skip).limit(limit).all()
    return settings

@router.get("/{setting_id}", response_model=SettingsResponse)
def get_setting(setting_id: int, db: Session = Depends(get_db)):
    """특정 설정 조회"""
    setting = db.query(Settings).filter(Settings.id == setting_id).first()
    if setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting

@router.post("/", response_model=SettingsResponse)
def create_setting(setting: SettingsCreate, db: Session = Depends(get_db)):
    """새 설정 생성"""
    db_setting = Settings(**setting.dict())
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting
