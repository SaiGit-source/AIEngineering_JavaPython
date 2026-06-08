package com.nutriopt.MCPServer.dto;

import java.util.List;

// Output from LP tool
public record DietOptimizationResult(
        String status,
        double totalCalories,
        double totalProtein,
        double totalCarbs,
        double totalFat,
        double totalFiber,
        double totalCost,
        List<OptimizedFoodItem> items
) {
}