import logging
import logging.config
import logging.handlers

import sys
from datetime import datetime
import json
from pathlib import Path


# LogRecord를 받아 최종 문자열로 변환하는 메서드 오버라이드
class StructuredFormatter(logging.Formatter):
    
    def format(self, record: logging.LogRecord) -> str:
        # 기본 로그 정보 (타임스탬프/레벨/로거명/메시지/module/function/발생위치)
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # 추가 컨텍스트가 LogRecord에 있으면 함께 담기(extra=... 로 전달된 값들)
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'endpoint'):
            log_entry['endpoint'] = record.endpoint
        if hasattr(record, 'method'):
            log_entry['method'] = record.method
        if hasattr(record, 'status_code'):
            log_entry['status_code'] = record.status_code
        if hasattr(record, 'response_time'):
            log_entry['response_time'] = record.response_time
            
        # 예외 정보가 있으면 스택 트레이스를 문자열로 추가
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry, ensure_ascii=False)


# 환경(development/production)에 맞춰 로깅 설정
def setup_logging(environment: str = "development") -> None:
    
    # 로그 디렉토리 생성
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 환경별 로그 레벨 설정
    log_levels = {
        "development": "DEBUG", 
        "production": "WARNING"
    }
    
    # 로깅 설정
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "structured": {
                "()": StructuredFormatter
            },
            "simple": {
                "format": "%(asctime)s\n%(funcName)s()\n%(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_levels.get(environment, "INFO"),
                "formatter": "structured",
                "stream": sys.stdout
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "structured",
                "filename": log_dir / "app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "structured",
                "filename": log_dir / "error.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            }
        },
        "loggers": {
            "": {  # 루트 로거
                "handlers": ["console", "file", "error_file"],
                "level": log_levels.get(environment, "INFO"),
                "propagate": False
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.error": {
                "handlers": ["console", "error_file"],
                "level": "ERROR",
                "propagate": False
            },
            "sqlalchemy": {
                "handlers": ["file"],
                "level": "WARNING",
                "propagate": False
            }
        }
    }
    
    logging.config.dictConfig(logging_config)




