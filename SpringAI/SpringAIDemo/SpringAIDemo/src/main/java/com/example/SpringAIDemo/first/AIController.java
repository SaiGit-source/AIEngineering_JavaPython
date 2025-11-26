package com.example.SpringAIDemo.first;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.openai.OpenAiChatModel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AIController {
    // get object of ChatModel
    @Autowired
    private OpenAiChatModel chatModel;

    // we are creating a constructor to inject ChatModel here
    /*
    public AIController(OpenAiChatModel chatModel){
        this.chatModel = chatModel;
    }
    */

    @GetMapping("/api/greet/v1")
    public String home(){
        // i want AI to respond here
        String msg = chatModel.call("I need a message to greet user"); // it talks to OpenAI
       return msg;
    }

    // for chatClient, check ChatClientController
private ChatClient chatClient;


    @GetMapping("/api/chatclient/greet/v1")
    public String chatClient(){
        // i want AI to respond here
        String msg = chatModel.call("I need a message to greet user"); // it talks to OpenAI
        return msg;
    }
}
