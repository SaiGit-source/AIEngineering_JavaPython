package com.SpringAI.RAGExample.controller;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.api.Advisor;
import org.springframework.ai.chat.client.advisor.vectorstore.QuestionAnswerAdvisor;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class rag_controller {
    @Autowired
    private VectorStore vectorStore;
    private ChatClient chatClient;

    public rag_controller(ChatClient.Builder builder){
        this.chatClient = builder.build();
    }


    // we send requests to get (list of) products related to the keyword
    @GetMapping("/api/products")
    public List<Document> getProducts(@RequestParam String text){
        // return vectorStore.similaritySearch(text); // similaritySearch(text) will give you List<Document> matching with this text but we have to return a String
        return vectorStore.similaritySearch(SearchRequest.builder()
                .query(text)
                .topK(2)
                .build()); // with SearchRequest, we can customize how many search values you want
    }

    // RAG: instead of returning a Document, we got to return response from LLM, which is different from the above API
@GetMapping("api/ask/{userQuery}")
    public String productInfo(@PathVariable String userQuery) {

    // R of RAG (Retrieval)
    List<Document> docs = vectorStore.similaritySearch(userQuery);

    // A of RAG (Augmentation)
    StringBuilder context = new StringBuilder();
    for (Document doc : docs) {
        context.append(doc.getFormattedContent()).append("\n"); // putting all documents into one
    }

    // G of RAG (Generation)
    String prompt = """
            You are a helpful product suggestion assistant.
            Use only the information in the product details below to answer the user.
            If the information is not available there, say you don't know.
            Product details:
            %s
            User question: %s
            Answer in a short, clear way with price and other relevant details:
            """.formatted(context, userQuery);
    // we are providing Product details as context

    // we dont want additional rubbish data, lets say we want only price, category etc
    // thats where we need PromptTemplate
    String template = """
            {query}
            Context Information below.
            
            ---------------------------
            {question_answer_context}
            -----------------------------
            
            Given the context information and no prior knowledge, answer the query with name, price and category and description.
            
            Follow these rules:
            1. If the answer is not in the context, just say that you don't know
            2. Avoid statements like "Based on the context..." or "The provided information..."
            
            """;
    // Important: we see two placeholders: {userQuery} and {question_answer_context}, we are not replacing them dynamically here
    // they will be replaced by QuestionAnswerAdvisor internally

    PromptTemplate promptTemplate = PromptTemplate.builder()
            .template(template)
            .build();
    // return chatClient.prompt(prompt).call().content(); // no chat history memory

    return chatClient
            .prompt(userQuery)
            .advisors(QuestionAnswerAdvisor.builder(vectorStore)
                    .promptTemplate(promptTemplate).build())
            .call()
            .content();
    // if you want your application to remember chat history, you can use a memory advisor
    }
}


// you are talking to LLM but you are getting response based on your Product list
// for RAG
// http://localhost:8080/api/ask/suggest products for vacation
/*
For vacation, consider the "Waterproof Travel Backpack" for its multi-compartment design, padded laptop sleeve, and water-resistant fabric.
 */

// now added 'price' to prompt
// http://localhost:8080/api/ask/suggest products for cooking

/*
I suggest the "Silicone Baking Mats (Set of 2)" for cooking. They are non-stick mats made with reusable, heat-resistant silicone, priced at $13.00. Additionally, the "Digital Kitchen Scale" provides precise measurement for cooking and baking, includes a tare function, LCD screen, and auto-off feature, priced at $14.75.
 */

// with chat memory advisors
// GET http://localhost:8080/api/ask/suggest products for cooking

/*
Based on the context provided, here are some products that would be useful for cooking:

1. **Silicone Baking Mats (Set of 2)**
   - Description: Non-stick mats for baking with reusable, heat-resistant silicone.
   - Price: $13.00
   - Features: Reusable and heat-resistant, making them perfect for baking tasks.

2. **Kitchen Scale**
   - Description: Precise measurement for cooking and baking, with tare function.
   - Price: $14.75
   - Features: LCD screen, Slim design, Units in oz/g/ml/lb, Auto-off

These products can help with various cooking and baking tasks, providing precision and convenience in the kitchen.

 */

// After implementing PromptTemplate
// GET http://localhost:8080/api/ask/suggest products for cooking
/*
Title: "Silicone Baking Mats (Set of 2)"
Price: $13
Category: Cooking/Baking
Description: Non-stick mats for baking with reusable, heat-resistant silicone.
 */