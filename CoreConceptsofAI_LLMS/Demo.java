/// we can write a lot of code.
// we inject something here for LLM
/// we can use OpenAI, Gemini, Claude
// However, cloud services are not free
// first i need to login into OpenAI: https://auth.openai.com/log-in
// then i can use the API key to call the service
// https://platform.openai.com/settings/organization/api-keys
// Create new secret key
// Either use API key to call OpenAI models or download models in local
// Go to Ollama and download models
// Use Gemma3 or deepseek-r1
// open Powershell and type ollama run deepseek-r1:1.5b
// for OpenAI, you got to pay like $5
// look for openAI library: https://platform.openai.com/docs/libraries

// select Java
//  ResponseCreateParams params = ResponseCreateParams.builder()
// whatever you do on ChatGPT you can do it programmatically


// we are not going to use this code. we are going to IntelliJ

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

public class Main {
    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.fromEnv();

        ResponseCreateParams params = ResponseCreateParams.builder()
                .input("Say this is a test")
                .model("gpt-5-nano")
                .build();

        Response response = client.responses().create(params);
        System.out.println(response.outputText());
    }
}











