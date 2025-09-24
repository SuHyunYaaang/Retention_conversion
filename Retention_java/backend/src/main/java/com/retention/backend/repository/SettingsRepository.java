package com.retention.backend.repository;

import com.retention.backend.model.Settings;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 설정 Repository 인터페이스
 */
@Repository
public interface SettingsRepository extends JpaRepository<Settings, Long> {
    
    /**
     * 설정 키로 설정 조회
     */
    Optional<Settings> findBySettingKey(String settingKey);
    
    /**
     * 활성 설정 목록 조회
     */
    List<Settings> findByIsActiveTrue();
    
    /**
     * 비활성 설정 목록 조회
     */
    List<Settings> findByIsActiveFalse();
    
    /**
     * 설정 키로 활성 설정 조회
     */
    @Query("SELECT s FROM Settings s WHERE s.settingKey = :settingKey AND s.isActive = true")
    Optional<Settings> findActiveBySettingKey(@Param("settingKey") String settingKey);
    
    /**
     * 설정 키 존재 여부 확인
     */
    boolean existsBySettingKey(String settingKey);
    
    /**
     * 활성 설정 수 조회
     */
    @Query("SELECT COUNT(s) FROM Settings s WHERE s.isActive = true")
    Long countActiveSettings();
    
    /**
     * 비활성 설정 수 조회
     */
    @Query("SELECT COUNT(s) FROM Settings s WHERE s.isActive = false")
    Long countInactiveSettings();
    
    /**
     * 최근 생성된 설정 조회
     */
    @Query("SELECT s FROM Settings s ORDER BY s.createdAt DESC")
    List<Settings> findRecentSettings(org.springframework.data.domain.Pageable pageable);
}

