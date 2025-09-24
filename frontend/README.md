# 재대출 자동화 프론트엔드

Next.js를 기반으로 한 재대출 자동화 서비스의 프론트엔드 애플리케이션입니다.

## 🚀 주요 기능

- **대시보드**: 전체 현황 및 통계 정보 표시
- **고객 관리**: 고객 정보 조회, 검색, 편집
- **대출 관리**: 대출 정보 관리
- **재대출 신청**: 재대출 신청 처리 및 상태 관리
- **모바일 지원**: 반응형 디자인으로 모바일에서도 사용 가능
- **실시간 검색**: 고객 정보 실시간 검색 기능

## 🛠 기술 스택

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **State Management**: React Hooks

## 📁 프로젝트 구조

```
frontend/
├── app/
│   ├── globals.css          # 전역 스타일
│   ├── layout.tsx           # 루트 레이아웃
│   └── page.tsx             # 메인 페이지
├── components/
│   ├── ui/                  # 기본 UI 컴포넌트
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Input.tsx
│   ├── CustomerCard.tsx     # 고객 카드 컴포넌트
│   ├── Header.tsx           # 헤더 컴포넌트
│   └── LoadingSpinner.tsx   # 로딩 스피너
├── lib/
│   └── api.ts              # API 통신 함수
├── types/
│   └── index.ts            # TypeScript 타입 정의
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── README.md
```

## 🎨 디자인 시스템

### 색상 팔레트
- **Primary**: 흰색 계열 (#f8fafc ~ #ffffff)
- **Accent**: 파란색 계열 (#0ea5e9 ~ #0c4a6e)
- **Gray**: 슬레이트 계열 (#f1f5f9 ~ #0f172a)

### 컴포넌트
- **Button**: 5가지 variant (primary, secondary, outline, ghost, danger)
- **Card**: 호버 효과와 그림자 지원
- **Input**: 아이콘과 에러 상태 지원
- **LoadingSpinner**: 3가지 크기 지원

## 🚀 설치 및 실행

### 1. 의존성 설치

```bash
cd frontend
npm install
```

### 2. 환경 변수 설정

```bash
# .env.local 파일 생성
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 3. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 http://localhost:3000 으로 접속하세요.

## 📱 모바일 지원

- **반응형 디자인**: 모든 화면 크기에서 최적화
- **터치 친화적**: 모바일 터치 인터페이스 최적화
- **성능 최적화**: 모바일에서도 빠른 로딩 속도

## 🔌 API 연동

### 주요 API 엔드포인트

- **고객 관리**: `/api/v1/customers/`
- **대출 관리**: `/api/v1/loans/`
- **재대출 신청**: `/api/v1/refinance-applications/`
- **상품 관리**: `/api/v1/refinance-products/`

### 에러 처리

- 통합된 에러 처리 시스템
- 사용자 친화적인 에러 메시지
- 네트워크 오류 자동 복구

## 🎯 주요 페이지

### 1. 대시보드 (메인 페이지)
- 전체 통계 정보 표시
- 고객 목록 조회 및 검색
- 빠른 액션 버튼

### 2. 고객 관리
- 고객 정보 CRUD
- 실시간 검색
- 고객별 상세 정보

### 3. 대출 관리
- 대출 정보 관리
- 고객별 대출 목록
- 대출 상태 추적

### 4. 재대출 신청
- 신청 상태 관리
- 진행 상황 추적
- 문서 업로드

## 🔧 개발 가이드

### 컴포넌트 개발

```typescript
// 새로운 컴포넌트 예시
import React from 'react';
import { ComponentProps } from '@/types';

const MyComponent: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  return (
    <div className="bg-white rounded-lg p-4">
      {/* 컴포넌트 내용 */}
    </div>
  );
};

export default MyComponent;
```

### API 호출

```typescript
import { customerAPI } from '@/lib/api';

// 고객 목록 조회
const customers = await customerAPI.getCustomers();

// 고객 생성
const newCustomer = await customerAPI.createCustomer(customerData);
```

### 스타일링

```typescript
// Tailwind CSS 클래스 사용
<div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
  {/* 내용 */}
</div>
```

## 🧪 테스트

```bash
# 테스트 실행
npm test

# 테스트 커버리지
npm run test:coverage
```

## 📦 빌드 및 배포

```bash
# 프로덕션 빌드
npm run build

# 프로덕션 서버 실행
npm start
```

## 🔒 보안

- **CORS 설정**: 백엔드와 안전한 통신
- **입력 검증**: 클라이언트 사이드 유효성 검사
- **XSS 방지**: React의 기본 보안 기능 활용

## 📈 성능 최적화

- **코드 스플리팅**: Next.js 자동 코드 분할
- **이미지 최적화**: Next.js Image 컴포넌트 사용
- **캐싱**: API 응답 캐싱
- **번들 최적화**: Tree shaking 및 압축

## 🤝 기여

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
