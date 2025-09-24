'use client';

import React, { useState, useEffect } from 'react';
import { 
  Search, 
  RefreshCw, 
  Users, 
  CreditCard, 
  TrendingUp, 
  DollarSign, 
  FileText, 
  Star,
  Plus,
  Eye,
  Settings,
  BarChart3
} from 'lucide-react';
import Header from '@/components/Header';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import LoadingSpinner from '@/components/LoadingSpinner';

// 동적 렌더링 강제
export const dynamic = 'force-dynamic';
export const revalidate = 0;

interface DashboardData {
  customer_count: number;
  loan_count: number;
  refinance_count: number;
  product_count: number;
  total_assets: number;
}

interface Customer {
  id: number;
  customer_id: string;
  name: string;
  phone: string;
  email?: string;
  created_at: string;
}

interface Loan {
  id: number;
  customer_id: number;
  loan_number: string;
  loan_type: string;
  loan_amount: number;
  interest_rate: number;
  remaining_amount: number;
  monthly_payment: number;
  status: string;
  created_at: string;
}

interface RefinanceApplication {
  id: number;
  application_number: string;
  customer_id: number;
  original_loan_id: number;
  requested_amount: number;
  requested_interest_rate: number;
  application_status: string;
  application_date: string;
}

export default function MainDashboard() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loans, setLoans] = useState<Loan[]>([]);
  const [applications, setApplications] = useState<RefinanceApplication[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [searchTerm, setSearchTerm] = useState('');

  // 데이터 로드
  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // 백엔드 API에서 데이터 로드
      const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
      
      const [dashboardRes, customersRes, loansRes, applicationsRes] = await Promise.all([
        fetch(`${baseUrl}/api/dashboard`),
        fetch(`${baseUrl}/api/customers`),
        fetch(`${baseUrl}/api/loans`),
        fetch(`${baseUrl}/api/refinance-applications`)
      ]);

      if (dashboardRes.ok) {
        const dashboardData = await dashboardRes.json();
        setDashboardData(dashboardData);
      }

      if (customersRes.ok) {
        const customersData = await customersRes.json();
        setCustomers(customersData);
      }

      if (loansRes.ok) {
        const loansData = await loansRes.json();
        setLoans(loansData);
      }

      if (applicationsRes.ok) {
        const applicationsData = await applicationsRes.json();
        setApplications(applicationsData);
      }

    } catch (err) {
      console.error('데이터 로드 실패:', err);
      setError('데이터를 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  // 검색 필터링
  const handleSearch = (term: string) => {
    setSearchTerm(term);
  };

  // 상세보기 핸들러
  const handleViewDetails = (type: string, id: number) => {
    console.log(`View ${type} details:`, id);
    alert(`${type} 상세 정보를 확인합니다.`);
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  if (loading && !dashboardData) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <LoadingSpinner size="lg" message="대시보드 데이터를 불러오는 중..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 페이지 헤더 */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">
            고객데이터 통계
          </h1>
          <p className="text-slate-600">
            고객, 대출, 재대출 신청 현황을 한 눈에 확인할 수 있습니다
          </p>
        </div>

        {/* 통계 카드 */}
        {dashboardData && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <Card className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-blue-50 rounded-lg">
                  <Users className="w-6 h-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-slate-600">전체 고객</p>
                  <p className="text-2xl font-bold text-slate-900">{dashboardData.customer_count.toLocaleString()}</p>
                </div>
              </div>
            </Card>

            <Card className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-green-50 rounded-lg">
                  <CreditCard className="w-6 h-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-slate-600">전체 대출</p>
                  <p className="text-2xl font-bold text-slate-900">{dashboardData.loan_count.toLocaleString()}</p>
                </div>
              </div>
            </Card>

            <Card className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-purple-50 rounded-lg">
                  <FileText className="w-6 h-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-slate-600">재대출 신청</p>
                  <p className="text-2xl font-bold text-slate-900">{dashboardData.refinance_count.toLocaleString()}</p>
                </div>
              </div>
            </Card>

            <Card className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-orange-50 rounded-lg">
                  <DollarSign className="w-6 h-6 text-orange-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-slate-600">총 부채액</p>
                  <p className="text-2xl font-bold text-slate-900">{Math.round(dashboardData.total_assets / 100000000)}억원</p>
                </div>
              </div>
            </Card>
          </div>
        )}

        {/* 탭 네비게이션 */}
        <div className="mb-6">
          <nav className="flex space-x-8 border-b border-slate-200">
            {[
              { id: 'overview', name: '고객 검색', icon: BarChart3 },
              { id: 'loans', name: '대출 관리', icon: CreditCard },
              { id: 'applications', name: '재대출 신청', icon: FileText },
              { id: 'recommendations', name: '상품 추천', icon: Star }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-accent-500 text-accent-600'
                      : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.name}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* 검색 및 액션 바 */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="검색어를 입력하세요..."
                value={searchTerm}
                onChange={(e) => handleSearch(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <div className="flex gap-2">
            <Button
              onClick={loadDashboardData}
              disabled={loading}
              className="flex items-center"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              검색
            </Button>
          </div>
        </div>

        {/* 에러 메시지 */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {/* 탭 컨텐츠 */}
        <div className="space-y-6">
          {/* 개요 탭 */}
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="p-6">
                <h3 className="text-lg font-semibold text-slate-900 mb-4">최근 고객</h3>
                <div className="space-y-3">
                  {customers.slice(0, 5).map((customer) => (
                    <div key={customer.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                      <div>
                        <p className="font-medium text-slate-900">{customer.name}</p>
                        <p className="text-sm text-slate-600">{customer.customer_id}</p>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleViewDetails('고객', customer.id)}
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              </Card>

              <Card className="p-6">
                <h3 className="text-lg font-semibold text-slate-900 mb-4">최근 대출</h3>
                <div className="space-y-3">
                  {loans.slice(0, 5).map((loan) => (
                    <div key={loan.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                      <div>
                        <p className="font-medium text-slate-900">{loan.loan_type}</p>
                        <p className="text-sm text-slate-600">{loan.loan_amount.toLocaleString()}원</p>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleViewDetails('대출', loan.id)}
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          )}

          {/* 대출 관리 탭 */}
          {activeTab === 'loans' && (
            <Card className="p-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">대출 목록</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-slate-200">
                  <thead className="bg-slate-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">대출번호</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">대출유형</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">대출금액</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">이자율</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">상태</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">액션</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-slate-200">
                    {loans.map((loan) => (
                      <tr key={loan.id}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">{loan.loan_number}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">{loan.loan_type}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{loan.loan_amount.toLocaleString()}원</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{loan.interest_rate}%</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{loan.status}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleViewDetails('대출', loan.id)}
                          >
                            <Eye className="w-4 h-4" />
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          )}

          {/* 재대출 신청 탭 */}
          {activeTab === 'applications' && (
            <Card className="p-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">재대출 신청 목록</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-slate-200">
                  <thead className="bg-slate-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">신청번호</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">신청금액</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">희망이자율</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">상태</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">신청일</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">액션</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-slate-200">
                    {applications.map((app) => (
                      <tr key={app.id}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">{app.application_number}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{app.requested_amount.toLocaleString()}원</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{app.requested_interest_rate}%</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{app.application_status}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{new Date(app.application_date).toLocaleDateString()}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleViewDetails('재대출신청', app.id)}
                          >
                            <Eye className="w-4 h-4" />
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          )}

          {/* 상품 추천 탭 */}
          {activeTab === 'recommendations' && (
            <Card className="p-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">상품 추천</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[1, 2, 3].map((i) => (
                  <Card key={i} className="p-4 border-2 border-dashed border-slate-200">
                    <div className="text-center">
                      <Star className="w-8 h-8 text-yellow-400 mx-auto mb-2" />
                      <h4 className="font-medium text-slate-900 mb-2">추천 상품 {i}</h4>
                      <p className="text-sm text-slate-600 mb-4">고객 맞춤형 재대출 상품</p>
                      <Button variant="outline" size="sm">
                        상세보기
                      </Button>
                    </div>
                  </Card>
                ))}
              </div>
            </Card>
          )}
        </div>
      </main>
    </div>
  );
}
