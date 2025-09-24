package com.retention.backend.repository;

import com.retention.backend.model.Document;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 문서 Repository 인터페이스
 */
@Repository
public interface DocumentRepository extends JpaRepository<Document, Long> {
    
    /**
     * 신청 ID로 문서 목록 조회
     */
    List<Document> findByApplicationId(Long applicationId);
    
    /**
     * 문서 유형으로 문서 목록 조회
     */
    List<Document> findByDocumentType(String documentType);
    
    /**
     * 파일명으로 문서 조회
     */
    List<Document> findByFileName(String fileName);
    
    /**
     * 파일 경로로 문서 조회
     */
    List<Document> findByFilePath(String filePath);
    
    /**
     * 신청 ID와 문서 유형으로 문서 조회
     */
    List<Document> findByApplicationIdAndDocumentType(Long applicationId, String documentType);
    
    /**
     * 신청별 문서 수 조회
     */
    @Query("SELECT d.applicationId, COUNT(d) FROM Document d GROUP BY d.applicationId")
    List<Object[]> countByApplication();
    
    /**
     * 문서 유형별 문서 수 조회
     */
    @Query("SELECT d.documentType, COUNT(d) FROM Document d GROUP BY d.documentType")
    List<Object[]> countByDocumentType();
    
    /**
     * 총 문서 수 조회
     */
    @Query("SELECT COUNT(d) FROM Document d")
    Long getTotalDocumentCount();
    
    /**
     * 평균 파일 크기 조회
     */
    @Query("SELECT AVG(d.fileSize) FROM Document d WHERE d.fileSize IS NOT NULL")
    Double getAverageFileSize();
    
    /**
     * 최근 업로드된 문서 조회
     */
    @Query("SELECT d FROM Document d ORDER BY d.uploadDate DESC")
    List<Document> findRecentDocuments(org.springframework.data.domain.Pageable pageable);
}

