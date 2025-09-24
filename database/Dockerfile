FROM postgres:15-alpine

# 데이터베이스 초기화 스크립트 복사
COPY init.sql /docker-entrypoint-initdb.d/

# PostgreSQL 설정 최적화
RUN echo "max_connections = 100" >> /usr/local/share/postgresql/postgresql.conf.sample && \
    echo "shared_buffers = 256MB" >> /usr/local/share/postgresql/postgresql.conf.sample && \
    echo "effective_cache_size = 1GB" >> /usr/local/share/postgresql/postgresql.conf.sample && \
    echo "maintenance_work_mem = 64MB" >> /usr/local/share/postgresql/postgresql.conf.sample && \
    echo "checkpoint_completion_target = 0.9" >> /usr/local/share/postgresql/postgresql.conf.sample && \
    echo "wal_buffers = 16MB" >> /usr/local/share/postgresql/postgresql.conf.sample && \
    echo "default_statistics_target = 100" >> /usr/local/share/postgresql/postgresql.conf.sample

# 헬스 체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pg_isready -U retention_user -d retention_db || exit 1

EXPOSE 5432
