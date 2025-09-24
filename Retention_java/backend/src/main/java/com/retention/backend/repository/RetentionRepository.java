package com.retention.backend.repository;

import com.retention.backend.model.Retention;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 재고정 Repository 인터페이스
 */
@Repository
public interface RetentionRepository extends JpaRepository<Retention, Long> {
    
    /**
     * 고객 ID로 재고정 목록 조회
     */
    List<Retention> findByCustomerId(Long customerId);
    
    /**
     * 재고정 유형으로 재고정 목록 조회
     */
    List<Retention> findByRetentionType(String retentionType);
    
    /**
     * 상태로 재고정 목록 조회
     */
    List<Retention> findByStatus(String status);
    
    /**
     * 활성 재고정 목록 조회
     */
    @Query("SELECT r FROM Retention r WHERE r.status = 'active'")
    List<Retention> findActiveRetentions();
    
    /**
     * 만료된 재고정 목록 조회
     */
    @Query("SELECT r FROM Retention r WHERE r.status = 'expired'")
    List<Retention> findExpiredRetentions();
    
    /**
     * 취소된 재고정 목록 조회
     */
    @Query("SELECT r FROM Retention r WHERE r.status = 'cancelled'")
    List<Retention> findCancelledRetentions();
    
    /**
     * 특정 기간 내 재고정 목록 조회
     */
    @Query("SELECT r FROM Retention r WHERE r.startDate BETWEEN :startDate AND :endDate")
    List<Retention> findRetentionsByDateRange(@Param("startDate") LocalDateTime startDate, 
                                              @Param("endDate") LocalDateTime endDate);
    
    /**
     * 만료 예정 재고정 목록 조회
     */
    @Query("SELECT r FROM Retention r WHERE r.endDate IS NOT NULL AND r.endDate <= :expiryDate AND r.status = 'active'")
    List<Retention> findRetentionsExpiringBy(@Param("expiryDate") LocalDateTime expiryDate);
    
    /**
     * 재고정 유형별 재고정 수 조회
     */
    @Query("SELECT r.retentionType, COUNT(r) FROM Retention r GROUP BY r.retentionType")
    List<Object[]> countByRetentionType();
    
    /**
     * 상태별 재고정 수 조회
     */
    @Query("SELECT r.status, COUNT(r) FROM Retention r GROUP BY r.status")
    List<Object[]> countByStatus();
    
    /**
     * 고객별 재고정 수 조회
     */
    @Query("SELECT r.customerId, COUNT(r) FROM Retention r GROUP BY r.customerId")
    List<Object[]> countByCustomer();
    
    /**
     * 활성 재고정 수 조회
     */
    @Query("SELECT COUNT(r) FROM Retention r WHERE r.status = 'active'")
    Long countActiveRetentions();
    
    /**
     * 최근 재고정 조회
     */
    @Query("SELECT r FROM Retention r ORDER BY r.createdAt DESC")
    List<Retention> findRecentRetentions(org.springframework.data.domain.Pageable pageable);
}

