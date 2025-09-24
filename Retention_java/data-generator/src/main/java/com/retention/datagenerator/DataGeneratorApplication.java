package com.retention.datagenerator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * 재대출 자동화 서비스 데이터 생성기 애플리케이션
 * 
 * 주요 기능:
 * - 고객 데이터 생성
 * - 대출 데이터 생성
 * - 재대출 신청 데이터 생성
 * - 상품 데이터 생성
 * - CSV 파일 생성
 */
@SpringBootApplication
@EnableAsync
public class DataGeneratorApplication {

    public static void main(String[] args) {
        SpringApplication.run(DataGeneratorApplication.class, args);
    }
}

