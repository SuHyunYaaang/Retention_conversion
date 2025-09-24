import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# 데이터베이스 URL 설정
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://retention_user:retention_password@postgres:5432/retention_db"
)

# 데이터베이스 URL 설정
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL이 안들어왔엉요")

# 비동기 asynccpg 드라이버 사용
#if DATABASE_URL.startswith("postgresql://"):
#    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# engine : sqlalchemy CREATE Engine (비동기)
engine = create_engine(
    DATABASE_URL
)

# ORM 모델 상속 - SQLAlchemy 2.0 호환
Base = declarative_base()

# Async 세션 팩토리 생성
SessionLocal = sessionmaker(
    bind=engine, 
    autoflush=False, 
    expire_on_commit=False
)

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



