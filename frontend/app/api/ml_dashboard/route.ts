import { NextResponse } from 'next/server';

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

// GET 요청 처리
export async function GET() {
  try {
    // 백엔드 API에서 ML 예측 데이터 가져오기 (customers 스키마 기반)
    const response = await fetch('http://backend:8000/api/ml_dashboard', {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('ML 예측 데이터를 가져올 수 없습니다.');
    }

    const data = await response.json();
    
    return NextResponse.json(data);
  } catch (error) {
    console.error('ML 예측 데이터 로드 오류:', error);
    return NextResponse.json({ error: 'ML 예측 데이터를 가져올 수 없습니다.' }, { status: 500 });
  }
}

