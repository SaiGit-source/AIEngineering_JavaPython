package com.NutriPlannerAI.MCPClient.repository;

import com.NutriPlannerAI.MCPClient.model.MessageEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MessageRepository extends JpaRepository<MessageEntity, Long> {

    List<MessageEntity> findByConversationIdOrderByCreatedAtAsc(String conversationId);
}