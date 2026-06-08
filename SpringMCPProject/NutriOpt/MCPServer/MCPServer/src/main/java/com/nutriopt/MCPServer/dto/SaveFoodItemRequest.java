package com.nutriopt.MCPServer.dto;

import java.time.LocalDate;

public record SaveFoodItemRequest(
        String name,
        String genericName,
        String brand,
        String barcode,

        String quantityText,
        Double packageSizeGrams,

        Double caloriesPer100g,
        Double proteinPer100g,
        Double carbsPer100g,
        Double fatPer100g,
        Double fiberPer100g,

        Double latestPrice,
        String currency,
        Double costPer100g,
        String priceSource,
        LocalDate priceDate,

        Double minGrams,
        Double maxGrams
) {
}