package com.retention.backend.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * 재대출 상품 정보 엔티티
 */
@Entity
@Table(name = "refinance_products")
public class RefinanceProduct {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "product_name", nullable = false, length = 100)
    @NotBlank
    private String productName;
    
    @Column(name = "product_code", unique = true, nullable = false, length = 50)
    @NotBlank
    private String productCode;
    
    @Column(name = "min_interest_rate", nullable = false)
    @NotNull
    @Positive
    private Double minInterestRate;
    
    @Column(name = "max_interest_rate", nullable = false)
    @NotNull
    @Positive
    private Double maxInterestRate;
    
    @Column(name = "min_loan_amount", nullable = false)
    @NotNull
    @Positive
    private Double minLoanAmount;
    
    @Column(name = "max_loan_amount", nullable = false)
    @NotNull
    @Positive
    private Double maxLoanAmount;
    
    @Column(name = "loan_term_min", nullable = false)
    @NotNull
    @Positive
    private Integer loanTermMin;
    
    @Column(name = "loan_term_max", nullable = false)
    @NotNull
    @Positive
    private Integer loanTermMax;
    
    @Column(name = "eligibility_criteria", columnDefinition = "TEXT")
    private String eligibilityCriteria;
    
    @Column(name = "is_active")
    private Boolean isActive = true;
    
    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    // 기본 생성자
    public RefinanceProduct() {}
    
    // 생성자
    public RefinanceProduct(String productName, String productCode, Double minInterestRate, 
                           Double maxInterestRate, Double minLoanAmount, Double maxLoanAmount,
                           Integer loanTermMin, Integer loanTermMax) {
        this.productName = productName;
        this.productCode = productCode;
        this.minInterestRate = minInterestRate;
        this.maxInterestRate = maxInterestRate;
        this.minLoanAmount = minLoanAmount;
        this.maxLoanAmount = maxLoanAmount;
        this.loanTermMin = loanTermMin;
        this.loanTermMax = loanTermMax;
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }
    
    public String getProductCode() { return productCode; }
    public void setProductCode(String productCode) { this.productCode = productCode; }
    
    public Double getMinInterestRate() { return minInterestRate; }
    public void setMinInterestRate(Double minInterestRate) { this.minInterestRate = minInterestRate; }
    
    public Double getMaxInterestRate() { return maxInterestRate; }
    public void setMaxInterestRate(Double maxInterestRate) { this.maxInterestRate = maxInterestRate; }
    
    public Double getMinLoanAmount() { return minLoanAmount; }
    public void setMinLoanAmount(Double minLoanAmount) { this.minLoanAmount = minLoanAmount; }
    
    public Double getMaxLoanAmount() { return maxLoanAmount; }
    public void setMaxLoanAmount(Double maxLoanAmount) { this.maxLoanAmount = maxLoanAmount; }
    
    public Integer getLoanTermMin() { return loanTermMin; }
    public void setLoanTermMin(Integer loanTermMin) { this.loanTermMin = loanTermMin; }
    
    public Integer getLoanTermMax() { return loanTermMax; }
    public void setLoanTermMax(Integer loanTermMax) { this.loanTermMax = loanTermMax; }
    
    public String getEligibilityCriteria() { return eligibilityCriteria; }
    public void setEligibilityCriteria(String eligibilityCriteria) { this.eligibilityCriteria = eligibilityCriteria; }
    
    public Boolean getIsActive() { return isActive; }
    public void setIsActive(Boolean isActive) { this.isActive = isActive; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
    
    @Override
    public String toString() {
        return "RefinanceProduct{" +
                "id=" + id +
                ", productName='" + productName + '\'' +
                ", productCode='" + productCode + '\'' +
                ", minInterestRate=" + minInterestRate +
                ", maxInterestRate=" + maxInterestRate +
                ", minLoanAmount=" + minLoanAmount +
                ", maxLoanAmount=" + maxLoanAmount +
                ", loanTermMin=" + loanTermMin +
                ", loanTermMax=" + loanTermMax +
                ", eligibilityCriteria='" + eligibilityCriteria + '\'' +
                ", isActive=" + isActive +
                ", createdAt=" + createdAt +
                ", updatedAt=" + updatedAt +
                '}';
    }
}

