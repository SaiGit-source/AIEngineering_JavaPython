package org.gemini;

// Gemini: https://aistudio.google.com/
// https://aistudio.google.com/api-keys
// Get the API key and put it in Edit Configurations

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class GeminiTest {

    public static void main(String[] args) throws IOException, InterruptedException {

        String APIKey = System.getenv("GEMINI_API_KEY"); // click on Current File --> Edit Configurations
        // if you are using SDK then you dont have to use URI. it is needed for HttpClient

        // Gemini URI link: https://ai.google.dev/gemini-api/docs/openai

        String uri = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions";
        HttpClient client = HttpClient.newHttpClient();

        String requestBody = """
                {
                        "model": "gemini-2.5-flash",
                        "messages": [
                            {"role": "system", "content": "You are a movie review expert"},
                            {"role": "user", "content": "name one movie for Software engineers, just the name"}
                        ]
                }
                """;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(uri))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + APIKey)
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());

    }
}

// Output
// {"choices":[{"finish_reason":"stop","index":0,"message":{"content":"Ghostbusters","role":"assistant"}}],"created":1763164273,"id":"ccAXad3iNNbiz7IPocTe0Ac","model":"gemini-2.5-flash","object":"chat.completion","usage":{"completion_tokens":2,"prompt_tokens":17,"total_tokens":49}}
// {"choices":[{"finish_reason":"stop","index":0,"message":{"content":"The Social Network","role":"assistant"}}],"created":1763164315,"id":"m8AXaafJCKDpz7IPs5_OmQE","model":"gemini-2.5-flash","object":"chat.completion","usage":{"completion_tokens":3,"prompt_tokens":18,"total_tokens":671}}
// {"choices":[{"finish_reason":"stop","index":0,"message":{"content":"Inception","role":"assistant"}}],"created":1763164553,"id":"icEXaavRJf-Cz7IPm8Hf4Ak","model":"gemini-2.5-flash","object":"chat.completion","usage":{"completion_tokens":2,"prompt_tokens":18,"total_tokens":1258}}