package com.example.SpringAIDemo.embeddings;

import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
// add in application.properties file
// spring.ai.openai.embedding.options.model=text-embedding-3-large
// if you use normal words, how AI is able to understand what you are talking about? how AI is able to relate the words? AI does it with the help of Embeddings. Say we have two words "Laptop" and a "Computer", they should have a high similarity score
// Understanding embeddings: https://docs.spring.io/spring-ai/reference/api/vectordbs/understand-vectordbs.html
// Similarities goes from 0 to 1, it the value is between 0.5 to 0.8 means they are very similar
// if it is less than 0.5 then not similar or unrelated
// later on we will use in-built functions to implement Cosine functions

@RestController
public class embeddingController {

    @Autowired
    private EmbeddingModel embeddingModel;

    @GetMapping("/api/embeddings/")
    public float[] getVector(String text){

        return embeddingModel.embed(text);
    }

    // Output
    /*
    GET http://localhost:8080/api/embeddings/?text=Dog
    [
    -8.876295E-4,
    -0.01515465,
    -0.018503105,
    -0.029760847,................
]
     */
// where is the use-case for Cosine similarity?
    // sometimes, we got to provide data or context to LLM, thats where RAG comes into picture. Retrieval-Augmented-Generative
    // thats where we will use cosine similarity, it will fetch the similar reference document based on Cosine similarity
    @GetMapping("/api/similarity/")
    public double cosineSimilarity(@RequestParam String text1, @RequestParam String text2){
        float[] embed1 = embeddingModel.embed(text1);
        float[] embed2 = embeddingModel.embed(text2);

        double dotProduct = 0.0;
        double normA = 0.0;
        double normB = 0.0;
        for (int i=0; i<embed1.length; i++){
            dotProduct += embed1[i] * embed2[i];
            normA += Math.pow(embed1[i], 2);
            normB += Math.pow(embed2[i], 2);
        }

        return (dotProduct / (Math.sqrt(normA) * Math.sqrt(normB)))*100;
    }
    // Output
    /*
    GET http://localhost:8080/api/similarity/?text1=dog&text2=cat
    0.5907004576848616


     */

}
