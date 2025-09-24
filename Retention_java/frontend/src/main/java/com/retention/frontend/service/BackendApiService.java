package com.retention.frontend.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.Duration;
import java.util.Map;

/**
 * 백엔드 API 서비스
 * Next.js의 lib/api.ts와 동일한 기능을 제공
 */
@Service
public class BackendApiService {
    
    @Value("${api.backend.base-url}")
    private String backendBaseUrl;
    
    @Value("${api.backend.timeout}")
    private int timeout;
    
    private final WebClient webClient;
    
    @Autowired
    public BackendApiService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder
                .baseUrl(backendBaseUrl)
                .build();
    }
    
    /**
     * 대시보드 데이터 조회
     */
    public Map<String, Object> getDashboardData() {
        return webClient.get()
                .uri("/api/dashboard")
                .retrieve()
                .bodyToMono(Map.class)
                .timeout(Duration.ofMillis(timeout))
                .block();
    }
    
    /**
     * 고객 목록 조회
     */
    public Map<String, Object> getCustomers() {
        return webClient.get()
                .uri("/api/customers")
                .retrieve()
                .bodyToMono(Map.class)
                .timeout(Duration.ofMillis(timeout))
                .block();
    }
    
    /**
     * 대출 목록 조회
     */
    public Map<String, Object> getLoans() {
        return webClient.get()
                .uri("/api/loans")
                .retrieve()
                .bodyToMono(Map.class)
                .timeout(Duration.ofMillis(timeout))
                .block();
    }
    
    /**
     * 재대출 신청 목록 조회
     */
    public Map<String, Object> getRefinanceApplications() {
        return webClient.get()
                .uri("/api/refinance-applications")
                .retrieve()
                .bodyToMono(Map.class)
                .timeout(Duration.ofMillis(timeout))
                .block();
    }
    
    /**
     * 재대출 상품 목록 조회
     */
    public Map<String, Object> getProducts() {
        return webClient.get()
                .uri("/api/products")
                .retrieve()
                .bodyToMono(Map.class)
                .timeout(Duration.ofMillis(timeout))
                .block();
    }
    
    /**
     * 고객별 상품 추천 조회
     */
    public Map<String, Object> getRecommendations(Long customerId) {
        return webClient.get()
                .uri("/api/recommendations/{customerId}", customerId)
                .retrieve()
                .bodyToMono(Map.class)
                .timeout(Duration.ofMillis(timeout))
                .block();
    }
    
    /**
     * ML 예측 데이터 조회
     */
    public Map<String, Object> getMlPredictions() {
        return webClient.get()
                .uri("/api/ml_dashboard")
                .retrieve()
                .bodyToMono(Map.class)
                .timeout(Duration.ofMillis(timeout))
                .block();
    }
    
    /**
     * 고객 생성
     */
    public Map<String, Object> createCustomer(Map<String, Object> customerData) {
        return webClient.post()
                .uri("/api/customers")
                .bodyValue(customerData)
                .retrieve()
                .bodyToMono(Map.class)
                .timeout(Duration.ofMillis(timeout))
                .block();
    }
    
    /**
     * 대출 생성
     */
    public Map<String, Object> createLoan(Map<String, Object> loanData) {
        return webClient.post()
                .uri("/api/loans")
                .bodyValue(loanData)
                .retrieve()
                .bodyToMono(Map.class)
                .timeout(Duration.ofMillis(timeout))
                .block();
    }
    
    /**
     * 재대출 신청 생성
     */
    public Map<String, Object> createRefinanceApplication(Map<String, Object> applicationData) {
        return webClient.post()
                .uri("/api/refinance-applications")
                .bodyValue(applicationData)
                .retrieve()
                .bodyToMono(Map.class)
                .timeout(Duration.ofMillis(timeout))
                .block();
    }
}

