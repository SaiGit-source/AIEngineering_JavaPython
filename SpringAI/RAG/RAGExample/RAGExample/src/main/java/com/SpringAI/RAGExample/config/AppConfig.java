package com.SpringAI.RAGExample.config;

import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.vectorstore.mariadb.MariaDBVectorStore;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;

@Configuration
public class AppConfig {

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
