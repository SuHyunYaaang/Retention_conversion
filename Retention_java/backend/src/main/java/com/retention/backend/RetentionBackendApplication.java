package com.retention.backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

/**
 * 재대출 자동화 서비스 백엔드 애플리케이션
 * 
 * 주요 기능:
 * - 고객 관리
 * - 대출 관리
 * - 재대출 신청 처리
 * - 상품 관리
 * - 문서 관리
 * - ML 예측 데이터 제공
 */
@SpringBootApplication
@EnableJpaAuditing
public class RetentionBackendApplication {

    public static void main(String[] args) {
        SpringApplication.run(RetentionBackendApplication.class, args);
    }
}

