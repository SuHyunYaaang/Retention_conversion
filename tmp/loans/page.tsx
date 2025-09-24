'use client';

import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  DollarSign, 
  CreditCard, 
  Target, 
  BarChart3, 
  Users,
  Calculator,
  Lightbulb,
  AlertTriangle,
  CheckCircle,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react';
import { 
  CustomerFinancialProfile, 
  LoanSimulationScenario, 
  SimulationResult,
  SimulationRequest 
} from '@/types';
import { handleAPIError } from '@/lib/api';
import Header from '@/components/Header';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function LoansPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCustomerId, setSelectedCustomerId] = useState<string>('CUST001');
  const [customerProfile, setCustomerProfile] = useState<CustomerFinancialProfile | null>(null);
  const [simulations, setSimulations] = useState<SimulationResult[]>([]);
  const [defaultScenarios, setDefaultScenarios] = useState<LoanSimulationScenario[]>([]);
  const [aiRecommendations, setAiRecommendations] = useState<string[]>([]);

  // 샘플 고객 데이터 (실제로는 API에서 가져올 예정)
  const sampleCustomers = [
    { id: 'CUST001', name: '김철수', current_limit: 70000000 },

  ];

  // 기본 시나리오 데이터
  const defaultScenarioData: LoanSimulationScenario[] = [
    {
      id: 'scenario1',
      name: '소득 증가 시나리오',
      description: '연봉 10% 증가 시 대출 한도 변화',
      income_change: 10,
      debt_change: 0,
      credit_score_change: 20,
      interest_rate_change: 0,
      expected_loan_limit: 82000000,
      probability: 75,
      timeframe: 12
    },
    {
      id: 'scenario2',
      name: '부채 감소 시나리오',
      description: '카드빚 2000만원 상환 완료 시',
      income_change: 0,
      debt_change: -15,
      credit_score_change: 30,
      interest_rate_change: 0,
      expected_loan_limit: 95000000,
      probability: 60,
      timeframe: 6
    },
    {
      id: 'scenario3',
      name: '금리 하락 시나리오',
      description: '시장 금리 1% 하락 시',
      income_change: 0,
      debt_change: 0,
      credit_score_change: 0,
      interest_rate_change: -1,
      expected_loan_limit: 105000000,
      probability: 40,
      timeframe: 18
    },
    {
      id: 'scenario4',
      name: '최적 시나리오',
      description: '모든 조건 개선 시',
      income_change: 10,
      debt_change: -15,
      credit_score_change: 50,
      interest_rate_change: -1,
      expected_loan_limit: 120000000,
      probability: 25,
      timeframe: 12
    }
  ];

  // 샘플 고객 프로필
  const sampleProfile: CustomerFinancialProfile = {
    customer_id: 'CUST001',
    name: '김철수',
    current_income: 50000000,
    current_debt: 30000000,
    current_credit_score: 780,
    current_loan_limit: 70000000,
    current_interest_rate: 5.2,
    monthly_expenses: 2500000,
    savings_rate: 15,
    risk_level: 'medium'
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      setError(null);

      // 실제 API 호출 대신 샘플 데이터 사용
      setCustomerProfile(sampleProfile);
      setDefaultScenarios(defaultScenarioData);
      
      // 시뮬레이션 실행
      await runSimulations();
      
      // AI 추천 생성
      generateAIRecommendations();
      
    } catch (err) {
      const errorMessage = handleAPIError(err);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const runSimulations = async () => {
    try {
      const simulationResults: SimulationResult[] = defaultScenarioData.map(scenario => {
        const improvement = scenario.expected_loan_limit - sampleProfile.current_loan_limit;
        const improvementPercent = (improvement / sampleProfile.current_loan_limit) * 100;
        
        return {
          scenario,
          current_limit: sampleProfile.current_loan_limit,
          projected_limit: scenario.expected_loan_limit,
          improvement_amount: improvement,
          improvement_percentage: improvementPercent,
          recommended_actions: generateRecommendedActions(scenario),
          risk_factors: generateRiskFactors(scenario)
        };
      });

      setSimulations(simulationResults);
    } catch (err) {
      console.error('시뮬레이션 실행 중 오류:', err);
    }
  };

  const generateRecommendedActions = (scenario: LoanSimulationScenario): string[] => {
    const actions: string[] = [];
    
    if (scenario.income_change > 0) {
      actions.push('추가 수입원 개발 (부업, 투자 등)');
      actions.push('연봉 협상 준비');
    }
    
    if (scenario.debt_change < 0) {
      actions.push('고금리 부채 우선 상환');
      actions.push('카드 사용량 줄이기');
    }
    
    if (scenario.credit_score_change > 0) {
      actions.push('신용카드 한도 내 사용');
      actions.push('정기적인 신용점수 확인');
    }
    
    return actions;
  };

  const generateRiskFactors = (scenario: LoanSimulationScenario): string[] => {
    const risks: string[] = [];
    
    if (scenario.probability < 50) {
      risks.push('시장 환경 변화 가능성');
    }
    
    if (scenario.timeframe > 12) {
      risks.push('장기적 불확실성');
    }
    
    if (scenario.income_change > 15) {
      risks.push('소득 증가 지속성 불확실');
    }
    
    return risks;
  };

  const generateAIRecommendations = () => {
    const recommendations = [
      '다음 6개월간 부채를 2,000만원 줄이면 금리가 0.3% 낮아지고, 한도가 1,000만원 증가할 것으로 예상됩니다.',
      '신용점수를 30점 올리면 대출 한도가 평균 15% 증가할 가능성이 높습니다.',
      '월 저축률을 현재 15%에서 20%로 높이면 1년 후 대출 한도가 20% 증가할 것으로 예측됩니다.',
      '고금리 부채를 우선적으로 상환하는 것이 가장 효과적인 한도 개선 방법입니다.'
    ];
    
    setAiRecommendations(recommendations);
  };

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('ko-KR').format(amount);
  };

  const getRiskLevelColor = (level: string): string => {
    switch (level) {
      case 'low': return 'text-green-600 bg-green-50';
      case 'medium': return 'text-yellow-600 bg-yellow-50';
      case 'high': return 'text-red-600 bg-red-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <LoadingSpinner size="lg" message="대출 시뮬레이션을 준비하는 중..." />
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
            미래 대출 한도 시뮬레이션
          </h1>
          <p className="text-slate-600">
            AI가 예측하는 미래 대출 한도와 개선 방안을 확인하세요
          </p>
        </div>

        {/* 에러 메시지 */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {/* 고객 선택 */}
        <div className="mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">고객 선택</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {sampleCustomers.map((customer) => (
                <button
                  key={customer.id}
                  onClick={() => setSelectedCustomerId(customer.id)}
                  className={`p-4 rounded-lg border-2 transition-colors ${
                    selectedCustomerId === customer.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="text-left">
                    <p className="font-medium text-slate-900">{customer.name}</p>
                    <p className="text-sm text-slate-600">현재 한도: {formatCurrency(customer.current_limit)}원</p>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* 고객 프로필 */}
        {customerProfile && (
          <div className="mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4">현재 재무 현황</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                    <DollarSign className="w-6 h-6 text-blue-600" />
                  </div>
                  <p className="text-sm text-slate-600">연소득</p>
                  <p className="text-lg font-semibold text-slate-900">{formatCurrency(customerProfile.current_income)}원</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                    <CreditCard className="w-6 h-6 text-red-600" />
                  </div>
                  <p className="text-sm text-slate-600">총 부채</p>
                  <p className="text-lg font-semibold text-slate-900">{formatCurrency(customerProfile.current_debt)}원</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                    <Target className="w-6 h-6 text-green-600" />
                  </div>
                  <p className="text-sm text-slate-600">신용점수</p>
                  <p className="text-lg font-semibold text-slate-900">{customerProfile.current_credit_score}점</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                    <BarChart3 className="w-6 h-6 text-purple-600" />
                  </div>
                  <p className="text-sm text-slate-600">현재 대출 한도</p>
                  <p className="text-lg font-semibold text-slate-900">{formatCurrency(customerProfile.current_loan_limit)}원</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 시뮬레이션 결과 */}
        <div className="mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">시뮬레이션 결과</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {simulations.map((simulation) => (
                <div key={simulation.scenario.id} className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-medium text-slate-900">{simulation.scenario.name}</h3>
                    <span className="text-sm text-slate-500">{simulation.scenario.probability}% 확률</span>
                  </div>
                  
                  <p className="text-sm text-slate-600 mb-4">{simulation.scenario.description}</p>
                  
                  <div className="space-y-3 mb-4">
                    <div className="flex justify-between">
                      <span className="text-sm text-slate-600">현재 한도:</span>
                      <span className="text-sm font-medium">{formatCurrency(simulation.current_limit)}원</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-slate-600">예상 한도:</span>
                      <span className="text-sm font-medium text-green-600">{formatCurrency(simulation.projected_limit)}원</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-slate-600">개선 금액:</span>
                      <span className="text-sm font-medium text-blue-600">
                        +{formatCurrency(simulation.improvement_amount)}원 ({simulation.improvement_percentage.toFixed(1)}%)
                      </span>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <h4 className="text-sm font-medium text-slate-900">권장 행동:</h4>
                    <ul className="text-sm text-slate-600 space-y-1">
                      {simulation.recommended_actions.map((action, index) => (
                        <li key={index} className="flex items-center">
                          <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                          {action}
                        </li>
                      ))}
                    </ul>
                  </div>
                  
                  {simulation.risk_factors.length > 0 && (
                    <div className="mt-4 space-y-2">
                      <h4 className="text-sm font-medium text-slate-900">주의사항:</h4>
                      <ul className="text-sm text-slate-600 space-y-1">
                        {simulation.risk_factors.map((risk, index) => (
                          <li key={index} className="flex items-center">
                            <AlertTriangle className="w-4 h-4 text-yellow-500 mr-2" />
                            {risk}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* AI 추천 */}
        <div className="mb-8">
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg shadow p-6">
            <div className="flex items-center mb-4">
              <Lightbulb className="w-6 h-6 text-blue-600 mr-2" />
              <h2 className="text-lg font-semibold text-slate-900">AI 추천</h2>
            </div>
            <div className="space-y-3">
              {aiRecommendations.map((recommendation, index) => (
                <div key={index} className="flex items-start">
                  <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <p className="text-slate-700">{recommendation}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* 액션 버튼 */}
        <div className="flex justify-center">
          <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors flex items-center">
            <Calculator className="w-5 h-5 mr-2" />
            상세 시뮬레이션 실행
          </button>
        </div>
      </main>
    </div>
  );
}
