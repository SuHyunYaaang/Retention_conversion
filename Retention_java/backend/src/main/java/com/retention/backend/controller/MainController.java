package com.retention.backend.controller;

import com.retention.backend.dto.CustomerDto;
import com.retention.backend.model.Customer;
import com.retention.backend.model.Loan;
import com.retention.backend.model.RefinanceApplication;
import com.retention.backend.model.RefinanceProduct;
import com.retention.backend.repository.CustomerRepository;
import com.retention.backend.repository.LoanRepository;
import com.retention.backend.repository.RefinanceApplicationRepository;
import com.retention.backend.repository.RefinanceProductRepository;
import com.retention.backend.service.CustomerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * 메인 컨트롤러
 * FastAPI의 main.py와 동일한 기능을 제공
 */
@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class MainController {
    
    @Autowired
    private CustomerService customerService;
    
    @Autowired
    private CustomerRepository customerRepository;
    
    @Autowired
    private LoanRepository loanRepository;
    
    @Autowired
    private RefinanceApplicationRepository refinanceApplicationRepository;
    
    @Autowired
    private RefinanceProductRepository refinanceProductRepository;
    
    /**
     * 메인 페이지 정보
     */
    @GetMapping("/")
    public ResponseEntity<Map<String, Object>> getMainInfo() {
        Map<String, Object> response = new HashMap<>();
        response.put("message", "재대출 자동화 서비스 API");
        response.put("version", "1.0.0");
        response.put("status", "running");
        return ResponseEntity.ok(response);
    }
    
    /**
     * 대시보드 데이터 조회
     */
    @GetMapping("/dashboard")
    public ResponseEntity<Map<String, Object>> getDashboardData() {
        try {
            // 고객 수
            long customerCount = customerRepository.count();
            
            // 대출 수
            long loanCount = loanRepository.count();
            
            // 재대출 신청 수
            long refinanceCount = refinanceApplicationRepository.count();
            
            // 상품 수
            long productCount = refinanceProductRepository.countActiveProducts();
            
            Map<String, Object> response = new HashMap<>();
            response.put("customer_count", customerCount);
            response.put("loan_count", loanCount);
            response.put("refinance_count", refinanceCount);
            response.put("product_count", productCount);
            response.put("total_assets", loanCount * 50000000L); // 예시 데이터
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("error", "대시보드 데이터 조회 실패: " + e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }
    
    /**
     * 고객 목록 조회
     */
    @GetMapping("/customers")
    public ResponseEntity<Page<Customer>> getCustomers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "100") int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<Customer> customers = customerService.getCustomers(pageable);
        return ResponseEntity.ok(customers);
    }
    
    /**
     * 새 고객 생성
     */
    @PostMapping("/customers")
    public ResponseEntity<Customer> createCustomer(@RequestBody CustomerDto.Create createDto) {
        try {
            Customer customer = customerService.createCustomer(createDto);
            return ResponseEntity.ok(customer);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().build();
        }
    }
    
    /**
     * 대출 목록 조회
     */
    @GetMapping("/loans")
    public ResponseEntity<Page<Loan>> getLoans(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "100") int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<Loan> loans = loanRepository.findAll(pageable);
        return ResponseEntity.ok(loans);
    }
    
    /**
     * 새 대출 생성
     */
    @PostMapping("/loans")
    public ResponseEntity<Loan> createLoan(@RequestBody Loan loan) {
        try {
            Loan savedLoan = loanRepository.save(loan);
            return ResponseEntity.ok(savedLoan);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }
    
    /**
     * 재대출 신청 목록 조회
     */
    @GetMapping("/refinance-applications")
    public ResponseEntity<Page<RefinanceApplication>> getRefinanceApplications(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "100") int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<RefinanceApplication> applications = refinanceApplicationRepository.findAll(pageable);
        return ResponseEntity.ok(applications);
    }
    
    /**
     * 새 재대출 신청 생성
     */
    @PostMapping("/refinance-applications")
    public ResponseEntity<RefinanceApplication> createRefinanceApplication(@RequestBody RefinanceApplication application) {
        try {
            RefinanceApplication savedApplication = refinanceApplicationRepository.save(application);
            return ResponseEntity.ok(savedApplication);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }
    
    /**
     * 재대출 상품 목록 조회
     */
    @GetMapping("/products")
    public ResponseEntity<List<RefinanceProduct>> getProducts() {
        List<RefinanceProduct> products = refinanceProductRepository.findByIsActiveTrue();
        return ResponseEntity.ok(products);
    }
    
    /**
     * 고객별 상품 추천
     */
    @GetMapping("/recommendations/{customerId}")
    public ResponseEntity<Map<String, Object>> getRecommendations(@PathVariable Long customerId) {
        try {
            // 고객 정보 조회
            Optional<Customer> customerOpt = customerRepository.findById(customerId);
            if (customerOpt.isEmpty()) {
                Map<String, Object> errorResponse = new HashMap<>();
                errorResponse.put("error", "Customer not found");
                return ResponseEntity.status(404).body(errorResponse);
            }
            
            Customer customer = customerOpt.get();
            
            // 고객의 대출 정보 조회
            List<Loan> loans = loanRepository.findByCustomerId(customer.getCustomerId());
            
            // 추천 상품 조회 (예시 로직)
            Pageable pageable = PageRequest.of(0, 3);
            List<RefinanceProduct> products = refinanceProductRepository.findByIsActiveTrue();
            if (products.size() > 3) {
                products = products.subList(0, 3);
            }
            
            Map<String, Object> response = new HashMap<>();
            response.put("customer", customer);
            response.put("current_loans", loans);
            response.put("recommended_products", products);
            response.put("recommendation_reason", "현재 대출 조건 대비 유리한 금리 상품");
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("error", "추천 데이터 조회 실패: " + e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }
    
    /**
     * ML 예측 데이터 조회
     */
    @GetMapping("/ml_dashboard")
    public ResponseEntity<List<Map<String, Object>>> getMlPredictions() {
        try {
            // 실제 구현에서는 복잡한 쿼리나 ML 서비스 호출이 필요
            // 여기서는 간단한 예시 데이터를 반환
            List<Map<String, Object>> data = List.of(
                Map.of(
                    "id", 1,
                    "customer_id", "CUST001",
                    "age", 30,
                    "income_level", "3000-4000만원",
                    "credit_grade", "B",
                    "loan_amount", 50000000,
                    "interest_rate", 5.2,
                    "loan_term", 36,
                    "monthly_payment", 1500000,
                    "payment_history_months", 12,
                    "late_payments_3m", 0,
                    "late_payments_6m", 0,
                    "late_payments_12m", 0,
                    "credit_utilization", 0.3,
                    "debt_to_income_ratio", 0.5,
                    "employment_length_years", 5,
                    "number_of_accounts", 3,
                    "inquiries_last_6m", 1,
                    "everdelinquent", 0,
                    "created_at", "2024-01-01 00:00:00"
                )
            );
            
            return ResponseEntity.ok(data);
        } catch (Exception e) {
            return ResponseEntity.status(500).build();
        }
    }
}

