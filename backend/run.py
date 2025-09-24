#!/usr/bin/env python3
"""
재대출 자동화 API 서버 실행 스크립트
"""

import uvicorn
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

if __name__ == "__main__":
    # 서버 설정
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"재대출 자동화 API 서버를 시작합니다...")
    print(f"서버 주소: http://{host}:{port}")
    print(f"API 문서: http://{host}:{port}/docs")
    print(f"ReDoc 문서: http://{host}:{port}/redoc")
    
    # 서버 실행
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
