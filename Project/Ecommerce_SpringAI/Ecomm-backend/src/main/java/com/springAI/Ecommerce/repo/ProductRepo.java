package com.springAI.Ecommerce.repo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.springAI.Ecommerce.model.Product;

@Repository
public interface ProductRepo extends JpaRepository<Product, Integer>{
	
}
