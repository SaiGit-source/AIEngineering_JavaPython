package com.nutriopt.MCPServer.dto;

import java.util.List;

// Input to LP tool
public record DietOptimizationRequest(
        MacroTargets targets,
        List<Long> foodIds
) {
}