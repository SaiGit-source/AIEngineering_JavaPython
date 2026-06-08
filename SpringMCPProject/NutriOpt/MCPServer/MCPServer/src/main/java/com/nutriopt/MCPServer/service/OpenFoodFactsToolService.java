package com.nutriopt.MCPServer.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.nutriopt.MCPServer.dto.OpenFoodFactsNutritionResult;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class OpenFoodFactsToolService {

    private final WebClient webClient;

    public OpenFoodFactsToolService(
            WebClient.Builder webClientBuilder,
            @Value("${nutriopt.openfoodfacts.base-url}") String baseUrl
    ) {
        this.webClient = webClientBuilder
                .baseUrl(baseUrl)
                .defaultHeader(
                        "User-Agent",
                        "NutriOpt/1.0"
                )
                .build();
    }

    @Tool(description = "Retrieve nutrition facts from OpenFoodFacts using a product barcode.")
    public OpenFoodFactsNutritionResult getNutritionFactsByBarcode(
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
                        .build(barcode))
                .retrieve()
                .bodyToMono(JsonNode.class)
                .block();

        if (response == null) {
            throw new RuntimeException("No response from OpenFoodFacts.");
        }

        int status = response.path("status").asInt(0);

        if (status != 1) {
            String message = response.path("status_verbose").asText("Product not found");
            throw new RuntimeException("OpenFoodFacts product lookup failed: " + message);
        }

        JsonNode product = response.path("product");
        JsonNode nutriments = product.path("nutriments");

        return new OpenFoodFactsNutritionResult(
                response.path("code").asText(barcode),
                product.path("product_name").asText("Unknown product"),
                product.path("brands").asText("Unknown brand"),
                getDoubleOrNull(nutriments, "energy-kcal_100g"),
                getDoubleOrNull(nutriments, "proteins_100g"),
                getDoubleOrNull(nutriments, "carbohydrates_100g"),
                getDoubleOrNull(nutriments, "fat_100g"),
                getDoubleOrNull(nutriments, "fiber_100g"),
                getDoubleOrNull(nutriments, "sugars_100g"),
                getDoubleOrNull(nutriments, "salt_100g"),
                product.path("nutrition_grades").asText("unknown"),
                product.path("image_front_url").asText(null),
                "OpenFoodFacts"
        );
    }

    private Double getDoubleOrNull(JsonNode node, String field) {
        JsonNode value = node.get(field);
        if (value == null || value.isNull() || !value.isNumber()) {
            return null;
        }
        return value.asDouble();
    }
}