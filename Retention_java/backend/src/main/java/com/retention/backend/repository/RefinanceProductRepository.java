package com.retention.backend.repository;

import com.retention.backend.model.RefinanceProduct;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 재대출 상품 Repository 인터페이스
 */
@Repository
public interface RefinanceProductRepository extends JpaRepository<RefinanceProduct, Long> {
    
    /**
     * 상품 코드로 재대출 상품 조회
     */
    Optional<RefinanceProduct> findByProductCode(String productCode);
    
    /**
     * 활성 상품 목록 조회
     */
    List<RefinanceProduct> findByIsActiveTrue();
    
    /**
     * 비활성 상품 목록 조회
     */
    List<RefinanceProduct> findByIsActiveFalse();
    
    /**
     * 상품명으로 상품 검색
     */
    List<RefinanceProduct> findByProductNameContainingIgnoreCase(String productName);
    
    /**
     * 금리 범위로 상품 조회
     */
    @Query("SELECT rp FROM RefinanceProduct rp WHERE rp.minInterestRate <= :interestRate AND rp.maxInterestRate >= :interestRate")
    List<RefinanceProduct> findByInterestRateRange(@Param("interestRate") Double interestRate);
    
    /**
     * 대출 금액 범위로 상품 조회
     */
    @Query("SELECT rp FROM RefinanceProduct rp WHERE rp.minLoanAmount <= :loanAmount AND rp.maxLoanAmount >= :loanAmount")
    List<RefinanceProduct> findByLoanAmountRange(@Param("loanAmount") Double loanAmount);
    
    /**
     * 대출 기간 범위로 상품 조회
     */
    @Query("SELECT rp FROM RefinanceProduct rp WHERE rp.loanTermMin <= :loanTerm AND rp.loanTermMax >= :loanTerm")
    List<RefinanceProduct> findByLoanTermRange(@Param("loanTerm") Integer loanTerm);
    
    /**
     * 조건에 맞는 상품 조회 (금리, 대출금액, 대출기간)
     */
    @Query("SELECT rp FROM RefinanceProduct rp WHERE " +
           "rp.isActive = true AND " +
           "rp.minInterestRate <= :interestRate AND rp.maxInterestRate >= :interestRate AND " +
           "rp.minLoanAmount <= :loanAmount AND rp.maxLoanAmount >= :loanAmount AND " +
           "rp.loanTermMin <= :loanTerm AND rp.loanTermMax >= :loanTerm")
    List<RefinanceProduct> findEligibleProducts(@Param("interestRate") Double interestRate,
                                               @Param("loanAmount") Double loanAmount,
                                               @Param("loanTerm") Integer loanTerm);
    
    /**
     * 최저 금리 상품 조회
     */
    @Query("SELECT rp FROM RefinanceProduct rp WHERE rp.isActive = true ORDER BY rp.minInterestRate ASC")
    List<RefinanceProduct> findLowestInterestRateProducts(Pageable pageable);
    
    /**
     * 최고 대출 한도 상품 조회
     */
    @Query("SELECT rp FROM RefinanceProduct rp WHERE rp.isActive = true ORDER BY rp.maxLoanAmount DESC")
    List<RefinanceProduct> findHighestLoanAmountProducts(Pageable pageable);
    
    /**
     * 페이징된 상품 목록 조회
     */
    Page<RefinanceProduct> findAll(Pageable pageable);
    
    /**
     * 활성 상품 페이징된 목록 조회
     */
    Page<RefinanceProduct> findByIsActiveTrue(Pageable pageable);
    
    /**
     * 상품명으로 페이징된 상품 검색
     */
    Page<RefinanceProduct> findByProductNameContainingIgnoreCase(String productName, Pageable pageable);
    
    /**
     * 활성 상품 수 조회
     */
    @Query("SELECT COUNT(rp) FROM RefinanceProduct rp WHERE rp.isActive = true")
    Long countActiveProducts();
    
    /**
     * 비활성 상품 수 조회
     */
    @Query("SELECT COUNT(rp) FROM RefinanceProduct rp WHERE rp.isActive = false")
    Long countInactiveProducts();
    
    /**
     * 평균 최저 금리 조회
     */
    @Query("SELECT AVG(rp.minInterestRate) FROM RefinanceProduct rp WHERE rp.isActive = true")
    Double getAverageMinInterestRate();
    
    /**
     * 평균 최고 금리 조회
     */
    @Query("SELECT AVG(rp.maxInterestRate) FROM RefinanceProduct rp WHERE rp.isActive = true")
    Double getAverageMaxInterestRate();
    
    /**
     * 최근 생성된 상품 조회
     */
    @Query("SELECT rp FROM RefinanceProduct rp ORDER BY rp.createdAt DESC")
    List<RefinanceProduct> findRecentProducts(Pageable pageable);
    
    /**
     * 상품 코드 존재 여부 확인
     */
    boolean existsByProductCode(String productCode);
}

