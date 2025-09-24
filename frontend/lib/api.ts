import axios from 'axios';
import { 
  Customer, 
  Loan, 
  RefinanceApplication, 
  RefinanceProduct, 
  Document,
  APIResponse,
  CustomerFormData,
  LoanFormData,
  RefinanceFormData,
  SearchFilters,
  LoanData,
  LoanStats,
  LoanDataResponse,
  LoanStatsResponse
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// axios 인스턴스 생성
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// 요청 인터셉터
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

// 고객 관련 API
export const customerAPI = {
  // 고객 목록 조회
  getCustomers: async (skip = 0, limit = 100): Promise<Customer[]> => {
    const response = await api.get(`/customers/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // 고객 상세 조회
  getCustomer: async (customerId: string): Promise<Customer> => {
    const response = await api.get(`/customers/${customerId}`);
    return response.data;
  },

  // 고객 생성
  createCustomer: async (customerData: CustomerFormData): Promise<Customer> => {
    const response = await api.post('/customers/', customerData);
    return response.data;
  },

  // 고객 정보 수정
  updateCustomer: async (customerId: string, customerData: Partial<CustomerFormData>): Promise<Customer> => {
    const response = await api.put(`/customers/${customerId}`, customerData);
    return response.data;
  },

  // 고객 검색
  searchCustomers: async (filters: SearchFilters): Promise<Customer[]> => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.append(key, value);
    });
    const response = await api.get(`/customers/?${params.toString()}`);
    return response.data;
  },
};

// 대출 관련 API
export const loanAPI = {
  // 대출 목록 조회
  getLoans: async (skip = 0, limit = 100): Promise<Loan[]> => {
    const response = await api.get(`/loans/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // 대출 상세 조회
  getLoan: async (loanId: number): Promise<Loan> => {
    const response = await api.get(`/loans/${loanId}`);
    return response.data;
  },

  // 고객별 대출 목록 조회
  getCustomerLoans: async (customerId: string, skip = 0, limit = 100): Promise<Loan[]> => {
    const response = await api.get(`/customers/${customerId}/loans/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // 대출 생성
  createLoan: async (loanData: LoanFormData): Promise<Loan> => {
    const response = await api.post('/loans/', loanData);
    return response.data;
  },

  // 대출 정보 수정
  updateLoan: async (loanId: number, loanData: Partial<LoanFormData>): Promise<Loan> => {
    const response = await api.put(`/loans/${loanId}`, loanData);
    return response.data;
  },
};

// 재대출 신청 관련 API
export const refinanceAPI = {
  // 재대출 신청 목록 조회
  getApplications: async (skip = 0, limit = 100): Promise<RefinanceApplication[]> => {
    const response = await api.get(`/refinance-applications/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // 재대출 신청 상세 조회
  getApplication: async (applicationId: number): Promise<RefinanceApplication> => {
    const response = await api.get(`/refinance-applications/${applicationId}`);
    return response.data;
  },

  // 신청 번호로 조회
  getApplicationByNumber: async (applicationNumber: string): Promise<RefinanceApplication> => {
    const response = await api.get(`/refinance-applications/number/${applicationNumber}`);
    return response.data;
  },

  // 고객별 재대출 신청 목록 조회
  getCustomerApplications: async (customerId: string, skip = 0, limit = 100): Promise<RefinanceApplication[]> => {
    const response = await api.get(`/customers/${customerId}/refinance-applications/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // 상태별 재대출 신청 목록 조회
  getApplicationsByStatus: async (status: string, skip = 0, limit = 100): Promise<RefinanceApplication[]> => {
    const response = await api.get(`/refinance-applications/status/${status}?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // 재대출 신청 생성
  createApplication: async (applicationData: RefinanceFormData): Promise<RefinanceApplication> => {
    const response = await api.post('/refinance-applications/', applicationData);
    return response.data;
  },

  // 재대출 신청 수정
  updateApplication: async (applicationId: number, applicationData: Partial<RefinanceFormData>): Promise<RefinanceApplication> => {
    const response = await api.put(`/refinance-applications/${applicationId}`, applicationData);
    return response.data;
  },

  // 통합 재대출 신청 처리
  applyRefinance: async (requestData: any): Promise<APIResponse> => {
    const response = await api.post('/refinance/apply/', requestData);
    return response.data;
  },
};

// 재대출 상품 관련 API
export const productAPI = {
  // 활성 상품 목록 조회
  getActiveProducts: async (skip = 0, limit = 100): Promise<RefinanceProduct[]> => {
    const response = await api.get(`/refinance-products/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // 상품 상세 조회
  getProduct: async (productId: number): Promise<RefinanceProduct> => {
    const response = await api.get(`/refinance-products/${productId}`);
    return response.data;
  },

  // 상품 생성
  createProduct: async (productData: Partial<RefinanceProduct>): Promise<RefinanceProduct> => {
    const response = await api.post('/refinance-products/', productData);
    return response.data;
  },

  // 상품 수정
  updateProduct: async (productId: number, productData: Partial<RefinanceProduct>): Promise<RefinanceProduct> => {
    const response = await api.put(`/refinance-products/${productId}`, productData);
    return response.data;
  },
};

// 문서 관련 API
export const documentAPI = {
  // 신청별 문서 목록 조회
  getApplicationDocuments: async (applicationId: number): Promise<Document[]> => {
    const response = await api.get(`/refinance-applications/${applicationId}/documents/`);
    return response.data;
  },

  // 문서 생성
  createDocument: async (documentData: Partial<Document>): Promise<Document> => {
    const response = await api.post('/retention/', documentData);
    return response.data;
  },
};


// 대출 데이터 관련 API
export const loanDataAPI = {
  // 대출 데이터 조회 (페이지네이션) - 실제 엔드포인트로 변경
  getLoanData: async (page = 1, limit = 50): Promise<LoanDataResponse> => {
    const response = await api.get(`/refinance/loan-data/?page=${page}&limit=${limit}`);
    return response.data;
  },

  // 대출 통계 조회 - 실제 엔드포인트로 변경
  getLoanStats: async (): Promise<LoanStatsResponse> => {
    const response = await api.get('/refinance/loan-stats/');
    return response.data;
  },
};

// 에러 처리 유틸리티
export const handleAPIError = (error: any): string => {
  if (error.response?.data?.detail) {
    return error.response.data.detail;
  }
  if (error.response?.data?.message) {
    return error.response.data.message;
  }
  if (error.message) {
    return error.message;
  }
  return '알 수 없는 오류가 발생했습니다.';
};

export default api;