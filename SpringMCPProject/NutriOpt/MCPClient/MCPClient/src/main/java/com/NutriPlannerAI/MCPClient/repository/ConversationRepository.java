package com.NutriPlannerAI.MCPClient.repository;

import com.NutriPlannerAI.MCPClient.model.ConversationEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ConversationRepository extends JpaRepository<ConversationEntity, String> {
}