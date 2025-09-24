package com.retention.datagenerator.service;

import org.springframework.stereotype.Service;

import java.util.*;

/**
 * 데이터 생성 서비스
 * Python의 loan_data_generator.py와 동일한 기능을 제공
 */
@Service
public class DataGeneratorService {
    
    private final Random random = new Random();
    
    // 샘플 데이터
    private final String[] names = {"김철수", "이영희", "박민수", "최지영", "정현우", "한소영", "윤태호", "강미래"};
    private final String[] jobTypes = {"직장인", "사업자", "자영업", "프리랜서", "공무원", "교사", "의사", "변호사"};
    private final String[] incomeLevels = {"2000만원 미만", "2000-3000만원", "3000-4000만원", "4000-5000만원", "5000-7000만원", "7000만원 이상"};
    private final String[] creditGrades = {"A", "B", "C", "D"};
    private final String[] loanTypes = {"주택담보대출", "신용대출", "전세자금대출", "자동차대출", "학자금대출"};
    private final String[] loanStatuses = {"active", "approved", "disbursed", "completed", "overdue"};
    private final String[] productNames = {"우리집 대출", "행복한 대출", "스마트 대출", "프리미엄 대출", "기본 대출"};
    
    /**
     * 고객 데이터 생성
     */
    public List<Map<String, Object>> generateCustomers(int count) {
        List<Map<String, Object>> customers = new ArrayList<>();
        
        for (int i = 1; i <= count; i++) {
            Map<String, Object> customer = new HashMap<>();
            customer.put("customer_id", String.format("CUST%06d", i));
            customer.put("name", names[random.nextInt(names.length)]);
            customer.put("phone", generatePhoneNumber());
            customer.put("email", generateEmail(customer.get("name").toString()));
            customer.put("age", 25 + random.nextInt(50));
            customer.put("job_type", jobTypes[random.nextInt(jobTypes.length)]);
            customer.put("income_level", incomeLevels[random.nextInt(incomeLevels.length)]);
            customer.put("credit_grade", creditGrades[random.nextInt(creditGrades.length)]);
            customer.put("address", generateAddress());
            customer.put("created_at", new Date());
            
            customers.add(customer);
        }
        
        return customers;
    }
    
    /**
     * 대출 데이터 생성
     */
    public List<Map<String, Object>> generateLoans(int count, List<Map<String, Object>> customers) {
        List<Map<String, Object>> loans = new ArrayList<>();
        
        for (int i = 1; i <= count; i++) {
            Map<String, Object> customer = customers.get(random.nextInt(customers.size()));
            Map<String, Object> loan = new HashMap<>();
            
            loan.put("loan_id", String.format("LOAN%06d", i));
            loan.put("customer_id", customer.get("customer_id"));
            loan.put("loan_type", loanTypes[random.nextInt(loanTypes.length)]);
            loan.put("loan_amount", 10000000 + random.nextInt(90000000)); // 1천만원 ~ 1억원
            loan.put("loan_term", 12 + random.nextInt(48)); // 1년 ~ 5년
            loan.put("interest_rate", 3.0 + random.nextDouble() * 5.0); // 3% ~ 8%
            loan.put("monthly_payment", calculateMonthlyPayment(loan));
            loan.put("status", loanStatuses[random.nextInt(loanStatuses.length)]);
            loan.put("application_date", generateRandomDate());
            loan.put("approval_date", generateRandomDate());
            loan.put("disbursement_date", generateRandomDate());
            loan.put("overdue_days", random.nextInt(30));
            loan.put("created_at", new Date());
            
            loans.add(loan);
        }
        
        return loans;
    }
    
    /**
     * 재대출 신청 데이터 생성
     */
    public List<Map<String, Object>> generateRefinanceApplications(int count, List<Map<String, Object>> customers, List<Map<String, Object>> loans) {
        List<Map<String, Object>> applications = new ArrayList<>();
        
        for (int i = 1; i <= count; i++) {
            Map<String, Object> customer = customers.get(random.nextInt(customers.size()));
            Map<String, Object> loan = loans.get(random.nextInt(loans.size()));
            Map<String, Object> application = new HashMap<>();
            
            application.put("application_number", String.format("REF-%s-%06d", 
                java.time.LocalDate.now().format(java.time.format.DateTimeFormatter.ofPattern("yyyyMMdd")), i));
            application.put("customer_id", customer.get("customer_id"));
            application.put("original_loan_id", loan.get("loan_id"));
            application.put("requested_amount", 10000000 + random.nextInt(50000000)); // 1천만원 ~ 6천만원
            application.put("requested_interest_rate", 2.5 + random.nextDouble() * 4.0); // 2.5% ~ 6.5%
            application.put("application_status", "pending");
            application.put("application_date", new Date());
            application.put("created_at", new Date());
            
            applications.add(application);
        }
        
        return applications;
    }
    
    /**
     * 재대출 상품 데이터 생성
     */
    public List<Map<String, Object>> generateRefinanceProducts() {
        List<Map<String, Object>> products = new ArrayList<>();
        
        for (int i = 0; i < productNames.length; i++) {
            Map<String, Object> product = new HashMap<>();
            product.put("product_name", productNames[i]);
            product.put("product_code", String.format("PROD%03d", i + 1));
            product.put("min_interest_rate", 2.0 + random.nextDouble() * 2.0); // 2% ~ 4%
            product.put("max_interest_rate", 4.0 + random.nextDouble() * 3.0); // 4% ~ 7%
            product.put("min_loan_amount", 10000000.0); // 1천만원
            product.put("max_loan_amount", 100000000.0); // 1억원
            product.put("loan_term_min", 12); // 1년
            product.put("loan_term_max", 60); // 5년
            product.put("eligibility_criteria", "신용등급 B 이상, 소득증빙서류 필수");
            product.put("is_active", true);
            product.put("created_at", new Date());
            
            products.add(product);
        }
        
        return products;
    }
    
    /**
     * 전체 데이터 생성
     */
    public Map<String, Object> generateAllData(int customerCount, int loanCount, int applicationCount) {
        Map<String, Object> result = new HashMap<>();
        
        List<Map<String, Object>> customers = generateCustomers(customerCount);
        List<Map<String, Object>> loans = generateLoans(loanCount, customers);
        List<Map<String, Object>> applications = generateRefinanceApplications(applicationCount, customers, loans);
        List<Map<String, Object>> products = generateRefinanceProducts();
        
        result.put("customers", customers);
        result.put("loans", loans);
        result.put("refinance_applications", applications);
        result.put("refinance_products", products);
        result.put("generated_at", new Date());
        result.put("total_records", customers.size() + loans.size() + applications.size() + products.size());
        
        return result;
    }
    
    // 헬퍼 메서드들
    private String generatePhoneNumber() {
        return String.format("010-%04d-%04d", random.nextInt(10000), random.nextInt(10000));
    }
    
    private String generateEmail(String name) {
        String[] domains = {"gmail.com", "naver.com", "daum.net", "yahoo.com"};
        return String.format("%s%d@%s", name, random.nextInt(1000), domains[random.nextInt(domains.length)]);
    }
    
    private String generateAddress() {
        String[] cities = {"서울시", "부산시", "대구시", "인천시", "광주시", "대전시", "울산시"};
        String[] districts = {"강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구"};
        return String.format("%s %s %d번지", 
            cities[random.nextInt(cities.length)], 
            districts[random.nextInt(districts.length)], 
            random.nextInt(100) + 1);
    }
    
    private Integer calculateMonthlyPayment(Map<String, Object> loan) {
        double amount = (Integer) loan.get("loan_amount");
        double rate = (Double) loan.get("interest_rate") / 100 / 12; // 월 이자율
        int term = (Integer) loan.get("loan_term");
        
        if (rate == 0) {
            return (int) (amount / term);
        }
        
        double monthlyPayment = amount * (rate * Math.pow(1 + rate, term)) / (Math.pow(1 + rate, term) - 1);
        return (int) monthlyPayment;
    }
    
    private Date generateRandomDate() {
        long now = System.currentTimeMillis();
        long randomTime = now - random.nextInt(365 * 24 * 60 * 60 * 1000); // 최근 1년 내
        return new Date(randomTime);
    }
}

