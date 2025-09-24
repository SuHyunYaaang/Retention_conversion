package com.retention.backend.service;

import com.retention.backend.dto.CustomerDto;
import com.retention.backend.model.Customer;
import com.retention.backend.repository.CustomerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

/**
 * 고객 서비스 클래스
 */
@Service
@Transactional
public class CustomerService {
    
    @Autowired
    private CustomerRepository customerRepository;
    
    /**
     * 고객 생성
     */
    public Customer createCustomer(CustomerDto.Create createDto) {
        // 고객 ID 중복 확인
        if (customerRepository.existsByCustomerId(createDto.getCustomerId())) {
            throw new IllegalArgumentException("이미 존재하는 고객 ID입니다: " + createDto.getCustomerId());
        }
        
        // 전화번호 중복 확인
        if (customerRepository.existsByPhone(createDto.getPhone())) {
            throw new IllegalArgumentException("이미 존재하는 전화번호입니다: " + createDto.getPhone());
        }
        
        // 이메일 중복 확인 (이메일이 제공된 경우)
        if (createDto.getEmail() != null && !createDto.getEmail().isEmpty() && 
            customerRepository.existsByEmail(createDto.getEmail())) {
            throw new IllegalArgumentException("이미 존재하는 이메일입니다: " + createDto.getEmail());
        }
        
        Customer customer = new Customer();
        customer.setCustomerId(createDto.getCustomerId());
        customer.setName(createDto.getName());
        customer.setPhone(createDto.getPhone());
        customer.setEmail(createDto.getEmail());
        customer.setAge(createDto.getAge());
        customer.setJobType(createDto.getJobType());
        customer.setIncomeLevel(createDto.getIncomeLevel());
        customer.setCreditGrade(createDto.getCreditGrade());
        customer.setAddress(createDto.getAddress());
        
        return customerRepository.save(customer);
    }
    
    /**
     * 고객 조회 (ID)
     */
    @Transactional(readOnly = true)
    public Optional<Customer> getCustomerById(Long id) {
        return customerRepository.findById(id);
    }
    
    /**
     * 고객 조회 (고객 ID)
     */
    @Transactional(readOnly = true)
    public Optional<Customer> getCustomerByCustomerId(String customerId) {
        return customerRepository.findByCustomerId(customerId);
    }
    
    /**
     * 고객 목록 조회 (페이징)
     */
    @Transactional(readOnly = true)
    public Page<Customer> getCustomers(Pageable pageable) {
        return customerRepository.findAll(pageable);
    }
    
    /**
     * 고객 검색 (이름)
     */
    @Transactional(readOnly = true)
    public List<Customer> searchCustomersByName(String name) {
        return customerRepository.findByNameContainingIgnoreCase(name);
    }
    
    /**
     * 고객 검색 (이름, 페이징)
     */
    @Transactional(readOnly = true)
    public Page<Customer> searchCustomersByName(String name, Pageable pageable) {
        return customerRepository.findByNameContainingIgnoreCase(name, pageable);
    }
    
    /**
     * 신용등급별 고객 조회
     */
    @Transactional(readOnly = true)
    public List<Customer> getCustomersByCreditGrade(String creditGrade) {
        return customerRepository.findByCreditGrade(creditGrade);
    }
    
    /**
     * 소득수준별 고객 조회
     */
    @Transactional(readOnly = true)
    public List<Customer> getCustomersByIncomeLevel(String incomeLevel) {
        return customerRepository.findByIncomeLevel(incomeLevel);
    }
    
    /**
     * 고객 정보 수정
     */
    public Customer updateCustomer(Long id, CustomerDto.Update updateDto) {
        Customer customer = customerRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("고객을 찾을 수 없습니다: " + id));
        
        // 전화번호 중복 확인 (다른 고객이 사용 중인지)
        if (updateDto.getPhone() != null && !updateDto.getPhone().equals(customer.getPhone())) {
            Optional<Customer> existingCustomer = customerRepository.findByPhone(updateDto.getPhone());
            if (existingCustomer.isPresent() && !existingCustomer.get().getId().equals(id)) {
                throw new IllegalArgumentException("이미 존재하는 전화번호입니다: " + updateDto.getPhone());
            }
        }
        
        // 이메일 중복 확인 (다른 고객이 사용 중인지)
        if (updateDto.getEmail() != null && !updateDto.getEmail().equals(customer.getEmail())) {
            Optional<Customer> existingCustomer = customerRepository.findByEmail(updateDto.getEmail());
            if (existingCustomer.isPresent() && !existingCustomer.get().getId().equals(id)) {
                throw new IllegalArgumentException("이미 존재하는 이메일입니다: " + updateDto.getEmail());
            }
        }
        
        // 필드 업데이트
        if (updateDto.getName() != null) customer.setName(updateDto.getName());
        if (updateDto.getPhone() != null) customer.setPhone(updateDto.getPhone());
        if (updateDto.getEmail() != null) customer.setEmail(updateDto.getEmail());
        if (updateDto.getAge() != null) customer.setAge(updateDto.getAge());
        if (updateDto.getJobType() != null) customer.setJobType(updateDto.getJobType());
        if (updateDto.getIncomeLevel() != null) customer.setIncomeLevel(updateDto.getIncomeLevel());
        if (updateDto.getCreditGrade() != null) customer.setCreditGrade(updateDto.getCreditGrade());
        if (updateDto.getAddress() != null) customer.setAddress(updateDto.getAddress());
        
        return customerRepository.save(customer);
    }
    
    /**
     * 고객 삭제
     */
    public void deleteCustomer(Long id) {
        if (!customerRepository.existsById(id)) {
            throw new IllegalArgumentException("고객을 찾을 수 없습니다: " + id);
        }
        customerRepository.deleteById(id);
    }
    
    /**
     * 고객 존재 여부 확인
     */
    @Transactional(readOnly = true)
    public boolean existsByCustomerId(String customerId) {
        return customerRepository.existsByCustomerId(customerId);
    }
    
    /**
     * 고객 통계 조회
     */
    @Transactional(readOnly = true)
    public List<Object[]> getCustomerStatistics() {
        return customerRepository.countByCreditGrade();
    }
    
    /**
     * 소득수준별 통계 조회
     */
    @Transactional(readOnly = true)
    public List<Object[]> getIncomeLevelStatistics() {
        return customerRepository.countByIncomeLevel();
    }
    
    /**
     * 최근 가입 고객 조회
     */
    @Transactional(readOnly = true)
    public List<Customer> getRecentCustomers(Pageable pageable) {
        return customerRepository.findRecentCustomers(pageable);
    }
}

