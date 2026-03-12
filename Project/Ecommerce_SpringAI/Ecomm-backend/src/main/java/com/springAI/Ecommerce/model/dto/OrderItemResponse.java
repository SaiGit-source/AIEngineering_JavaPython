package com.springAI.Ecommerce.model.dto;

import java.math.BigDecimal;

public record OrderItemResponse(String productName, int quantity, BigDecimal totalPrice) {


}
