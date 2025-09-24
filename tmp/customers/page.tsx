'use client';

import React, { useState, useEffect } from 'react';
import { Search, RefreshCw, Users, CreditCard, TrendingUp, DollarSign } from 'lucide-react';
import { LoanData, LoanStats } from '@/types';
import { postgrestAPI, handlePostgRESTError } from '@/lib/postgrest';
import Header from '@/components/Header';
import LoanDataCard from '@/components/LoanDataCard';
import StatsCard from '@/components/StatsCard';
import Pagination from '@/components/Pagination';
import LoadingSpinner from '@/components/LoadingSpinner';

// 동적 렌더링 강제
export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default function HomePage() {
  const [loanData, setLoanData] = useState<LoanData[]>([]);
  const [stats, setStats] = useState<LoanStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');

  // 데이터 로드
  const loadData = async (page: number = 1) => {
    try {
      setLoading(true);
      setError(null);
      
      // PostgREST에서 대출 데이터와 고객 데이터를 병렬로 로드
      const [loansResponse, customersResponse] = await Promise.all([
        postgrestAPI.loans.get({ limit: 50, offset: (page - 1) * 50 }),
        postgrestAPI.customers.get({ limit: 1000 })
      ]);

      // 대출 데이터와 고객 데이터를 조합하여 LoanData 형태로 변환
      const combinedData: LoanData[] = loansResponse.map((loan: any) => {
        const customer = customersResponse.find((c: any) => c.id === loan.customer_id);
        return {
          id: loan.id,
          customer_id: customer?.customer_id || `CUST${loan.customer_id}`,
          name: customer?.name || `고객${loan.customer_id}`,
          loan_id: loan.id,
          loan_type: loan.loan_type || '개인신용대출',
          loan_amount: loan.loan_amount || 0,
          interest_rate: loan.interest_rate || 0,
          loan_term: loan.loan_term || 12,
          monthly_payment: loan.monthly_payment || 0,
          status: loan.status || '상환중',
          application_date: loan.created_at || new Date().toISOString(),
          approval_date: loan.approval_date || new Date().toISOString(),
          phone: customer?.phone || '',
          email: customer?.email || ''
        };
      });

      setLoanData(combinedData);
      
      // 통계 계산
      const stats: LoanStats = {
        total_customers: customersResponse.length,
        total_loans: loansResponse.length,
        avg_loan_amount: loansResponse.reduce((sum: number, loan: any) => sum + (loan.loan_amount || 0), 0) / loansResponse.length || 0,
        status_stats: {
          '상환중': loansResponse.filter((loan: any) => loan.status === '상환중').length,
          '완료': loansResponse.filter((loan: any) => loan.status === '완료').length,
          '연체': loansResponse.filter((loan: any) => loan.status === '연체').length
        },
        loan_type_stats: {
          '개인신용대출': loansResponse.filter((loan: any) => loan.loan_type === '개인신용대출').length,
          '담보대출': loansResponse.filter((loan: any) => loan.loan_type === '담보대출').length,
          '기타': loansResponse.filter((loan: any) => !['개인신용대출', '담보대출'].includes(loan.loan_type)).length
        }
      };
      
      setStats(stats);
      setTotalPages(Math.ceil(loansResponse.length / 50));
      setCurrentPage(page);
    } catch (err) {
      const errorMessage = handlePostgRESTError(err);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // 검색 필터링
  const handleSearch = (term: string) => {
    setSearchTerm(term);
    // 실제 검색 기능은 백엔드에서 구현 필요
    // 현재는 클라이언트 사이드 필터링
  };

  // 페이지 변경
  const handlePageChange = (page: number) => {
    loadData(page);
  };

  // 상세보기 핸들러
  const handleViewDetails = (data: LoanData) => {
    // TODO: 상세보기 모달 또는 페이지로 이동
    console.log('View details:', data);
    alert(`${data.name}님의 대출 상세 정보를 확인합니다.`);
  };

  useEffect(() => {
    loadData();
  }, []);

  // 검색된 데이터 필터링
  const filteredData = loanData.filter(data =>
    data.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    data.customer_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
    data.loan_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
    data.status.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading && loanData.length === 0) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <LoadingSpinner size="lg" message="대출 데이터를 불러오는 중..." />
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
            고객 마이데이터
          </h1>
          <p className="text-slate-600">
            고객의 마이데이터를 전체 조회할 수 있습니다
          </p>
        </div>

        {/* 통계 카드 */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <StatsCard
              title="전체 고객"
              value={stats.total_customers.toLocaleString()}
              icon={Users}
              color="text-blue-600"
              bgColor="bg-blue-50"
            />
            <StatsCard
              title="전체 대출"
              value={stats.total_loans.toLocaleString()}
              icon={CreditCard}
              color="text-green-600"
              bgColor="bg-green-50"
            />
            <StatsCard
              title="평균 대출금액"
              value={`${Math.round(stats.avg_loan_amount / 10000)}만원`}
              icon={DollarSign}
              color="text-purple-600"
              bgColor="bg-purple-50"
            />
            <StatsCard
              title="상환중 대출"
              value={stats.status_stats['상환중'] || 0}
              icon={TrendingUp}
              color="text-orange-600"
              bgColor="bg-orange-50"
            />
          </div>
        )}

        {/* 검색 및 액션 바 */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="고객명, ID, 대출유형, 상태로 검색..."
                value={searchTerm}
                onChange={(e) => handleSearch(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => loadData(currentPage)}
              disabled={loading}
              className="flex items-center px-4 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              새로고침
            </button>
          </div>
        </div>

        {/* 에러 메시지 */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {/* 대출 데이터 카드 그리드 */}
        <div className="space-y-6">
          {loading ? (
            <div className="flex justify-center py-12">
              <LoadingSpinner size="lg" message="데이터를 불러오는 중..." />
            </div>
          ) : filteredData.length === 0 ? (
            <div className="text-center py-12">
              <CreditCard className="w-12 h-12 text-slate-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-slate-900 mb-2">
                {searchTerm ? '검색 결과가 없습니다' : '대출 데이터가 없습니다'}
              </h3>
              <p className="text-slate-600">
                {searchTerm 
                  ? '다른 검색어를 시도해보세요'
                  : '데이터 생성기를 실행하여 대출 데이터를 생성하세요'
                }
              </p>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredData.map((data) => (
                  <LoanDataCard
                    key={`${data.customer_id}-${data.loan_id}`}
                    data={data}
                    onViewDetails={handleViewDetails}
                  />
                ))}
              </div>

              {/* 페이지네이션 */}
              {totalPages > 1 && (
                <Pagination
                  currentPage={currentPage}
                  totalPages={totalPages}
                  onPageChange={handlePageChange}
                />
              )}

              {/* 결과 카운트 */}
              <div className="text-center text-sm text-slate-500">
                총 {filteredData.length}건의 대출 데이터가 있습니다
                {searchTerm && ` (검색어: "${searchTerm}")`}
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  );
}
