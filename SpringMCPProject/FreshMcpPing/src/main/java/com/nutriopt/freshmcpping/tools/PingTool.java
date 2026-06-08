package com.nutriopt.freshmcpping.tools;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Service;

@Service
public class PingTool {

    @Tool(description = "Simple ping test tool")
    public String ping() {
        return "pong";
    }
}