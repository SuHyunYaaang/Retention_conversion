'use client';

import React from 'react';
import { LoanData } from '@/types';
import { 
  User, 
  Phone, 
  Mail, 
  MapPin, 
  CreditCard, 
  Calendar, 
  DollarSign, 
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Clock,
  XCircle
} from 'lucide-react';

interface LoanDataCardProps {
  data: LoanData;
  onViewDetails?: (data: LoanData) => void;
}

const LoanDataCard: React.FC<LoanDataCardProps> = ({ data, onViewDetails }) => {
  // 상태별 아이콘과 색상
  const getStatusInfo = (status: string) => {
    switch (status) {
      case '완료':
        return { icon: CheckCircle, color: 'text-green-600', bgColor: 'bg-green-50' };
      case '상환중':
        return { icon: TrendingUp, color: 'text-blue-600', bgColor: 'bg-blue-50' };
      case '연체':
        return { icon: AlertCircle, color: 'text-red-600', bgColor: 'bg-red-50' };
      case '승인':
        return { icon: CheckCircle, color: 'text-green-600', bgColor: 'bg-green-50' };
      case '심사중':
        return { icon: Clock, color: 'text-yellow-600', bgColor: 'bg-yellow-50' };
      case '신청':
        return { icon: Clock, color: 'text-gray-600', bgColor: 'bg-gray-50' };
      case '거절':
        return { icon: XCircle, color: 'text-red-600', bgColor: 'bg-red-50' };
      default:
        return { icon: Clock, color: 'text-gray-600', bgColor: 'bg-gray-50' };
    }
  };

  const statusInfo = getStatusInfo(data.status);
  const StatusIcon = statusInfo.icon;

  // 금액 포맷팅
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('ko-KR').format(amount);
  };

  // 날짜 포맷팅
  const formatDate = (dateString: string | null) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('ko-KR');
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">
      {/* 헤더 */}
      <div className="p-4 border-b border-gray-100">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold text-gray-900">{data.name}</h3>
          <div className={`flex items-center px-2 py-1 rounded-full text-sm font-medium ${statusInfo.bgColor} ${statusInfo.color}`}>
            <StatusIcon className="w-4 h-4 mr-1" />
            {data.status}
          </div>
        </div>
        <div className="flex items-center text-sm text-gray-600">
          <User className="w-4 h-4 mr-1" />
          {data.customer_id} • {data.age}세 • {data.job_type}
        </div>
      </div>

      {/* 고객 정보 */}
      <div className="p-4 border-b border-gray-100">
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="flex items-center text-gray-600">
            <Phone className="w-4 h-4 mr-2 text-gray-400" />
            {data.phone}
          </div>
          <div className="flex items-center text-gray-600">
            <Mail className="w-4 h-4 mr-2 text-gray-400" />
            {data.email}
          </div>
          <div className="flex items-center text-gray-600">
            <MapPin className="w-4 h-4 mr-2 text-gray-400" />
            <span className="truncate">{data.address}</span>
          </div>
          <div className="flex items-center text-gray-600">
            <CreditCard className="w-4 h-4 mr-2 text-gray-400" />
            신용등급: {data.credit_grade}
          </div>
        </div>
      </div>

      {/* 대출 정보 */}
      <div className="p-4 border-b border-gray-100">
        <div className="mb-3">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-medium text-gray-900">{data.loan_type}</h4>
            <span className="text-sm text-gray-500">{data.loan_id}</span>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <div className="text-sm text-gray-600">대출금액</div>
              <div className="text-lg font-semibold text-gray-900">
                {formatCurrency(data.loan_amount)}원
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">월상환금</div>
              <div className="text-lg font-semibold text-gray-900">
                {formatCurrency(data.monthly_payment)}원
              </div>
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-3 gap-3 text-sm">
          <div>
            <div className="text-gray-600">대출기간</div>
            <div className="font-medium">{data.loan_term}개월</div>
          </div>
          <div>
            <div className="text-gray-600">이자율</div>
            <div className="font-medium">{data.interest_rate}%</div>
          </div>
          <div>
            <div className="text-gray-600">소득수준</div>
            <div className="font-medium">{data.income_level}</div>
          </div>
        </div>
      </div>

      {/* 날짜 정보 */}
      <div className="p-4 border-b border-gray-100">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <div className="text-gray-600">신청일</div>
            <div className="font-medium">{formatDate(data.application_date)}</div>
          </div>
          <div>
            <div className="text-gray-600">승인일</div>
            <div className="font-medium">{formatDate(data.approval_date)}</div>
          </div>
          {data.disbursement_date && (
            <div>
              <div className="text-gray-600">대출실행일</div>
              <div className="font-medium">{formatDate(data.disbursement_date)}</div>
            </div>
          )}
          {data.overdue_days > 0 && (
            <div>
              <div className="text-gray-600">연체일수</div>
              <div className="font-medium text-red-600">{data.overdue_days}일</div>
            </div>
          )}
        </div>
      </div>

      {/* 액션 버튼 */}
      <div className="p-4">
        <button
          onClick={() => onViewDetails?.(data)}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors duration-200 text-sm font-medium"
        >
          상세보기
        </button>
      </div>
    </div>
  );
};

export default LoanDataCard;