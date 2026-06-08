package com.nutriopt.MCPServer.tools;

import com.nutriopt.MCPServer.dto.SaveFoodItemRequest;
import com.nutriopt.MCPServer.dto.SavedFoodItemResponse;
import com.nutriopt.MCPServer.model.FoodItem;
import com.nutriopt.MCPServer.repo.FoodItemRepo;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;

import java.util.List;

//@Component
public class FoodStorageTool {

    private final FoodItemRepo foodItemRepository;

    public FoodStorageTool(FoodItemRepo foodItemRepository) {
        this.foodItemRepository = foodItemRepository;
    }

    @Tool(description = "Save one or more food items with nutrition and price information into MariaDB. If a barcode already exists, update the existing food item. Returns saved food IDs.")
    public List<SavedFoodItemResponse> saveFoodItems(List<SaveFoodItemRequest> requests) {

        if (requests == null || requests.isEmpty()) {
            return List.of();
        }

        return requests.stream()
                .map(this::saveOrUpdateFoodItem)
                .toList();
        
        /* OR
		List<SavedFoodItemResponse> responses = new ArrayList<>();
		
		for (SaveFoodItemRequest request : requests) {
		    SavedFoodItemResponse response = saveOrUpdateFoodItem(request);
		    responses.add(response);
		}
		
		return responses;
         */
    }
    

    @Tool(description = "Find saved food items in MariaDB by food name. Useful before saving a duplicate food item.")
    public List<SavedFoodItemResponse> findSavedFoodsByName(String name) {

        if (name == null || name.isBlank()) {
            return List.of();
        }

        return foodItemRepository.findByNameContainingIgnoreCase(name)
                .stream()
                .map(food -> toResponse(food, "FOUND"))
                .toList();
    }

    @Tool(description = "List all saved food items from MariaDB with their IDs. Use these IDs when calling the LP optimizer.")
    public List<SavedFoodItemResponse> listSavedFoods() {

        return foodItemRepository.findAll()
                .stream()
                .map(food -> toResponse(food, "FOUND"))
                .toList();
    }

    private SavedFoodItemResponse saveOrUpdateFoodItem(SaveFoodItemRequest request) {

        FoodItem foodItem = findExistingFoodItem(request);

        boolean isNew = foodItem.getId() == null;

        foodItem.setName(request.name());
        foodItem.setGenericName(request.genericName());
        foodItem.setBrand(request.brand());
        foodItem.setBarcode(request.barcode());

        foodItem.setQuantityText(request.quantityText());
        foodItem.setPackageSizeGrams(request.packageSizeGrams());

        foodItem.setCaloriesPer100g(request.caloriesPer100g());
        foodItem.setProteinPer100g(request.proteinPer100g());
        foodItem.setCarbsPer100g(request.carbsPer100g());
        foodItem.setFatPer100g(request.fatPer100g());
        foodItem.setFiberPer100g(request.fiberPer100g());

        foodItem.setLatestPrice(request.latestPrice());
        foodItem.setCurrency(request.currency());

        Double costPer100g = request.costPer100g();

        if (costPer100g == null
                && request.latestPrice() != null
                && request.packageSizeGrams() != null
                && request.packageSizeGrams() > 0) {

            costPer100g = request.latestPrice() / request.packageSizeGrams() * 100.0;
        }

        foodItem.setCostPer100g(costPer100g);
        foodItem.setPriceSource(request.priceSource());
        foodItem.setPriceDate(request.priceDate());

        foodItem.setMinGrams(request.minGrams() == null ? 0.0 : request.minGrams());
        foodItem.setMaxGrams(request.maxGrams() == null ? 1000.0 : request.maxGrams());

        FoodItem saved = foodItemRepository.save(foodItem); // saving entity here

        return toResponse(saved, isNew ? "SAVED" : "UPDATED");
    }

    private FoodItem findExistingFoodItem(SaveFoodItemRequest request) {

        if (request.barcode() != null && !request.barcode().isBlank()) {
            return foodItemRepository.findByBarcode(request.barcode())
                    .orElseGet(FoodItem::new);
        }

        return new FoodItem();
    }

    private SavedFoodItemResponse toResponse(FoodItem food, String status) {

        return new SavedFoodItemResponse(
                food.getId(),
                food.getName(),
                food.getGenericName(),
                food.getBrand(),
                food.getBarcode(),
                food.getCaloriesPer100g(),
                food.getProteinPer100g(),
                food.getCostPer100g(),
                status
        );
    }
}