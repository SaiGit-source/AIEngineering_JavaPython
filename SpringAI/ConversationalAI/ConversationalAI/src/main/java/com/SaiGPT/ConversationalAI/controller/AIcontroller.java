package com.SaiGPT.ConversationalAI.controller;

import org.apache.logging.log4j.message.Message;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.memory.MessageWindowChatMemory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AIcontroller {

    private ChatClient chatClient;
    // In-memory, and database
    private ChatMemory memory = MessageWindowChatMemory.builder().build(); // this is in-memory, but the problem is, once you restart the application in-memory is gone. thats why database is better

    // we dont want dependency on chatModel, so we use Chat Client builder
    // however if you have more than one dependency, this chat builder will fail

    // we have to link chatMemory with the chatClient
    // for that, we have something called as advisors
    // in Spring, we have something called as AOP (Aspect Oriented Programming)
    // Spring Advisors have AOP behind the scene
    public AIcontroller(ChatClient.Builder builder){
        // this.chatClient = builder.build();
        this.chatClient = builder
                .defaultAdvisors(MessageChatMemoryAdvisor.builder(memory).build())
                .build();
    }
    @GetMapping("/api/{message}")
    public String home(@PathVariable String message){
        // i want AI to respond here
        String msg = chatClient.prompt(message).call().content(); // prompt then call OpenAPI model then fetch the results (content())
        // it talks to OpenAI
        return msg;
    }

}
