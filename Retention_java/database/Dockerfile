FROM postgres:15-alpine

# 환경 변수 설정
ENV POSTGRES_DB=retention_db
ENV POSTGRES_USER=retention_user
ENV POSTGRES_PASSWORD=retention_password

# 초기화 스크립트 복사
COPY init.sql /docker-entrypoint-initdb.d/

# 포트 노출
EXPOSE 5432

# 헬스 체크
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD pg_isready -U retention_user -d retention_db || exit 1

