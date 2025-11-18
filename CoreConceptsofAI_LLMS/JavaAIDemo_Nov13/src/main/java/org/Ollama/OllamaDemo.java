package org.Ollama;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class OllamaDemo {

    public static void main(String[] args) throws IOException, InterruptedException {
        //String APIKey = System.getenv("OPENAI_API_KEY");
        // for Ollama, if it is running on the local, we got to change only the URI

        String uri = "http://localhost:11434/api/chat";
        HttpClient client = HttpClient.newHttpClient();

        String requestBody = """
                {
                        "model": "deepseek-r1:14b",
                        "messages": [
                            {"role": "system", "content": "You are a movie review expert"},
                            {"role": "user", "content": "name one hollywood comedy movie, just the name"}
                        ],
                        "stream": false
                }
                """;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(uri))
                .header("Content-Type", "application/json")
                //.header("Authorization", "Bearer " + APIKey)
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());

    }

}
