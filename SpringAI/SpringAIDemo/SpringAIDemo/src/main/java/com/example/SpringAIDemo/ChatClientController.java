package com.example.SpringAIDemo;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ChatClientController {

    private ChatClient chatClient;

    // we dont want dependency on chatModel, so we use Chat Client builder
    // however if you have more than one dependency, this chat builder will fail

    public ChatClientController(ChatClient.Builder builder){
        this.chatClient = builder.build();
    }

    @GetMapping("/api/chatclient/greet")
    public String chatClient(){
        // i want AI to respond here
        String msg = chatClient.prompt("I need a message to greet user").call().content(); // prompt then call OpenAPI model then fetch the results (content())
        // it talks to OpenAI
        return msg;
    }

    // next we are passing the input string

    @GetMapping("/api/chatclient/input/{message}")
    public String chatClientInput(@PathVariable String message){
        // i want AI to respond here
        String msg = chatClient.prompt(message).call().content(); // prompt then call OpenAPI model then fetch the results (content())
        // it talks to OpenAI
        return msg;
    }


}
