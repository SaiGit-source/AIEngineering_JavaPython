package com.banking.rca_backend.controller;

import com.banking.rca_backend.dto.RcaAnalysisResponse;
import com.banking.rca_backend.dto.RcaRequest;
import com.banking.rca_backend.dto.RcaResponse;
import com.banking.rca_backend.service.RcaService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/rca")
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:5173")
public class RcaController {

    private final RcaService rcaService;

    @PostMapping("/search")
    public RcaResponse search(@Valid @RequestBody RcaRequest request) {
        return rcaService.searchEvidence(request.question());
    }

    @PostMapping("/analyze")
    public RcaAnalysisResponse analyze(@Valid @RequestBody RcaRequest request) {
        return rcaService.analyzeRca(request.question());
    }
}