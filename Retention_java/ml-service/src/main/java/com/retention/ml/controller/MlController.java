package com.retention.ml.controller;

import com.retention.ml.service.MlService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 머신러닝 서비스 컨트롤러
 * Python의 churn-ga-xgb.py와 동일한 기능을 제공
 */
@RestController
@RequestMapping("/api/ml")
@CrossOrigin(origins = "*")
public class MlController {
    
    @Autowired
    private MlService mlService;
    
    /**
     * 모델 학습 실행
     */
    @PostMapping("/train")
    public ResponseEntity<Map<String, Object>> trainModel(@RequestBody Map<String, Object> request) {
        try {
            String csvPath = (String) request.getOrDefault("csvPath", "data/churn_data.csv");
            String targetColumn = (String) request.getOrDefault("targetColumn", "churn");
            Double testSize = Double.valueOf(request.getOrDefault("testSize", 0.2).toString());
            Integer kfold = Integer.valueOf(request.getOrDefault("kfold", 5).toString());
            Integer generations = Integer.valueOf(request.getOrDefault("generations", 20).toString());
            Integer population = Integer.valueOf(request.getOrDefault("population", 36).toString());
            Double precisionK = Double.valueOf(request.getOrDefault("precisionK", 0.1).toString());
            String outdir = (String) request.getOrDefault("outdir", "outputs");
            String scoring = (String) request.getOrDefault("scoring", "pr_auc");
            
            Map<String, Object> result = mlService.trainModel(
                csvPath, targetColumn, testSize, kfold, generations, 
                population, precisionK, outdir, scoring
            );
            
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 모델 예측
     */
    @PostMapping("/predict")
    public ResponseEntity<Map<String, Object>> predict(@RequestBody Map<String, Object> data) {
        try {
            Map<String, Object> result = mlService.predict(data);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 모델 성능 지표 조회
     */
    @GetMapping("/metrics")
    public ResponseEntity<Map<String, Object>> getMetrics() {
        try {
            Map<String, Object> metrics = mlService.getMetrics();
            return ResponseEntity.ok(metrics);
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 모델 상태 조회
     */
    @GetMapping("/status")
    public ResponseEntity<Map<String, Object>> getStatus() {
        try {
            Map<String, Object> status = mlService.getStatus();
            return ResponseEntity.ok(status);
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 리포트 생성
     */
    @PostMapping("/report")
    public ResponseEntity<Map<String, Object>> generateReport() {
        try {
            Map<String, Object> report = mlService.generateReport();
            return ResponseEntity.ok(report);
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 헬스 체크
     */
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> healthCheck() {
        Map<String, String> health = Map.of(
            "status", "UP",
            "service", "Retention ML Service",
            "version", "1.0.0"
        );
        return ResponseEntity.ok(health);
    }
}

