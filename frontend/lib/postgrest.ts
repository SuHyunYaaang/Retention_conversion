import axios from 'axios';

const POSTGREST_URL = process.env.NEXT_PUBLIC_POSTGREST_URL || 'http://localhost:8090/postgrest';

// PostgREST API 인스턴스 생성
const postgrest = axios.create({
  baseURL: POSTGREST_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: 10000,
});

// 요청 인터셉터
postgrest.interceptors.request.use(
  (config) => {
    console.log('PostgREST Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터
postgrest.interceptors.response.use(
  (response) => {
    console.log('PostgREST Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('PostgREST Error:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

// PostgREST API 함수들
export const postgrestAPI = {
  // 고객 관련 API
  customers: {
    // 고객 목록 조회
    get: async (params?: any) => {
      const response = await postgrest.get('/customers', { params });
      return response.data;
    },

    // 고객 상세 조회
    getById: async (id: string) => {
      const response = await postgrest.get(`/customers?customer_id=eq.${id}`);
      return response.data[0];
    },

    // 고객 생성
    create: async (data: any) => {
      const response = await postgrest.post('/customers', data);
      return response.data[0];
    },

    // 고객 수정
    update: async (id: string, data: any) => {
      const response = await postgrest.patch(`/customers?customer_id=eq.${id}`, data);
      return response.data[0];
    },

    // 고객 삭제
    delete: async (id: string) => {
      const response = await postgrest.delete(`/customers?customer_id=eq.${id}`);
      return response.data;
    },

    // 고객 검색
    search: async (query: string) => {
      const response = await postgrest.get(`/customers?or=(name.ilike.*${query}*,customer_id.ilike.*${query}*,phone.ilike.*${query}*)`);
      return response.data;
    },
  },

  // 대출 관련 API
  loans: {
    // 대출 목록 조회
    get: async (params?: any) => {
      const response = await postgrest.get('/loans', { params });
      return response.data;
    },

    // 고객별 대출 목록 조회
    getByCustomer: async (customerId: number) => {
      const response = await postgrest.get(`/loans?customer_id=eq.${customerId}`);
      return response.data;
    },

    // 대출 생성
    create: async (data: any) => {
      const response = await postgrest.post('/loans', data);
      return response.data[0];
    },

    // 대출 수정
    update: async (id: number, data: any) => {
      const response = await postgrest.patch(`/loans?id=eq.${id}`, data);
      return response.data[0];
    },

    // 대출 삭제
    delete: async (id: number) => {
      const response = await postgrest.delete(`/loans?id=eq.${id}`);
      return response.data;
    },
  },

  // 재대출 신청 관련 API
  applications: {
    // 신청 목록 조회
    get: async (params?: any) => {
      const response = await postgrest.get('/refinance_applications', { params });
      return response.data;
    },

    // 고객별 신청 목록 조회
    getByCustomer: async (customerId: number) => {
      const response = await postgrest.get(`/refinance_applications?customer_id=eq.${customerId}`);
      return response.data;
    },

    // 상태별 신청 목록 조회
    getByStatus: async (status: string) => {
      const response = await postgrest.get(`/refinance_applications?application_status=eq.${status}`);
      return response.data;
    },

    // 신청 생성
    create: async (data: any) => {
      const response = await postgrest.post('/refinance_applications', data);
      return response.data[0];
    },

    // 신청 수정
    update: async (id: number, data: any) => {
      const response = await postgrest.patch(`/refinance_applications?id=eq.${id}`, data);
      return response.data[0];
    },

    // 신청 삭제
    delete: async (id: number) => {
      const response = await postgrest.delete(`/refinance_applications?id=eq.${id}`);
      return response.data;
    },
  },

  // 재대출 상품 관련 API
  products: {
    // 상품 목록 조회
    get: async (params?: any) => {
      const response = await postgrest.get('/refinance_products', { params });
      return response.data;
    },

    // 활성 상품 목록 조회
    getActive: async () => {
      const response = await postgrest.get('/refinance_products?is_active=eq.true');
      return response.data;
    },

    // 상품 생성
    create: async (data: any) => {
      const response = await postgrest.post('/refinance_products', data);
      return response.data[0];
    },

    // 상품 수정
    update: async (id: number, data: any) => {
      const response = await postgrest.patch(`/refinance_products?id=eq.${id}`, data);
      return response.data[0];
    },

    // 상품 삭제
    delete: async (id: number) => {
      const response = await postgrest.delete(`/refinance_products?id=eq.${id}`);
      return response.data;
    },
  },

  // 문서 관련 API
  documents: {
    // 문서 목록 조회
    get: async (params?: any) => {
      const response = await postgrest.get('/documents', { params });
      return response.data;
    },

    // 신청별 문서 목록 조회
    getByApplication: async (applicationId: number) => {
      const response = await postgrest.get(`/documents?application_id=eq.${applicationId}`);
      return response.data;
    },

    // 문서 생성
    create: async (data: any) => {
      const response = await postgrest.post('/documents', data);
      return response.data[0];
    },

    // 문서 삭제
    delete: async (id: number) => {
      const response = await postgrest.delete(`/documents?id=eq.${id}`);
      return response.data;
    },
  },

  // 로그 관련 API
  logs: {
    // 로그 목록 조회
    get: async (params?: any) => {
      const response = await postgrest.get('/application_logs', { params });
      return response.data;
    },

    // 신청별 로그 목록 조회
    getByApplication: async (applicationId: number) => {
      const response = await postgrest.get(`/application_logs?application_id=eq.${applicationId}&order=performed_at.desc`);
      return response.data;
    },

    // 로그 생성
    create: async (data: any) => {
      const response = await postgrest.post('/application_logs', data);
      return response.data[0];
    },
  },
};

// 관계형 데이터 조회 함수들
export const postgrestRelations = {
  // 고객과 대출 정보 함께 조회
  getCustomerWithLoans: async (customerId: string) => {
    const response = await postgrest.get(`/customers?customer_id=eq.${customerId}&select=*,loans(*)`);
    return response.data[0];
  },

  // 고객과 신청 정보 함께 조회
  getCustomerWithApplications: async (customerId: string) => {
    const response = await postgrest.get(`/customers?customer_id=eq.${customerId}&select=*,refinance_applications(*)`);
    return response.data[0];
  },

  // 신청과 문서 정보 함께 조회
  getApplicationWithDocuments: async (applicationId: number) => {
    const response = await postgrest.get(`/refinance_applications?id=eq.${applicationId}&select=*,documents(*)`);
    return response.data[0];
  },

  // 신청과 로그 정보 함께 조회
  getApplicationWithLogs: async (applicationId: number) => {
    const response = await postgrest.get(`/refinance_applications?id=eq.${applicationId}&select=*,application_logs(*)`);
    return response.data[0];
  },
};

// 에러 처리 유틸리티
export const handlePostgRESTError = (error: any): string => {
  if (error.response?.data?.message) {
    return error.response.data.message;
  }
  if (error.response?.data?.hint) {
    return error.response.data.hint;
  }
  if (error.response?.data?.details) {
    return error.response.data.details;
  }
  if (error.message) {
    return error.message;
  }
  return 'PostgREST API 오류가 발생했습니다.';
};

export default postgrest;
