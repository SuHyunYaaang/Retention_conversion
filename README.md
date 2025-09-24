Copyright 양수현 

* 프로젝트 소개 : 재대출(Retention) 자동화 서비스
* 내용 : 대환이 성행 중. 현재는 재대출이 고정금리로 제공되고 있음
        이에 초개인화 재대출 상품 탐색방법을 도입, 소비자로 하여금 대환과 재대출 중 고민할 수 있도록 함
        경기부진 중 기존 고객의 유지와 로얄티를 높이는 데에 도움이 될 것이라 가정


* Architecture
- Container Managing : Kubernetes
- Language : Python (JSON, Pandas, PDF Reader etc)
- DB : PostgreSQL(PostgREST)
- Back-end : FastAPI, NginX, Node.js
- Front-end : Next.js, JavaScript, TypeScript


* 작업 중

# 재대출 자동화 시스템 (Retention System)

## 📋 프로젝트 개요

이 프로젝트는 대출 금융 데이터를 관리하고 시각화하는 웹 애플리케이션입니다. Docker를 사용하여 컨테이너화된 마이크로서비스 아키텍처로 구성되어 있으며, 1000개의 샘플 대출 데이터를 생성하고 관리할 수 있습니다.

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
│   Port: 8090    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Nginx         │
                    │   (Reverse      │
                    │    Proxy)       │
                    │   Port: 8090    │
                    └─────────────────┘
```

## 🛠️ 기술 스택

### Frontend
- **Next.js 14** (App Router)
- **React 18**
- **TypeScript**
- **Tailwind CSS**
- **Lucide React** (아이콘)
- **Axios** (HTTP 클라이언트)

### Backend
- **FastAPI** (Python)
- **SQLAlchemy** (ORM)
- **psycopg2** (PostgreSQL 드라이버)
- **Pydantic** (데이터 검증)

### Database
- **PostgreSQL 15**
- **PostgREST** (REST API)

### Infrastructure
- **Docker & Docker Compose**
- **Nginx** (리버스 프록시)
- **Python 3.11**

## 📁 프로젝트 구조

```
Retention/
├── frontend/                 # Next.js 프론트엔드
│   ├── app/
│   │   ├── page.tsx         # 메인 대시보드
│   │   └── layout.tsx       # 레이아웃
│   ├── components/
│   │   ├── Header.tsx       # 네비게이션 헤더
│   │   ├── LoanDataCard.tsx # 대출 데이터 카드
│   │   ├── Pagination.tsx   # 페이지네이션
│   │   └── StatsCard.tsx    # 통계 카드
│   ├── lib/
│   │   └── api.ts          # API 클라이언트
│   ├── types/
│   │   └── index.ts        # TypeScript 타입 정의
│   ├── Dockerfile          # 프론트엔드 컨테이너
│   └── next.config.js      # Next.js 설정
├── backend/                 # FastAPI 백엔드
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints.py # API 엔드포인트
│   │   ├── database.py      # 데이터베이스 연결
│   │   └── main.py          # FastAPI 앱
│   ├── requirements.txt     # Python 의존성
│   └── Dockerfile          # 백엔드 컨테이너
├── data_generator/          # 데이터 생성 스크립트
│   ├── loan_data_generator.py # 메인 데이터 생성기
│   ├── run_generator.py     # 실행 스크립트
│   ├── requirements.txt     # Python 의존성
│   ├── Dockerfile          # 데이터 생성기 컨테이너
│   ├── generate_data.sh    # 실행 쉘 스크립트
│   └── README.md           # 데이터 생성기 문서
├── nginx/                   # Nginx 설정
│   ├── nginx.conf          # 메인 Nginx 설정
│   └── conf.d/
│       └── default.conf    # 서버 설정
├── docker-compose.yml       # Docker Compose 설정
├── build.bat               # 빌드 스크립트 (Windows)
└── README_cursor.md        # 이 파일
```

## 🚀 설치 및 실행

### 1. 사전 요구사항
- Docker Desktop
- Git

### 2. 프로젝트 클론
```bash
git clone <repository-url>
cd Retention
```

### 3. 데이터 생성 (선택사항)
```bash
cd data_generator
docker build -t loan-data-generator .
docker run --rm --network retention_default loan-data-generator
```

### 4. 애플리케이션 실행
```bash
# 전체 서비스 빌드 및 실행
docker-compose up -d

# 또는 개별 서비스 실행
docker-compose up -d postgres
docker-compose up -d backend
docker-compose up -d frontend
docker-compose up -d nginx
```

### 5. 접속
- **프론트엔드**: http://localhost:8090
- **백엔드 API**: http://localhost:8000
- **PostgreSQL**: localhost:5432

## 📊 데이터베이스 스키마

### customers 테이블
```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### loans 테이블
```sql
CREATE TABLE loans (
    loan_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    loan_amount DECIMAL(15,2) NOT NULL,
    interest_rate DECIMAL(5,2) NOT NULL,
    loan_term INTEGER NOT NULL,
    loan_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE NOT NULL
);
```

### repayments 테이블
```sql
CREATE TABLE repayments (
    repayment_id SERIAL PRIMARY KEY,
    loan_id INTEGER REFERENCES loans(loan_id),
    amount DECIMAL(15,2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔌 API 엔드포인트

### 대출 데이터 조회
```
GET /loan-data/
Query Parameters:
- page: 페이지 번호 (기본값: 1)
- limit: 페이지당 항목 수 (기본값: 50)
- search: 검색어 (고객명, 이메일)
```

### 대출 통계 조회
```
GET /loan-stats/
Response: 총 고객 수, 총 대출 수, 상태별/유형별 분포, 평균 대출 금액
```

## 🎨 프론트엔드 기능

### 메인 대시보드
- **통계 카드**: 총 고객 수, 총 대출 수, 활성 대출, 평균 대출 금액
- **대출 데이터 카드**: 고객 정보, 대출 상세 정보, 상태 표시
- **검색 기능**: 고객명 또는 이메일로 검색
- **페이지네이션**: 50개씩 페이지 단위로 표시

### 반응형 디자인
- **데스크톱**: 카드 그리드 레이아웃
- **모바일**: 세로 스택 레이아웃
- **태블릿**: 중간 크기 그리드

## 🔧 주요 설정 파일

### docker-compose.yml
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: retention
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/retention

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "8090:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/conf.d:/etc/nginx/conf.d
    depends_on:
      - frontend
      - backend

volumes:
  postgres_data:
```

### nginx/conf.d/default.conf
```nginx
server {
    listen 80;
    server_name localhost;

    # Next.js 정적 파일 프록시
    location /_next/ {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # API 요청을 백엔드로 프록시
    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 나머지 요청을 프론트엔드로 프록시
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🐛 문제 해결

### 일반적인 문제들

#### 1. NextRouter 오류
**문제**: `Error: NextRouter was not mounted`
**해결**: App Router에서는 `useRouter` 대신 `usePathname` 사용
```typescript
// ❌ 잘못된 방법
import { useRouter } from 'next/router';

// ✅ 올바른 방법
import { usePathname } from 'next/navigation';
```

#### 2. Nginx 404 오류
**문제**: `_next/static/` 파일들이 404 반환
**해결**: Nginx 설정에서 Next.js 정적 파일 프록시 추가

#### 3. 데이터베이스 연결 오류
**문제**: 백엔드가 PostgreSQL에 연결할 수 없음
**해결**: `DATABASE_URL`에서 `localhost`를 `postgres`로 변경

#### 4. Python 패키지 설치 오류
**문제**: `psycopg2-binary` 설치 실패
**해결**: `psycopg2` 사용 및 필요한 시스템 라이브러리 설치

## 📈 성능 최적화

### 프론트엔드
- **페이지네이션**: 50개씩 로드하여 초기 로딩 시간 단축
- **이미지 최적화**: Next.js Image 컴포넌트 사용
- **코드 분할**: 동적 import로 번들 크기 최적화

### 백엔드
- **데이터베이스 인덱싱**: 자주 조회되는 컬럼에 인덱스 추가
- **쿼리 최적화**: JOIN과 LIMIT 사용으로 효율적인 데이터 조회
- **캐싱**: Redis 도입 고려 (향후 확장)

### 데이터베이스
- **연결 풀링**: SQLAlchemy connection pool 설정
- **쿼리 최적화**: 적절한 WHERE 절과 ORDER BY 사용

## 🔒 보안 고려사항

### 현재 구현된 보안
- **환경 변수**: 데이터베이스 자격 증명 분리
- **CORS 설정**: FastAPI에서 허용된 도메인만 접근
- **입력 검증**: Pydantic 모델을 통한 데이터 검증

### 향후 개선 사항
- **인증/인가**: JWT 토큰 기반 사용자 인증
- **HTTPS**: SSL/TLS 인증서 적용
- **Rate Limiting**: API 요청 제한
- **SQL Injection 방지**: 파라미터화된 쿼리 사용

## 🚀 배포 가이드

### 개발 환경
```bash
# 개발 모드 실행
docker-compose -f docker-compose.dev.yml up -d
```

### 프로덕션 환경
```bash
# 프로덕션 빌드
docker-compose -f docker-compose.prod.yml up -d

# 환경 변수 설정
export DATABASE_URL=postgresql://user:password@host:5432/dbname
export SECRET_KEY=your-secret-key
```

## 📝 개발 가이드

### 새로운 기능 추가
1. **백엔드**: `backend/app/api/endpoints.py`에 새 엔드포인트 추가
2. **프론트엔드**: `frontend/components/`에 새 컴포넌트 생성
3. **타입 정의**: `frontend/types/index.ts`에 TypeScript 인터페이스 추가
4. **API 클라이언트**: `frontend/lib/api.ts`에 새 API 메서드 추가

### 코드 스타일
- **TypeScript**: 엄격한 타입 체크 사용
- **ESLint**: 코드 품질 검사
- **Prettier**: 코드 포맷팅
- **Husky**: Git hooks를 통한 자동 검사

## 🤝 기여 가이드

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 👥 팀

- **개발자**: AI Assistant
- **프로젝트 관리**: User

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해주세요.

---

**마지막 업데이트**: 2024년 12월

# 미래 대출 한도 시뮬레이션

## 📌 개념

미래 대출 한도 시뮬레이션은 고객이 **앞으로 어떤 조건에서, 어느 정도
금액까지 대출이 가능할지**를 AI가 예측·시각화해 주는 서비스입니다.

------------------------------------------------------------------------

## 🔍 기본 아이디어

-   현재 대출 한도는 **소득, 부채, 신용점수, 금리 환경** 등에 따라
    결정됩니다.
-   고객은 미래에 "소득 증가, 부채 감소, 금리 변화"와 같은 조건 변화 시
    한도가 어떻게 달라질지 궁금해합니다.
-   AI가 고객의 **재무 변화 가능성 + 시장 환경 변화 가능성**을
    시뮬레이션해 예측.

------------------------------------------------------------------------

## 💻 예시 시나리오

### 1. 현재 상태

-   한도: 7,000만 원\
-   신용점수: 780점\
-   금리: 5.2%

### 2. 시나리오 시뮬레이션

-   💼 **소득 증가 10%** → 한도 8,200만 원\
-   💳 **카드빚 상환 완료** → 한도 9,500만 원\
-   📉 **금리 1% 하락** → 한도 1억 500만 원\
-   🏠 **위 세 조건 모두 충족** → 한도 1억 2,000만 원

### 3. AI 제안

> "다음 6개월간 부채를 2,000만 원 줄이면 금리가 0.3% 낮아지고, 한도가
> 1,000만 원 증가할 것으로 예상됩니다."

------------------------------------------------------------------------

## 📈 활용 포인트

-   **고객 입장**: 미래 대출 가능성을 미리 확인하고 재무 계획 수립
-   **금융사 입장**: 고객을 장기적으로 유지하고, 재대출·추가대출
    타이밍을 예측
-   **AI 학습 요소**: 신용 변화 추세, 경기/금리 전망, 고객 지출·저축
    패턴


# 재대출 자동화 백엔드 API

재대출 자동화 서비스를 위한 FastAPI 기반 백엔드 API입니다.

## 🚀 주요 기능

- **고객 관리**: 고객 정보 등록, 조회, 수정
- **대출 관리**: 기존 대출 정보 관리
- **재대출 신청**: 재대출 신청 처리 및 상태 관리
- **상품 관리**: 재대출 상품 정보 관리
- **문서 관리**: 신청 관련 문서 업로드 및 관리
- **모바일 지원**: CORS 설정으로 모바일 웹 지원

## 🛠 기술 스택

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Migration**: Alembic
- **Documentation**: Swagger UI / ReDoc

## 📁 프로젝트 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 애플리케이션
│   ├── database.py          # 데이터베이스 연결
│   ├── models.py            # SQLAlchemy 모델
│   ├── schemas.py           # Pydantic 스키마
│   ├── crud.py              # CRUD 작업
│   └── api/
│       ├── __init__.py
│       └── endpoints.py     # API 엔드포인트
├── requirements.txt         # Python 의존성
├── alembic.ini             # Alembic 설정
├── env.example             # 환경 변수 예시
├── run.py                  # 서버 실행 스크립트
└── README.md               # 프로젝트 설명서
```

## 🗄 데이터베이스 스키마

### 주요 테이블

1. **customers**: 고객 정보
2. **loans**: 기존 대출 정보
3. **refinance_applications**: 재대출 신청 정보
4. **refinance_products**: 재대출 상품 정보
5. **documents**: 문서 정보
6. **application_logs**: 신청 로그

## 🚀 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
cp env.example .env
# .env 파일을 편집하여 데이터베이스 연결 정보 설정
```

### 3. 데이터베이스 설정

PostgreSQL 데이터베이스를 생성하고 연결 정보를 `.env` 파일에 설정합니다.

### 4. 서버 실행

```bash
python run.py
```

또는

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📚 API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 주요 API 엔드포인트

### 고객 관리
- `POST /api/v1/customers/` - 고객 생성
- `GET /api/v1/customers/{customer_id}` - 고객 조회
- `PUT /api/v1/customers/{customer_id}` - 고객 정보 수정

### 대출 관리
- `POST /api/v1/loans/` - 대출 정보 생성
- `GET /api/v1/loans/{loan_id}` - 대출 정보 조회
- `GET /api/v1/customers/{customer_id}/loans/` - 고객 대출 목록

### 재대출 신청
- `POST /api/v1/refinance-applications/` - 재대출 신청 생성
- `POST /api/v1/refinance/apply/` - 통합 재대출 신청 처리
- `GET /api/v1/refinance-applications/{application_id}` - 신청 정보 조회
- `PUT /api/v1/refinance-applications/{application_id}` - 신청 정보 수정

### 상품 관리
- `GET /api/v1/refinance-products/` - 활성 상품 목록
- `POST /api/v1/refinance-products/` - 상품 생성

## 📱 모바일 지원

- CORS 미들웨어로 모바일 웹 지원
- 반응형 API 응답 구조
- JSON 기반 데이터 교환

## 🔧 개발 환경

### 환경 변수

```env
# 데이터베이스 설정
DATABASE_URL=postgresql://username:password@localhost:5432/database_name

# 서버 설정
HOST=0.0.0.0
PORT=8000
DEBUG=True

# 보안 설정
SECRET_KEY=your-secret-key
```

### 데이터베이스 마이그레이션

```bash
# 마이그레이션 초기화
alembic init alembic

# 마이그레이션 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 실행
alembic upgrade head
```

## 🧪 테스트

```bash
# 테스트 실행 (추후 구현 예정)
pytest
```

## 📝 로깅

- 애플리케이션 로그는 INFO 레벨로 설정
- 데이터베이스 작업 로그 포함
- 에러 로그 자동 기록

## 🔒 보안

- 입력 데이터 검증 (Pydantic)
- SQL 인젝션 방지 (SQLAlchemy ORM)
- CORS 설정으로 허용된 도메인만 접근 가능

## 📈 성능 최적화

- 데이터베이스 연결 풀링
- 비동기 처리 지원
- 효율적인 쿼리 최적화

## 🤝 기여

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
