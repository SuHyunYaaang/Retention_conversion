package com.retention.backend.repository;

import com.retention.backend.model.Customer;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 고객 Repository 인터페이스
 */
@Repository
public interface CustomerRepository extends JpaRepository<Customer, Long> {
    
    /**
     * 고객 ID로 고객 조회
     */
    Optional<Customer> findByCustomerId(String customerId);
    
    /**
     * 전화번호로 고객 조회
     */
    Optional<Customer> findByPhone(String phone);
    
    /**
     * 이메일로 고객 조회
     */
    Optional<Customer> findByEmail(String email);
    
    /**
     * 이름으로 고객 검색
     */
    List<Customer> findByNameContainingIgnoreCase(String name);
    
    /**
     * 신용등급으로 고객 조회
     */
    List<Customer> findByCreditGrade(String creditGrade);
    
    /**
     * 소득수준으로 고객 조회
     */
    List<Customer> findByIncomeLevel(String incomeLevel);
    
    /**
     * 고객 ID로 고객 존재 여부 확인
     */
    boolean existsByCustomerId(String customerId);
    
    /**
     * 전화번호로 고객 존재 여부 확인
     */
    boolean existsByPhone(String phone);
    
    /**
     * 이메일로 고객 존재 여부 확인
     */
    boolean existsByEmail(String email);
    
    /**
     * 페이징된 고객 목록 조회
     */
    Page<Customer> findAll(Pageable pageable);
    
    /**
     * 이름으로 페이징된 고객 검색
     */
    Page<Customer> findByNameContainingIgnoreCase(String name, Pageable pageable);
    
    /**
     * 신용등급별 고객 수 조회
     */
    @Query("SELECT c.creditGrade, COUNT(c) FROM Customer c GROUP BY c.creditGrade")
    List<Object[]> countByCreditGrade();
    
    /**
     * 소득수준별 고객 수 조회
     */
    @Query("SELECT c.incomeLevel, COUNT(c) FROM Customer c GROUP BY c.incomeLevel")
    List<Object[]> countByIncomeLevel();
    
    /**
     * 최근 가입 고객 조회
     */
    @Query("SELECT c FROM Customer c ORDER BY c.createdAt DESC")
    List<Customer> findRecentCustomers(Pageable pageable);
}

