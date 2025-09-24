package com.retention.backend.repository;

import com.retention.backend.model.RefinanceApplication;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

/**
 * 재대출 신청 Repository 인터페이스
 */
@Repository
public interface RefinanceApplicationRepository extends JpaRepository<RefinanceApplication, Long> {
    
    /**
     * 신청 번호로 재대출 신청 조회
     */
    Optional<RefinanceApplication> findByApplicationNumber(String applicationNumber);
    
    /**
     * 고객 ID로 재대출 신청 목록 조회
     */
    List<RefinanceApplication> findByCustomerId(Long customerId);
    
    /**
     * 원본 대출 ID로 재대출 신청 목록 조회
     */
    List<RefinanceApplication> findByOriginalLoanId(Long originalLoanId);
    
    /**
     * 신청 상태로 재대출 신청 목록 조회
     */
    List<RefinanceApplication> findByApplicationStatus(String applicationStatus);
    
    /**
     * 특정 기간 내 재대출 신청 목록 조회
     */
    @Query("SELECT ra FROM RefinanceApplication ra WHERE ra.applicationDate BETWEEN :startDate AND :endDate")
    List<RefinanceApplication> findApplicationsByDateRange(@Param("startDate") LocalDateTime startDate, 
                                                          @Param("endDate") LocalDateTime endDate);
    
    /**
     * 대기 중인 재대출 신청 목록 조회
     */
    @Query("SELECT ra FROM RefinanceApplication ra WHERE ra.applicationStatus = 'pending'")
    List<RefinanceApplication> findPendingApplications();
    
    /**
     * 승인된 재대출 신청 목록 조회
     */
    @Query("SELECT ra FROM RefinanceApplication ra WHERE ra.applicationStatus = 'approved'")
    List<RefinanceApplication> findApprovedApplications();
    
    /**
     * 거절된 재대출 신청 목록 조회
     */
    @Query("SELECT ra FROM RefinanceApplication ra WHERE ra.applicationStatus = 'rejected'")
    List<RefinanceApplication> findRejectedApplications();
    
    /**
     * 처리 중인 재대출 신청 목록 조회
     */
    @Query("SELECT ra FROM RefinanceApplication ra WHERE ra.applicationStatus = 'processing'")
    List<RefinanceApplication> findProcessingApplications();
    
    /**
     * 페이징된 재대출 신청 목록 조회
     */
    Page<RefinanceApplication> findAll(Pageable pageable);
    
    /**
     * 고객 ID로 페이징된 재대출 신청 목록 조회
     */
    Page<RefinanceApplication> findByCustomerId(Long customerId, Pageable pageable);
    
    /**
     * 신청 상태로 페이징된 재대출 신청 목록 조회
     */
    Page<RefinanceApplication> findByApplicationStatus(String applicationStatus, Pageable pageable);
    
    /**
     * 신청 상태별 재대출 신청 수 조회
     */
    @Query("SELECT ra.applicationStatus, COUNT(ra) FROM RefinanceApplication ra GROUP BY ra.applicationStatus")
    List<Object[]> countByApplicationStatus();
    
    /**
     * 월별 재대출 신청 수 조회
     */
    @Query("SELECT YEAR(ra.applicationDate), MONTH(ra.applicationDate), COUNT(ra) " +
           "FROM RefinanceApplication ra " +
           "GROUP BY YEAR(ra.applicationDate), MONTH(ra.applicationDate) " +
           "ORDER BY YEAR(ra.applicationDate), MONTH(ra.applicationDate)")
    List<Object[]> countByMonth();
    
    /**
     * 평균 신청 금액 조회
     */
    @Query("SELECT AVG(ra.requestedAmount) FROM RefinanceApplication ra")
    Double getAverageRequestedAmount();
    
    /**
     * 총 신청 금액 조회
     */
    @Query("SELECT SUM(ra.requestedAmount) FROM RefinanceApplication ra")
    Double getTotalRequestedAmount();
    
    /**
     * 승인율 조회
     */
    @Query("SELECT COUNT(ra) FROM RefinanceApplication ra WHERE ra.applicationStatus = 'approved'")
    Long countApprovedApplications();
    
    /**
     * 최근 재대출 신청 조회
     */
    @Query("SELECT ra FROM RefinanceApplication ra ORDER BY ra.createdAt DESC")
    List<RefinanceApplication> findRecentApplications(Pageable pageable);
    
    /**
     * 고객별 재대출 신청 수 조회
     */
    @Query("SELECT ra.customerId, COUNT(ra) FROM RefinanceApplication ra GROUP BY ra.customerId")
    List<Object[]> countByCustomer();
}

