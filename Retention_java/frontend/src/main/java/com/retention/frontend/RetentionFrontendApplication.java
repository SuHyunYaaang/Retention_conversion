package com.retention.frontend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * 재대출 자동화 서비스 프론트엔드 애플리케이션
 * 
 * 주요 기능:
 * - 웹 대시보드
 * - 고객 관리 UI
 * - 대출 관리 UI
 * - 재대출 신청 UI
 * - ML 대시보드
 */
@SpringBootApplication
@EnableAsync
public class RetentionFrontendApplication {

    public static void main(String[] args) {
        SpringApplication.run(RetentionFrontendApplication.class, args);
    }
}

