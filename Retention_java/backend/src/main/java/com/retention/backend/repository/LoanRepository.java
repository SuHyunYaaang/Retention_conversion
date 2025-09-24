package com.retention.backend.repository;

import com.retention.backend.model.Loan;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 대출 Repository 인터페이스
 */
@Repository
public interface LoanRepository extends JpaRepository<Loan, Long> {
    
    /**
     * 대출 ID로 대출 조회
     */
    Optional<Loan> findByLoanId(String loanId);
    
    /**
     * 고객 ID로 대출 목록 조회
     */
    List<Loan> findByCustomerId(String customerId);
    
    /**
     * 고객 ID로 활성 대출 목록 조회
     */
    @Query("SELECT l FROM Loan l WHERE l.customerId = :customerId AND l.status IN ('active', 'approved', 'disbursed')")
    List<Loan> findActiveLoansByCustomerId(@Param("customerId") String customerId);
    
    /**
     * 대출 상태로 대출 목록 조회
     */
    List<Loan> findByStatus(String status);
    
    /**
     * 대출 유형으로 대출 목록 조회
     */
    List<Loan> findByLoanType(String loanType);
    
    /**
     * 연체 대출 목록 조회
     */
    @Query("SELECT l FROM Loan l WHERE l.overdueDays > 0")
    List<Loan> findOverdueLoans();
    
    /**
     * 특정 기간 내 대출 목록 조회
     */
    @Query("SELECT l FROM Loan l WHERE l.applicationDate BETWEEN :startDate AND :endDate")
    List<Loan> findLoansByDateRange(@Param("startDate") java.time.LocalDateTime startDate, 
                                   @Param("endDate") java.time.LocalDateTime endDate);
    
    /**
     * 대출 금액 범위로 대출 목록 조회
     */
    @Query("SELECT l FROM Loan l WHERE l.loanAmount BETWEEN :minAmount AND :maxAmount")
    List<Loan> findLoansByAmountRange(@Param("minAmount") Integer minAmount, 
                                     @Param("maxAmount") Integer maxAmount);
    
    /**
     * 페이징된 대출 목록 조회
     */
    Page<Loan> findAll(Pageable pageable);
    
    /**
     * 고객 ID로 페이징된 대출 목록 조회
     */
    Page<Loan> findByCustomerId(String customerId, Pageable pageable);
    
    /**
     * 대출 상태별 대출 수 조회
     */
    @Query("SELECT l.status, COUNT(l) FROM Loan l GROUP BY l.status")
    List<Object[]> countByStatus();
    
    /**
     * 대출 유형별 대출 수 조회
     */
    @Query("SELECT l.loanType, COUNT(l) FROM Loan l GROUP BY l.loanType")
    List<Object[]> countByLoanType();
    
    /**
     * 평균 대출 금액 조회
     */
    @Query("SELECT AVG(l.loanAmount) FROM Loan l")
    Double getAverageLoanAmount();
    
    /**
     * 총 대출 금액 조회
     */
    @Query("SELECT SUM(l.loanAmount) FROM Loan l")
    Long getTotalLoanAmount();
    
    /**
     * 연체율 조회
     */
    @Query("SELECT COUNT(l) FROM Loan l WHERE l.overdueDays > 0")
    Long countOverdueLoans();
    
    /**
     * 최근 대출 조회
     */
    @Query("SELECT l FROM Loan l ORDER BY l.createdAt DESC")
    List<Loan> findRecentLoans(Pageable pageable);
}

