package com.nutriopt.freshmcpping.config;

import com.nutriopt.freshmcpping.tools.PingTool;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class McpServerConfig {

    @Bean
    public ToolCallbackProvider toolCallbackProvider(PingTool pingTool) {
        return MethodToolCallbackProvider.builder()
                .toolObjects(pingTool)
                .build();
    }
}