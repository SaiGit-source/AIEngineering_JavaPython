package com.nutriopt.MCPServer.dto;


// One item in result
public record OptimizedFoodItem(
        Long foodId,
        String food,
        double quantity,
        String unit
) {
}