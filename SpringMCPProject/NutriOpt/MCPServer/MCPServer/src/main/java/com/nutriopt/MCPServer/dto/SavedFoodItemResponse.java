package com.nutriopt.MCPServer.dto;

public record SavedFoodItemResponse(
        Long id,
        String name,
        String genericName,
        String brand,
        String barcode,
        Double caloriesPer100g,
        Double proteinPer100g,
        Double costPer100g,
        String status
) {
}