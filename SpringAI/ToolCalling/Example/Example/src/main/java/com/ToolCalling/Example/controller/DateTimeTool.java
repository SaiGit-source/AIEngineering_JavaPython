package com.ToolCalling.Example.controller;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;

@Component
public class DateTimeTool {

    @Tool(description="Get current date and time for user's timezone")
    public String getCurrentDateTime(){
        // return java.time.LocalDateTime.now().toString();
        System.out.println("in local timezone");
        return java.time.ZonedDateTime.now().toString();
    }

    @Tool(description="Get current date and time for specified timezone")
    public String getSpecifiedDateTime(String timezone){
        // return java.time.LocalDateTime.now().toString();
        System.out.println("in specified timezone");
        return java.time.ZonedDateTime.now(java.time.ZoneId.of(timezone)).toString();
    }

}
