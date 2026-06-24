package com.banking.rca_backend.service;

import com.banking.rca_backend.dto.RcaAnalysisResponse;
import com.banking.rca_backend.dto.RcaResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RcaService {

    private final PineconeSearchService pineconeSearchService;
    private final ChatClient chatClient;
    private final ObjectMapper objectMapper;

    public RcaService(PineconeSearchService pineconeSearchService,
                      ChatClient.Builder chatClientBuilder,
                      ObjectMapper objectMapper) {
        this.pineconeSearchService = pineconeSearchService;
        this.chatClient = chatClientBuilder.build();
        this.objectMapper = objectMapper;
    }

    public RcaResponse searchEvidence(String question) {
        List<String> evidence = pineconeSearchService.searchEvidence(question);

        return new RcaResponse(
                question,
                "Retrieved " + evidence.size() + " evidence records from Pinecone",
                evidence
        );
    }

    public RcaAnalysisResponse analyzeRca(String question) {
        List<String> retrievedEvidence = pineconeSearchService.searchEvidence(question);

        if (retrievedEvidence.isEmpty()) {
            return new RcaAnalysisResponse(
                    question,
                    "No relevant evidence found",
                    "Unknown",
                    "Unknown",
                    List.of(),
                    List.of("Check whether logs were ingested into Pinecone."),
                    retrievedEvidence
            );
        }

        String evidenceContext = String.join("\n\n---\n\n", retrievedEvidence);

        String aiResponse = chatClient.prompt()
                .system("""
                        You are a production support RCA assistant for banking microservices.

                        Use only the provided evidence logs.
                        Do not guess beyond the evidence.

                        Return ONLY valid JSON.
                        Do not return markdown.
                        Do not wrap the answer in ```json.

                        JSON format:
                        {
                          "question": "...",
                          "rootCause": "...",
                          "symptom": "...",
                          "impactedService": "...",
                          "evidence": ["...", "..."],
                          "suggestedFix": ["...", "..."]
                        }
                        """)
                .user("""
                        User question:
                        %s

                        Retrieved evidence logs:
                        %s
                        """.formatted(question, evidenceContext))
                .call()
                .content();

        try {
            String cleanJson = cleanJson(aiResponse);
            RcaAnalysisResponse parsed = objectMapper.readValue(cleanJson, RcaAnalysisResponse.class);

            return new RcaAnalysisResponse(
                    question,
                    parsed.rootCause(),
                    parsed.symptom(),
                    parsed.impactedService(),
                    parsed.evidence(),
                    parsed.suggestedFix(),
                    retrievedEvidence
            );

        } catch (Exception e) {
            return new RcaAnalysisResponse(
                    question,
                    "AI response could not be parsed",
                    aiResponse,
                    "Unknown",
                    List.of("Raw AI response returned in symptom field"),
                    List.of("Check the JSON prompt or model output format."),
                    retrievedEvidence
            );
        }
    }

    private String cleanJson(String response) {
        return response
                .replace("```json", "")
                .replace("```", "")
                .trim();
    }
}