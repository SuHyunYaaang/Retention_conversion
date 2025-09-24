from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os

from .logging import setup_logging
from .database import engine
from .models import Base
from .api.router import api_router


# 환경 : 항상 개발환경 가정
environment = os.getenv("ENVIRONMENT", "development")

# 로그
setup_logging(environment)
logger = logging.getLogger(__name__)


# 데이터베이스 테이블 생성
try:
    Base.metadata.create_all(bind=engine)
    logger.info("데이터베이스 테이블이 성공적으로 생성되었습니다.")
except Exception as e:
    logger.error(f"데이터베이스 테이블 생성 중 오류 발생: {str(e)}")

# FastAPI 설정
app = FastAPI(
    title="재대출 자동화 API",
    description="재대출 자동화 서비스를 위한 REST API",
    version="1.0.0"
)

# CORS 미들웨어 설정 : 무조건 접속 가능
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터
app.include_router(api_router, prefix="/api")

# 예외 처리
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logging.error(f"전역 예외 발생: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "예외가 발생했습니다.",
            "detail": str(exc) if os.getenv("DEBUG", "False").lower() == "true" else None
        }
    )

# Endpoint '/'
@app.get("/")
async def root():
    return {
        "message": "API Server is Running.",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    
    # 도커 가동 시 무조건 접속 가능하도록 설정
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    logging.info(f"서버를 시작합니다: {host}:{port}")
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
