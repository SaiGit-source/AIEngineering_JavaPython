package org.example;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.embeddings.CreateEmbeddingResponse;
import com.openai.models.embeddings.Embedding;
import com.openai.models.embeddings.EmbeddingCreateParams;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.List;

public class OpenAIEmbeddings {

    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.fromEnv();

        List<String> wordsImmutable = List.of("Cat", "Dog", "Fish", "Laptop", "Java", "Apple");

        for (String word:wordsImmutable){
            EmbeddingCreateParams params = new EmbeddingCreateParams.Builder()
                    .model("text-embedding-3-large")
                    .input(word)
                    .dimensions(2)
                    .build();

            CreateEmbeddingResponse createEmbeddingResponse = client.embeddings().create(params);
            System.out.println(createEmbeddingResponse.data().get(0).embedding());
            Embedding embedding = createEmbeddingResponse.data().getFirst();
            System.out.printf("%s = (%.6f, %.6f)%n",
                    word,
                    embedding.embedding().get(0),
                    embedding.embedding().get(1)
            );
        }

    }

}
/* Output
[-0.9921954, -0.124692425]
Cat = (-0.992195, -0.124692)
[-0.9711004, 0.23867139]
Dog = (-0.971100, 0.238671)
[-0.9470845, 0.32098433]
Fish = (-0.947084, 0.320984)
[-0.58899564, 0.8081362]
Laptop = (-0.588996, 0.808136)
[-0.29357088, -0.9559373]
Java = (-0.293571, -0.955937)
[-0.83752567, 0.546398]
Apple = (-0.837526, 0.546398)
 */

// going forward we are going to learn RAG, similarity search

