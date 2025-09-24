package com.retention.backend.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

/**
 * 신청 로그 엔티티
 */
@Entity
@Table(name = "application_logs")
public class ApplicationLog {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "application_id", nullable = false)
    @NotNull
    private Long applicationId;
    
    @Column(name = "action", nullable = false, length = 50)
    @NotBlank
    private String action;
    
    @Column(name = "description", columnDefinition = "TEXT")
    private String description;
    
    @Column(name = "performed_by", length = 100)
    private String performedBy;
    
    @CreationTimestamp
    @Column(name = "performed_at", nullable = false, updatable = false)
    private LocalDateTime performedAt;
    
    // 관계 설정
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "application_id", insertable = false, updatable = false)
    private RefinanceApplication application;
    
    // 기본 생성자
    public ApplicationLog() {}
    
    // 생성자
    public ApplicationLog(Long applicationId, String action, String description, String performedBy) {
        this.applicationId = applicationId;
        this.action = action;
        this.description = description;
        this.performedBy = performedBy;
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Long getApplicationId() { return applicationId; }
    public void setApplicationId(Long applicationId) { this.applicationId = applicationId; }
    
    public String getAction() { return action; }
    public void setAction(String action) { this.action = action; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public String getPerformedBy() { return performedBy; }
    public void setPerformedBy(String performedBy) { this.performedBy = performedBy; }
    
    public LocalDateTime getPerformedAt() { return performedAt; }
    public void setPerformedAt(LocalDateTime performedAt) { this.performedAt = performedAt; }
    
    public RefinanceApplication getApplication() { return application; }
    public void setApplication(RefinanceApplication application) { this.application = application; }
    
    @Override
    public String toString() {
        return "ApplicationLog{" +
                "id=" + id +
                ", applicationId=" + applicationId +
                ", action='" + action + '\'' +
                ", description='" + description + '\'' +
                ", performedBy='" + performedBy + '\'' +
                ", performedAt=" + performedAt +
                '}';
    }
}

