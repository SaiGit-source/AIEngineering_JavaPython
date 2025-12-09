package com.vectordb.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

// Lets say if you want to talk to AI models, AI models give answer based on training. But every model has a limit until what point they are trained
// Say that model has data only until Nov 30th, 2025. Lets say we dont have any data in the model since Nov 30th
// Also if you ask the model about current Game scores or current weather, it has no idea
// in that case, you can add your own data - use case1
// say when you are building Conversational AI where you are talking to AI model and AI model should answer related to only your company
// Say if you ask Conversational AI, I am going to some place, suggest me list of things to bring: it might suggest warmers, shoes etc. It will provide suggestions only related to the products they sell not products in the entire world
// this can be achieved when you send your data to the AI model and that can be done with the help of RAG
// first before RAG, we got to store the 'product_details' data into Vector database. how do we do it?

// we need a dependency for vector database or vector store
// Step 1:
/*
<!-- https://mvnrepository.com/artifact/org.springframework.ai/spring-ai-advisors-vector-store -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-advisors-vector-store</artifactId>
    <version>1.0.0-M8</version>
</dependency>
 */

// Step 2: Where are we going to use it?
// even if we search for Tea or Coffee it should suggest this product: "Electric Coffee Grinder"

@SpringBootApplication
public class RagApplication {

	public static void main(String[] args) {
		SpringApplication.run(RagApplication.class, args);
	}

}
