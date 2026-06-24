package com.banking.rca_backend.dto;

import jakarta.validation.constraints.NotBlank;

public record RcaRequest(
        @NotBlank(message = "Question is required")
        String question
) {}