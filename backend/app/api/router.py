from fastapi import APIRouter
from . import main, settings

# 메인 라우터 생성
api_router = APIRouter()

# 각 도메인별 라우터를 메인 라우터에 포함
api_router.include_router(main.router)
api_router.include_router(settings.router)
