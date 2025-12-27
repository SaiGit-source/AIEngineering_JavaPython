package com.mcp.MCPClient.controller;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class MCPClient {
    private ChatClient chatClient;

    // we need to inform ChatClient that we are calling MCP Server, so add ToolCallBaclProvider

    public MCPClient(ChatClient.Builder chatClientBuilder, ToolCallbackProvider toolCallBackProvider){
        this.chatClient = chatClientBuilder
                .defaultToolCallbacks(toolCallBackProvider)
                .build();
    }
    @GetMapping("/chat")
    public String getAnswer(@RequestParam String question)
    {
        return chatClient.prompt(question).call().content();
    }
}

// GET http://localhost:8080/api/chat?question=What can you do for me?
/*
I can assist you with a variety of tasks, including:

1. **Current Date and Time**:
   - Provide the current date and time for your timezone or any specified timezone.

2. **News Headlines**:
   - Get the latest news headlines on specific topics of interest.

If you have any specific requests or questions, feel free to let me know!
 */