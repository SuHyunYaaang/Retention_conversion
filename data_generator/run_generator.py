#!/usr/bin/env python3
"""
대출 데이터 생성기 실행 스크립트
"""

import sys
import os
from loan_data_generator import LoanDataGenerator
from create_schema import create_customers_schema

def main():
    """메인 실행 함수"""
    print("=" * 50)
    print("대출 금융 데이터 생성기")
    print("=" * 50)
    
    # 데이터베이스 연결 설정 (Docker 환경)
    db_config = {
        "host": "postgres",  # Docker 서비스명
        "port": 5432,
        "database": "retention_db",
        "user": "retention_user",
        "password": "retention_password"
    }
    
    try:
        # 기본값으로 1000개 데이터 생성
        num_records = 1000
        
        print(f"\n{num_records}개의 대출 데이터를 생성합니다...")
        print("데이터베이스 연결 중...")
        
        # customers 스키마 생성
        print("customers 스키마 및 테이블 생성 중...")
        create_customers_schema()
        
        # 데이터 생성기 초기화 및 실행
        generator = LoanDataGenerator(db_config)
        generator.generate_and_save_data(num_records)
        
        print("\n" + "=" * 50)
        print("데이터 생성이 완료되었습니다!")
        print("=" * 50)
        
        # 데이터 생성 완료 후 컨테이너 종료
        print("데이터 생성기 작업 완료. 컨테이너를 종료합니다.")
        
    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
