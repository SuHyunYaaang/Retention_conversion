package com.retention.backend.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

/**
 * 문서 정보 엔티티
 */
@Entity
@Table(name = "documents")
public class Document {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "application_id", nullable = false)
    @NotNull
    private Long applicationId;
    
    @Column(name = "document_type", nullable = false, length = 50)
    @NotBlank
    private String documentType;
    
    @Column(name = "file_name", nullable = false, length = 255)
    @NotBlank
    private String fileName;
    
    @Column(name = "file_path", nullable = false, length = 500)
    @NotBlank
    private String filePath;
    
    @Column(name = "file_size")
    private Long fileSize;
    
    @CreationTimestamp
    @Column(name = "upload_date", nullable = false, updatable = false)
    private LocalDateTime uploadDate;
    
    // 관계 설정
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "application_id", insertable = false, updatable = false)
    private RefinanceApplication application;
    
    // 기본 생성자
    public Document() {}
    
    // 생성자
    public Document(Long applicationId, String documentType, String fileName, String filePath) {
        this.applicationId = applicationId;
        this.documentType = documentType;
        this.fileName = fileName;
        this.filePath = filePath;
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Long getApplicationId() { return applicationId; }
    public void setApplicationId(Long applicationId) { this.applicationId = applicationId; }
    
    public String getDocumentType() { return documentType; }
    public void setDocumentType(String documentType) { this.documentType = documentType; }
    
    public String getFileName() { return fileName; }
    public void setFileName(String fileName) { this.fileName = fileName; }
    
    public String getFilePath() { return filePath; }
    public void setFilePath(String filePath) { this.filePath = filePath; }
    
    public Long getFileSize() { return fileSize; }
    public void setFileSize(Long fileSize) { this.fileSize = fileSize; }
    
    public LocalDateTime getUploadDate() { return uploadDate; }
    public void setUploadDate(LocalDateTime uploadDate) { this.uploadDate = uploadDate; }
    
    public RefinanceApplication getApplication() { return application; }
    public void setApplication(RefinanceApplication application) { this.application = application; }
    
    @Override
    public String toString() {
        return "Document{" +
                "id=" + id +
                ", applicationId=" + applicationId +
                ", documentType='" + documentType + '\'' +
                ", fileName='" + fileName + '\'' +
                ", filePath='" + filePath + '\'' +
                ", fileSize=" + fileSize +
                ", uploadDate=" + uploadDate +
                '}';
    }
}

