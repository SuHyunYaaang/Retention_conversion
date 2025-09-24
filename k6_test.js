// load-breakpoint-fixed.js
import http from 'k6/http';
import { check, sleep } from 'k6';

// ====== 환경변수로 쉽게 튜닝 ======
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8090';
const ENDPOINT = __ENV.ENDPOINT || '/';
const SVC      = __ENV.SVC || 'api';
const ENV      = __ENV.ENV || 'test';

// 부하 단계(RPS) 정의
const START_RPS = Number(__ENV.START_RPS || 100);
const MAX_RPS   = Number(__ENV.MAX_RPS   || 800);
const STEP_RPS  = Number(__ENV.STEP_RPS  || 100);
const STAGE_SEC = __ENV.STAGE_SEC || '120s';
const TIME_UNIT = __ENV.TIME_UNIT || '1s';
const P95_MS    = Number(__ENV.P95_MS || 500);
const THINK     = Number(__ENV.THINK || 0.1);

// ARR는 VU 여유가 중요
const PRE_VUS = Number(__ENV.PRE_VUS || 300);
const MAX_VUS = Number(__ENV.MAX_VUS || 2000);

// 동적으로 스테이지 구성
const stages = [];
for (let r = START_RPS; r <= MAX_RPS; r += STEP_RPS) {
  stages.push({ target: r, duration: STAGE_SEC });
}
// 램프다운(선택)
stages.push({ target: Math.max(1, Math.floor(START_RPS / 2)), duration: '60s' });

export const options = {
  // 필요 없으면 주석: 응답 바디가 크면 꺼두는 게 좋아요
  // discardResponseBodies: true,

  thresholds: {
    // 에러율 < 1%
    http_req_failed: ['rate<0.01'],

    // p95 SLO (svc 라벨별로 평가)  ← 동적 키 사용
    // 예: http_req_duration{svc:api}: p(95)<500
    [`http_req_duration{svc:${SVC}}`]: [`p(95)<${P95_MS}`],

    // 목표 RPS 미달이 없어야 함(해당 시나리오 한정)
    'dropped_iterations{scenario:breakpoint}': ['count==0'],
  },

  scenarios: {
    breakpoint: {
      executor: 'ramping-arrival-rate',
      startRate: START_RPS,
      timeUnit: TIME_UNIT,
      preAllocatedVUs: PRE_VUS,
      maxVUs: MAX_VUS,
      stages,
      tags: { svc: SVC, env: ENV, kind: 'breakpoint' },
    },
  },

  summaryTrendStats: ['min', 'avg', 'p(90)', 'p(95)', 'p(99)', 'max'],
};

export default function () {
  const res = http.get(`${BASE_URL}${ENDPOINT}`, {
    tags: { svc: SVC, env: ENV, endpoint: ENDPOINT },
  });

  // 2xx면 성공으로 간주 (200만 체크하면 204/201도 실패로 집계됨)
  check(res, { 'status 2xx': (r) => r.status >= 200 && r.status < 300 });

  sleep(THINK);
}
