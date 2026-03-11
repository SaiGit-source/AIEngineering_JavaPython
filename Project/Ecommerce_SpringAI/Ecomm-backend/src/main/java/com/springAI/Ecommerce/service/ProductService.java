package com.springAI.Ecommerce.service;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import javax.swing.text.Document;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.springAI.Ecommerce.model.Product;
import com.springAI.Ecommerce.repo.ProductRepo;

@Service
public class ProductService {
	
	@Autowired
	private ProductRepo repo;
	
	public List<Product> getAllProducts(){
		return repo.findAll();
	}
	
	public Product getProductByID(int id) {
		return repo.findById(id).orElse(new Product(-1));
	}
	
	public Product addOrUpdateProduct(Product product, MultipartFile image) throws IOException{
		
        if (image != null && !image.isEmpty()) {
            product.setImageName(image.getOriginalFilename());
            product.setImageType(image.getContentType());
            product.setProductImage(image.getBytes());

        }

        Product savedProduct = repo.save(product);
        
        return savedProduct;
	}
	
    public void deleteProduct(int id) {
        repo.deleteById(id);
    }
	
	
	}


