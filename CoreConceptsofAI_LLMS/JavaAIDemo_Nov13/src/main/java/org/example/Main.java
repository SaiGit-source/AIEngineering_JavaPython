package org.example;


import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Main {
    public static void main(String[] args) throws IOException, InterruptedException {
        String APIKey = System.getenv("OPENAI_API_KEY"); // click on Current File --> Edit Configurations
        // if you are using SDK then you dont have to use URI. it is needed for HttpClient
        // URI https://platform.openai.com/docs/api-reference/authentication

        String uri = "https://api.openai.com/v1/chat/completions";
        HttpClient client = HttpClient.newHttpClient();

        String requestBody = """
                {
                        "model": "gpt-4o",
                        "messages": [
                            {"role": "system", "content": "You are a movie review expert"},
                            {"role": "user", "content": "name one hollywood comedy movie, just the name"}
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

/* Output

{
  "id": "chatcmpl-CbertSHLY0Cdh7MSyFy2wm9pKUWq1",
  "object": "chat.completion",
  "created": 1763091269,
  "model": "gpt-4o-2024-08-06",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "\"Superbad\"",
        "refusal": null,
        "annotations": []
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 26,
    "completion_tokens": 4,
    "total_tokens": 30,
    "prompt_tokens_details": {
      "cached_tokens": 0,
      "audio_tokens": 0
    },
    "completion_tokens_details": {
      "reasoning_tokens": 0,
      "audio_tokens": 0,
      "accepted_prediction_tokens": 0,
      "rejected_prediction_tokens": 0
    }
  },
  "service_tier": "default",
  "system_fingerprint": "fp_b1442291a8"
}
51:30 --> Next try with Gemini
 */