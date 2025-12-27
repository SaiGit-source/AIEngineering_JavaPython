package com.mcp.MCPServer.config;

import com.mcp.MCPServer.tools.DateTimeTool;
import com.mcp.MCPServer.tools.NewsTool;
import org.springframework.ai.support.ToolCallbacks;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class McpServerConfig {

    @Bean
    public List<ToolCallback> toolCallBacks(DateTimeTool dateTimeTool, NewsTool newsTool){
        return List.of(ToolCallbacks.from(dateTimeTool, newsTool));
    }
// we are specifying the capabilities of the MCP server
    // primitives

}
