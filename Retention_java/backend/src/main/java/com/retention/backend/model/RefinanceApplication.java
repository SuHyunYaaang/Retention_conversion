package com.retention.backend.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 재대출 신청 정보 엔티티
 */
@Entity
@Table(name = "refinance_applications")
public class RefinanceApplication {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "application_number", unique = true, nullable = false, length = 50)
    @NotBlank
    private String applicationNumber;
    
    @Column(name = "customer_id", nullable = false)
    @NotNull
    private Long customerId;
    
    @Column(name = "original_loan_id", nullable = false)
    @NotNull
    private Long originalLoanId;
    
    @Column(name = "requested_amount", nullable = false)
    @NotNull
    @Positive
    private Double requestedAmount;
    
    @Column(name = "requested_interest_rate")
    @Positive
    private Double requestedInterestRate;
    
    @Column(name = "application_status", length = 20)
    private String applicationStatus = "pending";
    
    @Column(name = "application_date")
    @CreationTimestamp
    private LocalDateTime applicationDate;
    
    @Column(name = "approval_date")
    private LocalDateTime approvalDate;
    
    @Column(name = "rejection_reason", columnDefinition = "TEXT")
    private String rejectionReason;
    
    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    // 관계 설정
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id", insertable = false, updatable = false)
    private Customer customer;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "original_loan_id", insertable = false, updatable = false)
    private Loan originalLoan;
    
    @OneToMany(mappedBy = "application", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Document> documents;
    
    @OneToMany(mappedBy = "application", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<ApplicationLog> applicationLogs;
    
    // 기본 생성자
    public RefinanceApplication() {}
    
    // 생성자
    public RefinanceApplication(String applicationNumber, Long customerId, Long originalLoanId, 
                               Double requestedAmount) {
        this.applicationNumber = applicationNumber;
        this.customerId = customerId;
        this.originalLoanId = originalLoanId;
        this.requestedAmount = requestedAmount;
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getApplicationNumber() { return applicationNumber; }
    public void setApplicationNumber(String applicationNumber) { this.applicationNumber = applicationNumber; }
    
    public Long getCustomerId() { return customerId; }
    public void setCustomerId(Long customerId) { this.customerId = customerId; }
    
    public Long getOriginalLoanId() { return originalLoanId; }
    public void setOriginalLoanId(Long originalLoanId) { this.originalLoanId = originalLoanId; }
    
    public Double getRequestedAmount() { return requestedAmount; }
    public void setRequestedAmount(Double requestedAmount) { this.requestedAmount = requestedAmount; }
    
    public Double getRequestedInterestRate() { return requestedInterestRate; }
    public void setRequestedInterestRate(Double requestedInterestRate) { this.requestedInterestRate = requestedInterestRate; }
    
    public String getApplicationStatus() { return applicationStatus; }
    public void setApplicationStatus(String applicationStatus) { this.applicationStatus = applicationStatus; }
    
    public LocalDateTime getApplicationDate() { return applicationDate; }
    public void setApplicationDate(LocalDateTime applicationDate) { this.applicationDate = applicationDate; }
    
    public LocalDateTime getApprovalDate() { return approvalDate; }
    public void setApprovalDate(LocalDateTime approvalDate) { this.approvalDate = approvalDate; }
    
    public String getRejectionReason() { return rejectionReason; }
    public void setRejectionReason(String rejectionReason) { this.rejectionReason = rejectionReason; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
    
    public Customer getCustomer() { return customer; }
    public void setCustomer(Customer customer) { this.customer = customer; }
    
    public Loan getOriginalLoan() { return originalLoan; }
    public void setOriginalLoan(Loan originalLoan) { this.originalLoan = originalLoan; }
    
    public List<Document> getDocuments() { return documents; }
    public void setDocuments(List<Document> documents) { this.documents = documents; }
    
    public List<ApplicationLog> getApplicationLogs() { return applicationLogs; }
    public void setApplicationLogs(List<ApplicationLog> applicationLogs) { this.applicationLogs = applicationLogs; }
    
    @Override
    public String toString() {
        return "RefinanceApplication{" +
                "id=" + id +
                ", applicationNumber='" + applicationNumber + '\'' +
                ", customerId=" + customerId +
                ", originalLoanId=" + originalLoanId +
                ", requestedAmount=" + requestedAmount +
                ", requestedInterestRate=" + requestedInterestRate +
                ", applicationStatus='" + applicationStatus + '\'' +
                ", applicationDate=" + applicationDate +
                ", approvalDate=" + approvalDate +
                ", rejectionReason='" + rejectionReason + '\'' +
                ", createdAt=" + createdAt +
                ", updatedAt=" + updatedAt +
                '}';
    }
}

