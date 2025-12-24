package com.SpringAI.mcp_demo.controller;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class MCPController {
    private ChatClient chatClient;
    public MCPController(ChatClient.Builder chatClientBuilder){
        this.chatClient = chatClientBuilder.build();
    }
    @GetMapping("/chat")
    public String getAnswer(@RequestParam String question)
    {
        return chatClient.prompt(question).call().content();
    }
}

// GET http://localhost:8080/api/chat?question=What's Java?
// Output
/*
Java is a high-level, object-oriented programming language that was originally developed by Sun Microsystems, which is now part of Oracle Corporation. It was first released in 1995 and has since become one of the most widely used programming languages in the world.
 */