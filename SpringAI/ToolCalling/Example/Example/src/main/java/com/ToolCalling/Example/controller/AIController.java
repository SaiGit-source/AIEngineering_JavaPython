package com.ToolCalling.Example.controller;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.memory.MessageWindowChatMemory;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AIController {

    private ChatClient chatClient;
    private ChatMemory memory = MessageWindowChatMemory.builder().build();
    @Autowired
    private DateTimeTool dateTimeTool;

    @Autowired
    private NewsTool newsTool;

    @Autowired
    private BooksTool booksTool;

    public AIController(ChatClient.Builder builder) {
        this.chatClient = builder
                .defaultAdvisors(MessageChatMemoryAdvisor.builder(memory).build())
                .build();
    }

    @GetMapping("/api/{message}")
    public String home(@PathVariable String message) {
        ChatResponse response = chatClient
                .prompt(message)
                .tools(dateTimeTool, newsTool)
                .call()
                .chatResponse();  //.content();

        String result = response.getResult().getOutput().getText();

//        System.out.println(response.getMetadata());
//        System.out.println(response.getMetadata().getUsage().getTotalTokens());

        System.out.println(response);

        return result;
    }


    @GetMapping("/api/books/{bookname}")
    public String books(@PathVariable String bookname) {
        ChatResponse response = chatClient
                .prompt(bookname)
                .tools(booksTool)
                .call()
                .chatResponse();  //.content();

        String result = response.getResult().getOutput().getText();

//        System.out.println(response.getMetadata());
//        System.out.println(response.getMetadata().getUsage().getTotalTokens());

        System.out.println(response);

        return result;
    }


}

// Output first part only DateTimeTool
// GET http://localhost:8080/api/current date?
// The current date is December 18, 2025.


// GET http://localhost:8080/api/current date in NewYork?
// The current date and time in New York is December 18, 2025, 11:30 AM (EST).

// GET http://localhost:8080/api/current news in NewYork?
// I can't provide real-time news updates. You may want to check a reliable news website or app for the latest news in New York.

// GET http://localhost:8080/api/recent news in NewYork?
/*
Here are some recent news headlines from New York:

1. **Why college students prefer News Daddy over The New York Times** - College students are increasingly turning to platforms like TikTok for news, preferring influencers like Dylan Page for major story updates. [Read more](https://www.theverge.com/cs/features/818380/college-students-news-sources-tiktok-instagram-newsdaddy)

2. **New York’s new law forces advertisers to say when they’re using AI avatars** - Governor Kathy Hochul of New York signed a pioneering bill requiring advertisers to disclose the use of AI-generated people in ads. [Read more](https://www.theverge.com/news/842848/new-york-law-ai-advertisements-sag-aftra-labor)

3. **Your Data Might Determine How Much You Pay for Eggs** - A new law in New York requires retailers to disclose if consumer data affects pricing on basic goods, though it doesn't mandate transparency on how. [Read more](https://www.wired.com/story/algorithmic-pricing-eggs-ny-law/)

4. **AI’s water and electricity use soars in 2025** - AI technologies have significantly increased water and electricity consumption, with environmental impacts compared to New York City's carbon pollution levels. [Read more](https://www.theverge.com/news/845831/ai-chips-data-center-power-water)

5. **The Donald Trump v Zohran Mamdani show** - A surprising political dynamic unfolds as US President Donald Trump meets with New York's incoming mayor Zohran Mamdani. [Read more](https://www.bbc.co.uk/sounds/play/w3ct8bys)

These articles cover a variety of topics, including education, technology, environmental concerns, and political interactions.
 */

/*
GET http://localhost:8080/api/books/zerotoone

The book "Zero to One" is available for purchase. You can find it on Amazon and other major book retailers. If you're interested in exploring further, you can visit the [Amazon page for Zero to One](https://www.amazon.com).
 */