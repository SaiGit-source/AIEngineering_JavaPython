package controller;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.memory.MessageWindowChatMemory;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class AIController {

    @Autowired
    private VectorStore vectorStore;

    private ChatClient chatClient;
    @Autowired
    private DateTimeTool dateTimeTool;

    @GetMapping("/api/{message}")
    public String home(@PathVariable String message) {
        ChatResponse response = chatClient
                .prompt(message)
                .tools(dateTimeTool)
                .call()
                .chatResponse();  //.content();

        String result = response.getResult().getOutput().getText();

//        System.out.println(response.getMetadata());
//        System.out.println(response.getMetadata().getUsage().getTotalTokens());

        System.out.println(response);

        return result;
    }


}
