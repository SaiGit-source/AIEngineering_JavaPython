package com.NutriPlannerAI.MCPClient.service;

import com.NutriPlannerAI.MCPClient.model.ConversationEntity;
import com.NutriPlannerAI.MCPClient.model.MessageEntity;
import com.NutriPlannerAI.MCPClient.repository.ConversationRepository;
import com.NutriPlannerAI.MCPClient.repository.MessageRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class ConversationHistoryService {

    private final ConversationRepository conversationRepository;
    private final MessageRepository messageRepository;

    public ConversationHistoryService(
            ConversationRepository conversationRepository,
            MessageRepository messageRepository
    ) {
        this.conversationRepository = conversationRepository;
        this.messageRepository = messageRepository;
    }

    public void saveMessage(String conversationId, String role, String content) {
        ConversationEntity conversation = conversationRepository
                .findById(conversationId)
                .orElseGet(() -> new ConversationEntity(conversationId));

        conversation.setUpdatedAt(LocalDateTime.now());
        conversationRepository.save(conversation);

        MessageEntity message = new MessageEntity(
                conversationId,
                role,
                content
        );

        messageRepository.save(message);
    }

    public List<String> getHistoryAsText(String conversationId) {
        return messageRepository
                .findByConversationIdOrderByCreatedAtAsc(conversationId)
                .stream()
                .map(message -> message.getRole() + ": " + message.getContent())
                .toList();
    }

    public String getHistoryBlock(String conversationId) {
        List<String> history = getHistoryAsText(conversationId);

        if (history.isEmpty()) {
            return "No previous conversation.";
        }

        return String.join("\n", history);
    }

    public void saveSummary(String conversationId, String summary) {
        ConversationEntity conversation = conversationRepository
                .findById(conversationId)
                .orElseGet(() -> new ConversationEntity(conversationId));

        conversation.setSummary(summary);
        conversation.setUpdatedAt(LocalDateTime.now());

        conversationRepository.save(conversation);
    }

    public String getSummary(String conversationId) {
        return conversationRepository
                .findById(conversationId)
                .map(ConversationEntity::getSummary)
                .orElse("");
    }
}