package com.vectordb.demo.RAG.mariaDB;

import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.vectorstore.SimpleVectorStore;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.vectorstore.mariadb.MariaDBVectorStore;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;
// return the object of Maria Vector store

@Configuration
public class AppConfig {

    // bean that will return the VectorStore object
    // SimpleVectorStore is an in-memory data store, it needs an Embedding model to convert words into Vectors. Vector store will only store embeddings not convert
    /*
    @Bean
    public VectorStore getVectorStore(EmbeddingModel embeddingModel){
        return SimpleVectorStore.builder(embeddingModel).build();
    }
    */
    @Bean
    public VectorStore getVectorStore(JdbcTemplate jdbcTemplate, EmbeddingModel embeddingModel){
        // return SimpleVectorStore.builder(embeddingModel).build();
        return MariaDBVectorStore.builder(jdbcTemplate, embeddingModel)
                .vectorTableName("vector_name")
                .dimensions(1536)
                .distanceType(MariaDBVectorStore.MariaDBDistanceType.COSINE)
                .initializeSchema(true)
                .build();
    }
}
