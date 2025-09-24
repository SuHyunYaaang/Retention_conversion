package com.retention.backend.repository;

import com.retention.backend.model.ApplicationLog;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 신청 로그 Repository 인터페이스
 */
@Repository
public interface ApplicationLogRepository extends JpaRepository<ApplicationLog, Long> {
    
    /**
     * 신청 ID로 로그 목록 조회
     */
    List<ApplicationLog> findByApplicationId(Long applicationId);
    
    /**
     * 액션으로 로그 목록 조회
     */
    List<ApplicationLog> findByAction(String action);
    
    /**
     * 수행자로 로그 목록 조회
     */
    List<ApplicationLog> findByPerformedBy(String performedBy);
    
    /**
     * 신청 ID로 최신 로그 조회
     */
    @Query("SELECT al FROM ApplicationLog al WHERE al.applicationId = :applicationId ORDER BY al.performedAt DESC")
    List<ApplicationLog> findRecentLogsByApplicationId(@Param("applicationId") Long applicationId, Pageable pageable);
    
    /**
     * 특정 기간 내 로그 조회
     */
    @Query("SELECT al FROM ApplicationLog al WHERE al.performedAt BETWEEN :startDate AND :endDate")
    List<ApplicationLog> findLogsByDateRange(@Param("startDate") LocalDateTime startDate, 
                                            @Param("endDate") LocalDateTime endDate);
    
    /**
     * 액션별 로그 수 조회
     */
    @Query("SELECT al.action, COUNT(al) FROM ApplicationLog al GROUP BY al.action")
    List<Object[]> countByAction();
    
    /**
     * 수행자별 로그 수 조회
     */
    @Query("SELECT al.performedBy, COUNT(al) FROM ApplicationLog al GROUP BY al.performedBy")
    List<Object[]> countByPerformedBy();
    
    /**
     * 신청별 로그 수 조회
     */
    @Query("SELECT al.applicationId, COUNT(al) FROM ApplicationLog al GROUP BY al.applicationId")
    List<Object[]> countByApplication();
    
    /**
     * 최근 로그 조회
     */
    @Query("SELECT al FROM ApplicationLog al ORDER BY al.performedAt DESC")
    List<ApplicationLog> findRecentLogs(Pageable pageable);
    
    /**
     * 총 로그 수 조회
     */
    @Query("SELECT COUNT(al) FROM ApplicationLog al")
    Long getTotalLogCount();
    
    /**
     * 특정 신청의 특정 액션 로그 조회
     */
    @Query("SELECT al FROM ApplicationLog al WHERE al.applicationId = :applicationId AND al.action = :action")
    List<ApplicationLog> findByApplicationIdAndAction(@Param("applicationId") Long applicationId, 
                                                      @Param("action") String action);
}

