package com.SpringAI.mcp_demo.controller;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class MCPController {
    private ChatClient chatClient;

    // we need to inform ChatClient that we are calling MCP Server, so add ToolCallBaclProvider
    public MCPController(ChatClient.Builder chatClientBuilder, ToolCallbackProvider toolCallBackProvider){
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

// GET http://localhost:8080/api/chat?question=What's Java?
// Output
/*
Java is a high-level, object-oriented programming language that was originally developed by Sun Microsystems, which is now part of Oracle Corporation. It was first released in 1995 and has since become one of the most widely used programming languages in the world.
 */

// GET http://localhost:8080/api/chat?question=Create a file test.txt with content "MCP-servers test is successful" in the 'mcp_server' folder
/*
The file `test.txt` has been successfully created in the `mcp_server` folder with the content "MCP-servers test is successful."
 */

// GET http://localhost:8080/api/chat?question=List the files in the mcp_servers folder and its content

/*
The files in the `mcp_servers` folder are as follows:

- **test.txt**
  - Content: "MCP-servers test is successful"
 */
