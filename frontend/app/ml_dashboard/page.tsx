'use client';

import React, { useState, useEffect } from 'react';
import { 
  Search, 
  RefreshCw, 
  Users, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle, 
  Activity,
  BarChart3,
  PieChart,
  Filter,
  Download,
  Eye,
  Brain,
  Target,
  Zap
} from 'lucide-react';
import Header from '@/components/Header';
import LoadingSpinner from '@/components/LoadingSpinner';

// 동적 렌더링 강제
export const dynamic = 'force-dynamic';
export const revalidate = 0;

// ML 예측 데이터 타입
interface MLPrediction {
  id: number;
  customer_id: string;
  age: number;
  income_level: string;
  credit_grade: string;
  loan_amount: number;
  interest_rate: number;
  loan_term: number;
  monthly_payment: number;
  payment_history_months: number;
  late_payments_3m: number;
  late_payments_6m: number;
  late_payments_12m: number;
  credit_utilization: number;
  debt_to_income_ratio: number;
  employment_length_years: number;
  number_of_accounts: number;
  inquiries_last_6m: number;
  everdelinquent: number;
  created_at: string;
}

// ML 통계 타입
interface MLStats {
  total_predictions: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  avg_churn_probability: number;
  avg_age: number;
  avg_credit_utilization: number;
  avg_debt_to_income_ratio: number;
  delinquency_rate: number;
}

// 위험도별 색상 및 스타일
const RISK_STYLES = {
  high: {
    color: 'text-red-600',
    bgColor: 'bg-red-50',
    borderColor: 'border-red-200',
    icon: AlertTriangle,
    label: '고위험',
    description: '이탈 가능성이 높음'
  },
  medium: {
    color: 'text-yellow-600',
    bgColor: 'bg-yellow-50',
    borderColor: 'border-yellow-200',
    icon: Activity,
    label: '중위험',
    description: '주의가 필요함'
  },
  low: {
    color: 'text-green-600',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200',
    icon: CheckCircle,
    label: '저위험',
    description: '안정적인 고객'
  }
};

export default function MLDashboardPage() {
  const [mlData, setMlData] = useState<MLPrediction[]>([]);
  const [stats, setStats] = useState<MLStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [riskFilter, setRiskFilter] = useState<'all' | 'high' | 'medium' | 'low'>('all');
  const [ageFilter, setAgeFilter] = useState<'all' | 'young' | 'middle' | 'senior'>('all');
  const [creditFilter, setCreditFilter] = useState<'all' | 'A' | 'B' | 'C' | 'D'>('all');
  const [sortBy, setSortBy] = useState<'risk' | 'age' | 'credit' | 'amount'>('risk');

  // 데이터 로드
  const loadMLData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch('/api/ml_dashboard');
      if (!response.ok) {
        throw new Error('ML 예측 데이터를 가져올 수 없습니다.');
      }
      
      const data = await response.json();
      setMlData(data);
      calculateStats(data);
    } catch (err) {
      setError('데이터를 불러오는 중 오류가 발생했습니다.');
      console.error('ML 데이터 로드 오류:', err);
    } finally {
      setLoading(false);
    }
  };

  // 통계 계산
  const calculateStats = (data: MLPrediction[]) => {
    const total = data.length;
    const highRisk = data.filter(item => getRiskLevel(item) === 'high').length;
    const mediumRisk = data.filter(item => getRiskLevel(item) === 'medium').length;
    const lowRisk = data.filter(item => getRiskLevel(item) === 'low').length;
    
    const avgAge = data.reduce((sum, item) => sum + item.age, 0) / total;
    const avgCreditUtil = data.reduce((sum, item) => sum + item.credit_utilization, 0) / total;
    const avgDebtRatio = data.reduce((sum, item) => sum + item.debt_to_income_ratio, 0) / total;
    const delinquencyRate = data.filter(item => item.everdelinquent === 1).length / total;
    const avgChurnProb = data.reduce((sum, item) => sum + (item.everdelinquent === 1 ? 0.8 : 0.2), 0) / total;

    setStats({
      total_predictions: total,
      high_risk_count: highRisk,
      medium_risk_count: mediumRisk,
      low_risk_count: lowRisk,
      avg_churn_probability: avgChurnProb,
      avg_age: avgAge,
      avg_credit_utilization: avgCreditUtil,
      avg_debt_to_income_ratio: avgDebtRatio,
      delinquency_rate: delinquencyRate
    });
  };

  // 위험도 레벨 계산
  const getRiskLevel = (item: MLPrediction): 'low' | 'medium' | 'high' => {
    if (item.everdelinquent === 1) return 'high';
    
    const delinquencyScore = (item.late_payments_3m * 3 + item.late_payments_6m * 2 + item.late_payments_12m) / 10;
    const creditScore = 1 - (item.credit_utilization * 0.3 + item.debt_to_income_ratio * 0.3 + delinquencyScore * 0.4);
    
    if (creditScore > 0.7) return 'low';
    if (creditScore > 0.4) return 'medium';
    return 'high';
  };

  // 나이 그룹 계산
  const getAgeGroup = (age: number): 'young' | 'middle' | 'senior' => {
    if (age < 35) return 'young';
    if (age < 55) return 'middle';
    return 'senior';
  };

  // 필터링된 데이터
  const filteredData = mlData.filter(item => {
    const matchesSearch = 
      item.customer_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.income_level.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesRisk = riskFilter === 'all' || getRiskLevel(item) === riskFilter;
    const matchesAge = ageFilter === 'all' || getAgeGroup(item.age) === ageFilter;
    const matchesCredit = creditFilter === 'all' || item.credit_grade.startsWith(creditFilter);
    
    return matchesSearch && matchesRisk && matchesAge && matchesCredit;
  });

  // 정렬된 데이터
  const sortedData = [...filteredData].sort((a, b) => {
    switch (sortBy) {
      case 'risk':
        const riskOrder = { high: 3, medium: 2, low: 1 };
        return riskOrder[getRiskLevel(b)] - riskOrder[getRiskLevel(a)];
      case 'age':
        return b.age - a.age;
      case 'credit':
        return a.credit_grade.localeCompare(b.credit_grade);
      case 'amount':
        return b.loan_amount - a.loan_amount;
      default:
        return 0;
    }
  });

  // CSV 다운로드
  const downloadCSV = () => {
    const headers = [
      '고객ID', '나이', '소득수준', '신용등급', '대출금액', '이자율', '대출기간',
      '월상환금', '상환이력(개월)', '연체횟수(3개월)', '연체횟수(6개월)', '연체횟수(12개월)',
      '신용이용률', '부채비율', '근무연수', '계좌수', '신용조회(6개월)', '이탈여부', '위험도'
    ];
    
    const csvContent = [
      headers.join(','),
      ...sortedData.map(item => [
        item.customer_id,
        item.age,
        item.income_level,
        item.credit_grade,
        item.loan_amount,
        item.interest_rate,
        item.loan_term,
        item.monthly_payment,
        item.payment_history_months,
        item.late_payments_3m,
        item.late_payments_6m,
        item.late_payments_12m,
        item.credit_utilization,
        item.debt_to_income_ratio,
        item.employment_length_years,
        item.number_of_accounts,
        item.inquiries_last_6m,
        item.everdelinquent === 1 ? '이탈' : '유지',
        RISK_STYLES[getRiskLevel(item)].label
      ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `ml_dashboard_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  };

  useEffect(() => {
    loadMLData();
  }, []);

  if (loading && mlData.length === 0) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <LoadingSpinner size="lg" message="머신러닝 데이터를 불러오는 중..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 페이지 헤더 */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Brain className="w-8 h-8 text-purple-600" />
            <h1 className="text-3xl font-bold text-slate-900">
              머신러닝 대시보드
            </h1>
          </div>
          <p className="text-slate-600">
            머신러닝 기반 고객 이탈 예측결과를 조회할 수 있습니다
          </p>
        </div>

        {/* 통계 카드 */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">전체 예측</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total_predictions.toLocaleString()}</p>
                </div>
                <div className="p-2 bg-blue-50 rounded-lg">
                  <Target className="w-6 h-6 text-blue-600" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">고위험 고객</p>
                  <p className="text-2xl font-bold text-red-600">{stats.high_risk_count.toLocaleString()}</p>
                  <p className="text-xs text-gray-500">
                    {((stats.high_risk_count / stats.total_predictions) * 100).toFixed(1)}%
                  </p>
                </div>
                <div className="p-2 bg-red-50 rounded-lg">
                  <AlertTriangle className="w-6 h-6 text-red-600" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">평균 이탈 확률</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {(stats.avg_churn_probability * 100).toFixed(1)}%
                  </p>
                </div>
                <div className="p-2 bg-orange-50 rounded-lg">
                  <TrendingUp className="w-6 h-6 text-orange-600" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">연체율</p>
                  <p className="text-2xl font-bold text-purple-600">
                    {(stats.delinquency_rate * 100).toFixed(1)}%
                  </p>
                </div>
                <div className="p-2 bg-purple-50 rounded-lg">
                  <Zap className="w-6 h-6 text-purple-600" />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 필터 및 검색 바 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            {/* 검색 */}
            <div className="lg:col-span-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="고객 ID, 소득수준으로 검색..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* 위험도 필터 */}
            <div>
              <select
                value={riskFilter}
                onChange={(e) => setRiskFilter(e.target.value as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">전체 위험도</option>
                <option value="high">고위험</option>
                <option value="medium">중위험</option>
                <option value="low">저위험</option>
              </select>
            </div>

            {/* 나이 필터 */}
            <div>
              <select
                value={ageFilter}
                onChange={(e) => setAgeFilter(e.target.value as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">전체 연령</option>
                <option value="young">청년 (35세 미만)</option>
                <option value="middle">중년 (35-55세)</option>
                <option value="senior">고령 (55세 이상)</option>
              </select>
            </div>

            {/* 신용등급 필터 */}
            <div>
              <select
                value={creditFilter}
                onChange={(e) => setCreditFilter(e.target.value as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">전체 등급</option>
                <option value="A">A등급</option>
                <option value="B">B등급</option>
                <option value="C">C등급</option>
                <option value="D">D등급</option>
              </select>
            </div>
          </div>

          <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-200">
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">정렬:</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="risk">위험도순</option>
                <option value="age">나이순</option>
                <option value="credit">신용등급순</option>
                <option value="amount">대출금액순</option>
              </select>
            </div>

            <div className="flex gap-2">
              <button
                onClick={loadMLData}
                disabled={loading}
                className="flex items-center px-3 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
              >
                <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                새로고침
              </button>
              <button
                onClick={downloadCSV}
                className="flex items-center px-3 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700"
              >
                <Download className="w-4 h-4 mr-2" />
                CSV 다운로드
              </button>
            </div>
          </div>
        </div>

        {/* 에러 메시지 */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {/* 데이터 테이블 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">예측 결과 상세</h3>
            <p className="text-sm text-gray-600">
              총 {sortedData.length}건의 예측 데이터
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    고객 정보
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    대출 정보
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    신용 정보
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    위험도
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    액션
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {sortedData.map((item) => {
                  const riskLevel = getRiskLevel(item);
                  const riskStyle = RISK_STYLES[riskLevel];
                  const RiskIcon = riskStyle.icon;
                  
                  return (
                    <tr key={item.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {item.customer_id}
                          </div>
                          <div className="text-sm text-gray-500">
                            {item.age}세 • {item.income_level}
                          </div>
                          <div className="text-sm text-gray-500">
                            신용등급: {item.credit_grade}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="text-sm text-gray-900">
                            {item.loan_amount.toLocaleString()}원
                          </div>
                          <div className="text-sm text-gray-500">
                            {item.interest_rate}% • {item.loan_term}개월
                          </div>
                          <div className="text-sm text-gray-500">
                            월 {item.monthly_payment.toLocaleString()}원
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="text-sm text-gray-900">
                            연체: {item.late_payments_12m}회
                          </div>
                          <div className="text-sm text-gray-500">
                            신용이용률: {(item.credit_utilization * 100).toFixed(1)}%
                          </div>
                          <div className="text-sm text-gray-500">
                            부채비율: {(item.debt_to_income_ratio * 100).toFixed(1)}%
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${riskStyle.bgColor} ${riskStyle.color}`}>
                          <RiskIcon className="w-3 h-3 mr-1" />
                          {riskStyle.label}
                        </div>
                        <div className="text-xs text-gray-500 mt-1">
                          이탈확률: {item.everdelinquent === 1 ? '80%' : '20%'}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button className="text-blue-600 hover:text-blue-900 flex items-center">
                          <Eye className="w-4 h-4 mr-1" />
                          상세보기
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {sortedData.length === 0 && (
            <div className="text-center py-12">
              <Brain className="w-12 h-12 text-slate-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-slate-900 mb-2">
                검색 결과가 없습니다
              </h3>
              <p className="text-slate-600">
                다른 검색어나 필터를 시도해보세요
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}



