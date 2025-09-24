package com.retention.ml;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * 재대출 자동화 서비스 머신러닝 서비스 애플리케이션
 * 
 * 주요 기능:
 * - GA(Genetic Algorithm) 기반 하이퍼파라미터 최적화
 * - XGBoost 모델 학습 및 예측
 * - SHAP 기반 모델 해석
 * - 다양한 성능 지표 평가
 * - 자동 리포트 생성
 */
@SpringBootApplication
@EnableAsync
@EnableScheduling
public class RetentionMlServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(RetentionMlServiceApplication.class, args);
    }
}

