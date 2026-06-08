package com.nutriopt.MCPServer.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;

@Entity
@Table(name = "food_items")
@Getter
@Setter
public class FoodItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String genericName;
    private String brand;
    private String barcode;

    private String quantityText;
    private Double packageSizeGrams;

    private Double caloriesPer100g;
    private Double proteinPer100g;
    private Double carbsPer100g;
    private Double fatPer100g;
    private Double fiberPer100g;

    private Double latestPrice;
    private String currency;
    private Double costPer100g;
    private String priceSource;
    private LocalDate priceDate;

    private Double minGrams;
    private Double maxGrams;
}