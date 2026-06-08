package com.nutriopt.MCPServer.repo;

import com.nutriopt.MCPServer.model.FoodItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface FoodItemRepo extends JpaRepository<FoodItem, Long> {

    Optional<FoodItem> findByBarcode(String barcode);

    List<FoodItem> findByNameContainingIgnoreCase(String name);

    List<FoodItem> findByGenericNameContainingIgnoreCase(String genericName);
}