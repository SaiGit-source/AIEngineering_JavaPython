package com.mcp.MCPServer.tools;


import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class NewsTool {

    // to hit a client, either we need HttpClient or RestTemplate
    private RestTemplate restTemplate = new RestTemplate();
    @Tool(description = "Get current news headlines for specific topic")
    public String getNewsHeadlines(String topic){

        String apiKey = "****************";
        String url = "https://newsapi.org/v2/everything?q="+topic+ "&apiKey=" +apiKey;
        String result = restTemplate.getForObject(url, String.class);
        return "News headlines for "+topic + ": " + result;
    }

}
