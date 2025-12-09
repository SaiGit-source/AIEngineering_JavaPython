package com.vectordb.demo.RAG;

import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.vectorstore.SimpleVectorStore;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AppConfig {

    // bean that will return the VectorStore object
    // SimpleVectorStore is an in-memory data store, it needs an Embedding model to convert words into Vectors. Vector store will only store embeddings not convert
    @Bean
    public VectorStore getVectorStore(EmbeddingModel embeddingModel){
        return SimpleVectorStore.builder(embeddingModel).build();
    }
}
