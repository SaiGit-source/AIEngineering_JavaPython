package com.banking.rca_backend.controller;

import com.banking.rca_backend.service.DashboardService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/dashboard")
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:5173")
public class DashboardController {

    private final DashboardService dashboardService;

    @GetMapping("/overview")
    public Map<String, Object> overview() {
        return dashboardService.getOverview();
    }
}