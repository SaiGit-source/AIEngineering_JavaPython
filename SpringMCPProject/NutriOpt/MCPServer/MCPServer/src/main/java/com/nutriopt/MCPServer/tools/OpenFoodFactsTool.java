package com.nutriopt.MCPServer.tools;

import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.LinkedHashMap;
import java.util.Map;

@Component
public class OpenFoodFactsTool {

    private final WebClient webClient;

    public OpenFoodFactsTool(
            WebClient.Builder webClientBuilder,
            @Value("${nutriopt.openfoodfacts.base-url}") String baseUrl,
            @Value("${nutriopt.openfoodfacts.user-agent}") String userAgent
    ) {
        this.webClient = webClientBuilder
                .baseUrl(baseUrl)
                .defaultHeader("User-Agent", userAgent)
                .build();
    }

    @Tool(description = "Retrieve nutrition facts from OpenFoodFacts using a product barcode.")
    public Map<String, Object> getNutritionFactsByBarcode(
            @ToolParam(description = "Product barcode, for example 3017624010701")
            String barcode
    ) {
        JsonNode response = webClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/api/v2/product/{barcode}")
                        .queryParam(
                                "fields",
                                "code,status,status_verbose,product_name,brands,nutriments,nutrition_grades,image_front_url"
                        )
                        .build(barcode)
                )
                .retrieve()
                .bodyToMono(JsonNode.class)
                .block();

        if (response == null) {
            return errorResponse(barcode, "No response received from OpenFoodFacts.");
        }

        int status = response.path("status").asInt(0);

        if (status != 1) {
            String message = response.path("status_verbose").asText("Product not found.");
            return errorResponse(barcode, message);
        }

        JsonNode product = response.path("product");
        JsonNode nutriments = product.path("nutriments");

        Map<String, Object> result = new LinkedHashMap<>();

        result.put("barcode", response.path("code").asText(barcode));
        result.put("productName", product.path("product_name").asText("Unknown product"));
        result.put("brand", product.path("brands").asText("Unknown brand"));

        result.put("caloriesPer100g", getDoubleOrNull(nutriments, "energy-kcal_100g"));
        result.put("proteinPer100g", getDoubleOrNull(nutriments, "proteins_100g"));
        result.put("carbsPer100g", getDoubleOrNull(nutriments, "carbohydrates_100g"));
        result.put("fatPer100g", getDoubleOrNull(nutriments, "fat_100g"));
        result.put("fiberPer100g", getDoubleOrNull(nutriments, "fiber_100g"));
        result.put("sugarsPer100g", getDoubleOrNull(nutriments, "sugars_100g"));
        result.put("saltPer100g", getDoubleOrNull(nutriments, "salt_100g"));

        result.put("nutriScore", product.path("nutrition_grades").asText("unknown"));
        result.put("imageUrl", product.path("image_front_url").asText(null));
        result.put("source", "OpenFoodFacts");

        return result;
    }

    private Double getDoubleOrNull(JsonNode node, String fieldName) {
        JsonNode value = node.get(fieldName);

        if (value == null || value.isNull() || !value.isNumber()) {
            return null;
        }

        return value.asDouble();
    }

    private Map<String, Object> errorResponse(String barcode, String message) {
        Map<String, Object> error = new LinkedHashMap<>();
        error.put("barcode", barcode);
        error.put("success", false);
        error.put("message", message);
        error.put("source", "OpenFoodFacts");
        return error;
    }
}