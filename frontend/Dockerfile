# 빌드 스테이지
FROM node:18-alpine AS builder

# 작업 디렉토리 설정
WORKDIR /app

# package.json과 package-lock.json 복사
COPY package*.json ./

# 의존성 설치
RUN npm install --only=production

# 소스 코드 복사
COPY . .

# Next.js 애플리케이션 빌드
RUN npm run build

# 프로덕션 스테이지
FROM node:18-alpine AS runner

WORKDIR /app

# curl 설치 (헬스 체크용)
RUN apk add --no-cache curl

# 필요한 패키지 설치
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# 빌드된 애플리케이션 복사

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# 사용자 권한 설정
USER nextjs

# 포트 노출
EXPOSE 3000

# 환경 변수 설정
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# 헬스 체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

# 애플리케이션 실행
CMD ["node", "server.js"]
