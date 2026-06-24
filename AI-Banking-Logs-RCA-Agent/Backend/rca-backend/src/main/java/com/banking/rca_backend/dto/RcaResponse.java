package com.banking.rca_backend.dto;

import java.util.List;

public record RcaResponse(
        String question,
        String answer,
        List<String> evidence
) {}