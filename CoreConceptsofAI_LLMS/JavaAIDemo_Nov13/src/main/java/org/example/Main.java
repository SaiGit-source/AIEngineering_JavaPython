package org.example;


import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Main {
    public static void main(String[] args) {
        String APIKey = System.getenv("OPEN_API_KEY");
        // if you are using SDK then you dont have to use URI. it is needed for HttpClient
        // URI https://platform.openai.com/docs/api-reference/authentication

        String uri = "https://api.openai.com/v1/chat/completions";
        HttpClient client = HttpClient.newHttpClient();

        String requestBody = """
                {
                        "model": "gpt-4o",
                        "messages": [
                            {"role": "system", "content"
                        ]

                }
                """;
        
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(uri))
                .header("Content-Type", "appication/json")
                .header("Authorization", "Bearer " + APIKey)
                .POST(HttpRequest.BodyPublishers.ofString())
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());
    }
}