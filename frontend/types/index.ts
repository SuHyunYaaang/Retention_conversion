// API 응답 타입들
export interface Customer {
  id: number;
  customer_id: string;
  name: string;
  phone: string;
  email?: string;
  birth_date?: string;
  address?: string;
  created_at: string;
  updated_at?: string;
}

export interface Loan {
  id: number;
  customer_id: number;
  loan_number: string;
  loan_type: string;
  loan_amount: number;
  interest_rate: number;
  remaining_amount: number;
  monthly_payment: number;
  loan_start_date?: string;
  loan_end_date?: string;
  bank_name?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface RefinanceApplication {
  id: number;
  application_number: string;
  customer_id: number;
  original_loan_id: number;
  requested_amount: number;
  requested_interest_rate?: number;
  application_status: string;
  application_date: string;
  approval_date?: string;
  rejection_reason?: string;
  created_at: string;
  updated_at?: string;
}

export interface RefinanceProduct {
  id: number;
  product_name: string;
  product_code: string;
  min_interest_rate: number;
  max_interest_rate: number;
  min_loan_amount: number;
  max_loan_amount: number;
  loan_term_min: number;
  loan_term_max: number;
  eligibility_criteria?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface Document {
  id: number;
  application_id: number;
  document_type: string;
  file_name: string;
  file_path: string;
  file_size?: number;
  upload_date: string;
}

export interface APIResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
}

// 컴포넌트 Props 타입들
export interface CustomerCardProps {
  customer: Customer;
  onEdit?: (customer: Customer) => void;
  onDelete?: (id: number) => void;
}

export interface LoanCardProps {
  loan: Loan;
  onEdit?: (loan: Loan) => void;
}

export interface ApplicationCardProps {
  application: RefinanceApplication;
  onViewDetails?: (application: RefinanceApplication) => void;
}

export interface ProductCardProps {
  product: RefinanceProduct;
  onSelect?: (product: RefinanceProduct) => void;
}

// 폼 데이터 타입들
export interface CustomerFormData {
  customer_id: string;
  name: string;
  phone: string;
  email?: string;
  birth_date?: string;
  address?: string;
}

export interface LoanFormData {
  customer_id: number;
  loan_number: string;
  loan_type: string;
  loan_amount: number;
  interest_rate: number;
  remaining_amount: number;
  monthly_payment: number;
  loan_start_date?: string;
  loan_end_date?: string;
  bank_name?: string;
}

export interface RefinanceFormData {
  customer_id: number;
  original_loan_id: number;
  requested_amount: number;
  requested_interest_rate?: number;
}

// 검색 및 필터 타입들
export interface SearchFilters {
  customer_id?: string;
  name?: string;
  phone?: string;
  status?: string;
  date_from?: string;
  date_to?: string;
}

export interface PaginationParams {
  page: number;
  limit: number;
  total: number;
}

// 상태 관리 타입들
export interface AppState {
  customers: Customer[];
  loans: Loan[];
  applications: RefinanceApplication[];
  products: RefinanceProduct[];
  loading: boolean;
  error: string | null;
}

export interface LoadingState {
  isLoading: boolean;
  message?: string;
}

// 대출 데이터 관련 타입들
export interface LoanData {
  customer_id: string;
  name: string;
  age: number;
  phone: string;
  email: string;
  job_type: string;
  income_level: string;
  credit_grade: string;
  address: string;
  loan_id: string;
  loan_type: string;
  loan_amount: number;
  loan_term: number;
  interest_rate: number;
  monthly_payment: number;
  status: string;
  application_date: string | null;
  approval_date: string | null;
  disbursement_date: string | null;
  overdue_days: number;
  overdue_amount: number;
  created_at: string | null;
}

export interface LoanStats {
  total_customers: number;
  total_loans: number;
  status_stats: Record<string, number>;
  loan_type_stats: Record<string, number>;
  avg_loan_amount: number;
}

export interface PaginationInfo {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
}

export interface LoanDataResponse {
  success: boolean;
  data: LoanData[];
  pagination: PaginationInfo;
}

export interface LoanStatsResponse {
  success: boolean;
  data: LoanStats;
}

// 미래 대출 한도 시뮬레이션 관련 타입들
export interface LoanSimulationScenario {
  id: string;
  name: string;
  description: string;
  income_change: number; // 소득 변화율 (%)
  debt_change: number; // 부채 변화율 (%)
  credit_score_change: number; // 신용점수 변화
  interest_rate_change: number; // 금리 변화율 (%)
  expected_loan_limit: number; // 예상 대출 한도
  probability: number; // 발생 확률 (%)
  timeframe: number; // 예상 기간 (개월)
}

export interface CustomerFinancialProfile {
  customer_id: string;
  name: string;
  current_income: number;
  current_debt: number;
  current_credit_score: number;
  current_loan_limit: number;
  current_interest_rate: number;
  monthly_expenses: number;
  savings_rate: number;
  risk_level: 'low' | 'medium' | 'high';
}

export interface SimulationResult {
  scenario: LoanSimulationScenario;
  current_limit: number;
  projected_limit: number;
  improvement_amount: number;
  improvement_percentage: number;
  recommended_actions: string[];
  risk_factors: string[];
}

export interface SimulationRequest {
  customer_id: string;
  scenarios: Partial<LoanSimulationScenario>[];
}

export interface SimulationResponse {
  success: boolean;
  data: {
    customer_profile: CustomerFinancialProfile;
    simulations: SimulationResult[];
    ai_recommendations: string[];
  };
}
