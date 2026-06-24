package com.banking.rca_backend.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;
import org.springframework.web.util.UriUtils;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class PineconeSearchService {

private final RestClient restClient;
private final ObjectMapper objectMapper;
private final String indexHost;
private final String namespace;
private final int topK;

public PineconeSearchService(
        @Value("${pinecone.api-key}") String apiKey,
        @Value("${pinecone.index-host}") String indexHost,
        @Value("${pinecone.namespace}") String namespace,
        @Value("${pinecone.api-version}") String apiVersion,
        @Value("${pinecone.top-k:2}") int topK,
        ObjectMapper objectMapper
) {
    this.indexHost = indexHost;
    this.namespace = namespace;
    this.topK = topK;
    this.objectMapper = objectMapper;

    this.restClient = RestClient.builder()
            .defaultHeader("Api-Key", apiKey)
            .defaultHeader("X-Pinecone-Api-Version", apiVersion)
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .defaultHeader(HttpHeaders.ACCEPT, MediaType.APPLICATION_JSON_VALUE)
            .build();
}

public List<String> searchEvidence(String question) {
    try {
        String cleanHost = indexHost
                .replace("https://", "")
                .replace("http://", "")
                .replaceAll("/+$", "");

        String encodedNamespace = UriUtils.encodePathSegment(
                namespace,
                StandardCharsets.UTF_8
        );

        String url = "https://" + cleanHost
                + "/records/namespaces/"
                + encodedNamespace
                + "/search";

        System.out.println("Pinecone URL = " + url);
        System.out.println("Pinecone topK = " + topK);

        Map<String, Object> requestBody = Map.of(
                "query", Map.of(
                        "inputs", Map.of("text", question),
                        "top_k", topK
                ),
                "fields", List.of(
                        "text",
                        "traceId",
                        "transactionId",
                        "services",
                        "errorCodes",
                        "environment"
                )
        );

        String responseBody = restClient.post()
                .uri(url)
                .body(requestBody)
                .retrieve()
                .body(String.class);

        return parseEvidence(responseBody);

    } catch (Exception e) {
        throw new RuntimeException("Failed to search Pinecone evidence", e);
    }
}

private List<String> parseEvidence(String responseBody) throws Exception {
    List<String> evidenceList = new ArrayList<>();

    JsonNode root = objectMapper.readTree(responseBody);
    JsonNode hits = root.path("result").path("hits");

    if (!hits.isArray()) {
        return evidenceList;
    }

    for (JsonNode hit : hits) {
        JsonNode fields = hit.path("fields");

        String evidence = """
                ID: %s
                Score: %s
                Trace ID: %s
                Transaction ID: %s
                Services: %s
                Error Codes: %s
                Environment: %s

                Evidence:
                %s
                """.formatted(
                hit.path("_id").asText(""),
                hit.path("_score").asDouble(),
                fields.path("traceId").asText(""),
                fields.path("transactionId").asText(""),
                fields.path("services").asText(""),
                fields.path("errorCodes").asText(""),
                fields.path("environment").asText(""),
                fields.path("text").asText("")
        );

        evidenceList.add(evidence);
    }

    return evidenceList;
}

}
