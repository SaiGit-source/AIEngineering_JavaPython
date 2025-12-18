package controller;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;

@Component
public class DateTimeTool {

    @Tool
    public String getCurrentDateTime(){
        return java.time.LocalDateTime.now().toString();
    }

}
