package com.ToolCalling.Example.controller;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class BooksTool {

    // to hit a client, either we need HttpClient or RestTemplate
    private RestTemplate restTemplate = new RestTemplate();
    @Tool(description = "Get book availability and purchase location or link")
    public String getBookAvailabilityandPurchaseLink(String bookname){

        String apiKey = "**************";
        String url = "https://newsapi.org/v2/everything?q="+bookname+ "&apiKey=" +apiKey;
        String result = restTemplate.getForObject(url, String.class);
        return "Book is "+bookname + ": " + result;
    }

}
