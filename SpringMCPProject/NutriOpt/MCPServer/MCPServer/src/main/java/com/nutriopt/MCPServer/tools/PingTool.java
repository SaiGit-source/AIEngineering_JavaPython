package com.nutriopt.MCPServer.tools;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;

@Component
public class PingTool {

    @Tool(description = "Simple ping test tool")
    public String ping() {
        return "pong";
    }
}