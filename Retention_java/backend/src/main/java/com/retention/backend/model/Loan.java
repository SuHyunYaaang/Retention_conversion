package com.retention.backend.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * 기존 대출 정보 엔티티
 */
@Entity
@Table(name = "loans")
public class Loan {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "loan_id", unique = true, nullable = false, length = 20)
    @NotBlank
    private String loanId;
    
    @Column(name = "customer_id", nullable = false, length = 20)
    @NotBlank
    private String customerId;
    
    @Column(name = "loan_type", nullable = false, length = 30)
    @NotBlank
    private String loanType;
    
    @Column(name = "loan_amount", nullable = false)
    @NotNull
    @Positive
    private Integer loanAmount;
    
    @Column(name = "loan_term", nullable = false)
    @NotNull
    @Positive
    private Integer loanTerm;
    
    @Column(name = "interest_rate", nullable = false)
    @NotNull
    @Positive
    private Double interestRate;
    
    @Column(name = "monthly_payment", nullable = false)
    @NotNull
    @Positive
    private Integer monthlyPayment;
    
    @Column(name = "status", nullable = false, length = 20)
    @NotBlank
    private String status;
    
    @Column(name = "application_date")
    private LocalDateTime applicationDate;
    
    @Column(name = "approval_date")
    private LocalDateTime approvalDate;
    
    @Column(name = "disbursement_date")
    private LocalDateTime disbursementDate;
    
    @Column(name = "overdue_days")
    private Integer overdueDays = 0;
    
    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    // 관계 설정
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id", referencedColumnName = "customer_id", insertable = false, updatable = false)
    private Customer customer;
    
    @OneToMany(mappedBy = "originalLoan", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private java.util.List<RefinanceApplication> refinanceApplications;
    
    // 기본 생성자
    public Loan() {}
    
    // 생성자
    public Loan(String loanId, String customerId, String loanType, Integer loanAmount, 
                Integer loanTerm, Double interestRate, Integer monthlyPayment, String status) {
        this.loanId = loanId;
        this.customerId = customerId;
        this.loanType = loanType;
        this.loanAmount = loanAmount;
        this.loanTerm = loanTerm;
        this.interestRate = interestRate;
        this.monthlyPayment = monthlyPayment;
        this.status = status;
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getLoanId() { return loanId; }
    public void setLoanId(String loanId) { this.loanId = loanId; }
    
    public String getCustomerId() { return customerId; }
    public void setCustomerId(String customerId) { this.customerId = customerId; }
    
    public String getLoanType() { return loanType; }
    public void setLoanType(String loanType) { this.loanType = loanType; }
    
    public Integer getLoanAmount() { return loanAmount; }
    public void setLoanAmount(Integer loanAmount) { this.loanAmount = loanAmount; }
    
    public Integer getLoanTerm() { return loanTerm; }
    public void setLoanTerm(Integer loanTerm) { this.loanTerm = loanTerm; }
    
    public Double getInterestRate() { return interestRate; }
    public void setInterestRate(Double interestRate) { this.interestRate = interestRate; }
    
    public Integer getMonthlyPayment() { return monthlyPayment; }
    public void setMonthlyPayment(Integer monthlyPayment) { this.monthlyPayment = monthlyPayment; }
    
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    
    public LocalDateTime getApplicationDate() { return applicationDate; }
    public void setApplicationDate(LocalDateTime applicationDate) { this.applicationDate = applicationDate; }
    
    public LocalDateTime getApprovalDate() { return approvalDate; }
    public void setApprovalDate(LocalDateTime approvalDate) { this.approvalDate = approvalDate; }
    
    public LocalDateTime getDisbursementDate() { return disbursementDate; }
    public void setDisbursementDate(LocalDateTime disbursementDate) { this.disbursementDate = disbursementDate; }
    
    public Integer getOverdueDays() { return overdueDays; }
    public void setOverdueDays(Integer overdueDays) { this.overdueDays = overdueDays; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
    
    public Customer getCustomer() { return customer; }
    public void setCustomer(Customer customer) { this.customer = customer; }
    
    public java.util.List<RefinanceApplication> getRefinanceApplications() { return refinanceApplications; }
    public void setRefinanceApplications(java.util.List<RefinanceApplication> refinanceApplications) { 
        this.refinanceApplications = refinanceApplications; 
    }
    
    @Override
    public String toString() {
        return "Loan{" +
                "id=" + id +
                ", loanId='" + loanId + '\'' +
                ", customerId='" + customerId + '\'' +
                ", loanType='" + loanType + '\'' +
                ", loanAmount=" + loanAmount +
                ", loanTerm=" + loanTerm +
                ", interestRate=" + interestRate +
                ", monthlyPayment=" + monthlyPayment +
                ", status='" + status + '\'' +
                ", applicationDate=" + applicationDate +
                ", approvalDate=" + approvalDate +
                ", disbursementDate=" + disbursementDate +
                ", overdueDays=" + overdueDays +
                ", createdAt=" + createdAt +
                ", updatedAt=" + updatedAt +
                '}';
    }
}

