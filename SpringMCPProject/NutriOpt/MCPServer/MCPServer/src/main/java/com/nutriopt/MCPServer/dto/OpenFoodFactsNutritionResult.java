package com.nutriopt.MCPServer.dto;

public record OpenFoodFactsNutritionResult(
        String barcode,
        String productName,
        String brand,
        Double caloriesPer100g,
        Double proteinPer100g,
        Double carbsPer100g,
        Double fatPer100g,
        Double fiberPer100g,
        Double sugarsPer100g,
        Double saltPer100g,
        String nutriScore,
        String imageUrl,
        String source
) {
}