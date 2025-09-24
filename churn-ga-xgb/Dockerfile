# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the ML scripts
COPY churn-ga-xgb.py .
COPY churn-ga-xgb-db.py .
COPY docker_data_loader.py .
COPY create_ml_table.py .

# Copy data directory
COPY data/ ./data/

# Create directories for outputs
RUN mkdir -p /app/outputs /app/data

# Create startup script
RUN echo '#!/bin/bash\n\
echo "=== 머신러닝 서비스 시작 ==="\n\
echo "1. 데이터베이스 연결 확인 중..."\n\
sleep 10\n\
echo "2. CSV 데이터를 DB에 적재 중..."\n\
python create_ml_table.py\n\
python docker_data_loader.py\n\
echo "3. 머신러닝 모델 학습 시작..."\n\
python churn-ga-xgb-db.py --table ml_training_data --target EverDelinquent --test_size 0.2 --kfold 5 --generations 10 --population 20 --outdir outputs\n\
echo "=== 머신러닝 서비스 완료 ==="\n\
' > /app/start.sh && chmod +x /app/start.sh

# Set default command to run the startup script
CMD ["/app/start.sh"]
