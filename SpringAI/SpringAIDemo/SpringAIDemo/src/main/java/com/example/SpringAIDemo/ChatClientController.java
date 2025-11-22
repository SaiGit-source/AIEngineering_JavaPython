package com.example.SpringAIDemo;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatResponse;
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

// to get Metadata and other extra contents
    @GetMapping("/api/chatclient/input/v1/{message}")
    public String chatClientInput_1(@PathVariable String message){
        // i want AI to respond here
        ChatResponse response = chatClient
                .prompt(message)
                .call()
                .chatResponse(); // we want extra content,
        // it talks to OpenAI
        String result = response.getResult().getOutput().getText();
        System.out.println(response.getMetadata().getModel());
        System.out.println(response.getMetadata().getUsage().getTotalTokens()); // how many tokens were used for this one query?
        return result;

        // http://localhost:8080/api/chatclient/input/v1/recommend a movie with good background name, only movie name
        // Output
        /*
        ChatResponse [metadata={ id: chatcmpl-CeZ8fCFaJScWyzW5RTF2PChwLIdID, usage: DefaultUsage{promptTokens=18, completionTokens=5, totalTokens=23}, rateLimit: { @type: org.springframework.ai.openai.metadata.OpenAiRateLimit, requestsLimit: 10000, requestsRemaining: 9999, requestsReset: PT1M4S, tokensLimit: 200000; tokensRemaining: 199983; tokensReset: PT0.005S } }, generations=[Generation[assistantMessage=AssistantMessage [messageType=ASSISTANT, toolCalls=[], textContent="Amélie", metadata={role=ASSISTANT, messageType=ASSISTANT, refusal=, finishReason=STOP, annotations=[], index=0, id=chatcmpl-CeZ8fCFaJScWyzW5RTF2PChwLIdID}], chatGenerationMetadata=DefaultChatGenerationMetadata[finishReason='STOP', filters=0, metadata=0]]]]
         */
        /* printed in console
            gpt-4o-mini-2024-07-18 --> model
            23 --> number of tokens used
         */

        // http://localhost:8080/api/chatclient/input/v1/recommend a movie with good background name, only movie name
        // Output
        // "Inception"

        /* printed on console
        gpt-4o-2024-08-06
        21
         */



    }


}
