package com.nutriopt.MCPServer.dto;

public record MacroTargets(
        double caloriesMin,
        double caloriesMax,
        double proteinMin,
        double carbsMin,
        double carbsMax,
        double fatMin,
        double fatMax,
        double fiberMin,
        double budgetMax
) {
}