package com.banking.rca_backend.dto;

import java.util.List;

public record RcaAnalysisResponse(
        String question,
        String rootCause,
        String symptom,
        String impactedService,
        List<String> evidence,
        List<String> suggestedFix,
        List<String> retrievedEvidence
) {}