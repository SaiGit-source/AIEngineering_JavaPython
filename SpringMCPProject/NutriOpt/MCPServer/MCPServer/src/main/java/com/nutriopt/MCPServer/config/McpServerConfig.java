package com.nutriopt.MCPServer.config;

import com.nutriopt.MCPServer.tools.FoodStorageTool;
import com.nutriopt.MCPServer.tools.LpOptimizerTool;
import com.nutriopt.MCPServer.tools.OpenFoodFactsTool;
import com.nutriopt.MCPServer.tools.OpenPricesTool;
import com.nutriopt.MCPServer.tools.PingTool;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class McpServerConfig {

    @Bean
    public ToolCallbackProvider toolCallbackProvider(
            PingTool pingTool,
            OpenPricesTool openPricesTool,
            OpenFoodFactsTool openFoodFactsTool,
            FoodStorageTool foodStorageTool,
            LpOptimizerTool lpOptimizerTool
    ) {
        return MethodToolCallbackProvider.builder()
                .toolObjects(
                        pingTool,
                        openPricesTool,
                        openFoodFactsTool,
                        foodStorageTool,
                        lpOptimizerTool
                )
                .build();
    }
}