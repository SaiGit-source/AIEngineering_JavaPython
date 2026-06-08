package com.nutriopt.MCPServer.tools;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

//@Component
public class OpenPricesTool {

    private final WebClient webClient;

    public OpenPricesTool() {
        this.webClient = WebClient.builder()
                .baseUrl("https://prices.openfoodfacts.org")
                .build();
    }

    @Tool(description = "Get product price records from Open Prices using a product barcode or product code.")
    public String getOpenPricesByProductCode(String productCode) {

        String result = webClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/api/v1/prices")
                        .queryParam("product_code", productCode)
                        .queryParam("page_size", 5)
                        .build())
                .retrieve()
                .bodyToMono(String.class)
                .block();

        return "Open Prices results for product code " + productCode + ": " + result;
    }
}