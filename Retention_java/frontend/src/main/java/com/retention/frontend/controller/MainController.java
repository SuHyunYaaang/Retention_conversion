package com.retention.frontend.controller;

import com.retention.frontend.service.BackendApiService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.Map;

/**
 * 메인 컨트롤러
 * Next.js의 페이지들과 동일한 기능을 제공
 */
@Controller
@RequestMapping("/")
public class MainController {
    
    @Autowired
    private BackendApiService backendApiService;
    
    /**
     * 메인 페이지 (Next.js의 page.tsx와 동일)
     */
    @GetMapping("/")
    public String index(Model model) {
        try {
            // 대시보드 데이터 조회
            Map<String, Object> dashboardData = backendApiService.getDashboardData();
            model.addAttribute("dashboardData", dashboardData);
        } catch (Exception e) {
            model.addAttribute("error", "대시보드 데이터를 불러올 수 없습니다: " + e.getMessage());
        }
        return "index";
    }
    
    /**
     * 고객 관리 페이지 (Next.js의 customers/page.tsx와 동일)
     */
    @GetMapping("/customers")
    public String customers(Model model) {
        try {
            // 고객 목록 조회
            Map<String, Object> customersData = backendApiService.getCustomers();
            model.addAttribute("customersData", customersData);
        } catch (Exception e) {
            model.addAttribute("error", "고객 데이터를 불러올 수 없습니다: " + e.getMessage());
        }
        return "customers";
    }
    
    /**
     * 대출 관리 페이지 (Next.js의 loans/page.tsx와 동일)
     */
    @GetMapping("/loans")
    public String loans(Model model) {
        try {
            // 대출 목록 조회
            Map<String, Object> loansData = backendApiService.getLoans();
            model.addAttribute("loansData", loansData);
        } catch (Exception e) {
            model.addAttribute("error", "대출 데이터를 불러올 수 없습니다: " + e.getMessage());
        }
        return "loans";
    }
    
    /**
     * ML 대시보드 페이지 (Next.js의 ml_dashboard/page.tsx와 동일)
     */
    @GetMapping("/ml-dashboard")
    public String mlDashboard(Model model) {
        try {
            // ML 예측 데이터 조회
            Map<String, Object> mlData = backendApiService.getMlPredictions();
            model.addAttribute("mlData", mlData);
        } catch (Exception e) {
            model.addAttribute("error", "ML 데이터를 불러올 수 없습니다: " + e.getMessage());
        }
        return "ml-dashboard";
    }
    
    /**
     * 설정 페이지 (Next.js의 settings/page.tsx와 동일)
     */
    @GetMapping("/settings")
    public String settings(Model model) {
        return "settings";
    }
}

