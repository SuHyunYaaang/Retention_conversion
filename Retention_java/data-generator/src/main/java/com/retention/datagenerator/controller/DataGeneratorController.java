package com.retention.datagenerator.controller;

import com.retention.datagenerator.service.DataGeneratorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 데이터 생성기 컨트롤러
 * Python의 loan_data_generator.py와 동일한 기능을 제공
 */
@RestController
@RequestMapping("/api/data-generator")
@CrossOrigin(origins = "*")
public class DataGeneratorController {
    
    @Autowired
    private DataGeneratorService dataGeneratorService;
    
    /**
     * 고객 데이터 생성
     */
    @PostMapping("/customers")
    public ResponseEntity<Map<String, Object>> generateCustomers(@RequestParam(defaultValue = "1000") int count) {
        try {
            var customers = dataGeneratorService.generateCustomers(count);
            return ResponseEntity.ok(Map.of(
                "success", true,
                "data", customers,
                "count", customers.size(),
                "generated_at", new java.util.Date()
            ));
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    /**
     * 대출 데이터 생성
     */
    @PostMapping("/loans")
    public ResponseEntity<Map<String, Object>> generateLoans(@RequestParam(defaultValue = "500") int count) {
        try {
            // 먼저 고객 데이터를 생성
            var customers = dataGeneratorService.generateCustomers(1000);
            var loans = dataGeneratorService.generateLoans(count, customers);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "data", loans,
                "count", loans.size(),
                "generated_at", new java.util.Date()
            ));
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    /**
     * 재대출 신청 데이터 생성
     */
    @PostMapping("/refinance-applications")
    public ResponseEntity<Map<String, Object>> generateRefinanceApplications(@RequestParam(defaultValue = "200") int count) {
        try {
            // 먼저 고객과 대출 데이터를 생성
            var customers = dataGeneratorService.generateCustomers(1000);
            var loans = dataGeneratorService.generateLoans(500, customers);
            var applications = dataGeneratorService.generateRefinanceApplications(count, customers, loans);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "data", applications,
                "count", applications.size(),
                "generated_at", new java.util.Date()
            ));
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    /**
     * 재대출 상품 데이터 생성
     */
    @PostMapping("/refinance-products")
    public ResponseEntity<Map<String, Object>> generateRefinanceProducts() {
        try {
            var products = dataGeneratorService.generateRefinanceProducts();
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "data", products,
                "count", products.size(),
                "generated_at", new java.util.Date()
            ));
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    /**
     * 전체 데이터 생성
     */
    @PostMapping("/all")
    public ResponseEntity<Map<String, Object>> generateAllData(
            @RequestParam(defaultValue = "1000") int customerCount,
            @RequestParam(defaultValue = "500") int loanCount,
            @RequestParam(defaultValue = "200") int applicationCount) {
        try {
            var result = dataGeneratorService.generateAllData(customerCount, loanCount, applicationCount);
            result.put("success", true);
            
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    /**
     * 헬스 체크
     */
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> healthCheck() {
        Map<String, String> health = Map.of(
            "status", "UP",
            "service", "Retention Data Generator",
            "version", "1.0.0"
        );
        return ResponseEntity.ok(health);
    }
}

