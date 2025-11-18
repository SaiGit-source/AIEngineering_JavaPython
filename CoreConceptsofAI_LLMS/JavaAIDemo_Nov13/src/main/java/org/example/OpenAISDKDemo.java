package org.example;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

// SDK demo
// Copied template code from OpenAI Libraries: https://platform.openai.com/docs/libraries?language=java
// Go to Edit Configurations --> Add Environment variable : OPENAI_API_KEY
// Output:
// Response{id=resp_0dd0cc4d9a9a5f4700691bacd24bc88196abbc4655ff7b9034, createdAt=1.763421394E9, error=null, incompleteDetails=null, instructions=null, metadata=Metadata{additionalProperties={}}, model=ResponsesModel{chat=gpt-5-nano-2025-08-07}, object_=response, output=[ResponseOutputItem{reasoning=ResponseReasoningItem{id=rs_0dd0cc4d9a9a5f4700691bacd2bb588196abee4280b451ae39, summary=[], type=reasoning, content=, encryptedContent=, status=, additionalProperties={}}}, ResponseOutputItem{message=ResponseOutputMessage{id=msg_0dd0cc4d9a9a5f4700691bacd7185081969c636faa8fa695a8, content=[Content{outputText=ResponseOutputText{annotations=[], text=Hackers, type=output_text, logprobs=[], additionalProperties={}}}], role=assistant, status=completed, type=message, additionalProperties={}}}], parallelToolCalls=true, temperature=1.0, toolChoice=ToolChoice{options=auto}, tools=[], topP=1.0, background=false, conversation=, maxOutputTokens=null, maxToolCalls=null, previousResponseId=null, prompt=, promptCacheKey=null, reasoning=Reasoning{effort=medium, generateSummary=, summary=null, additionalProperties={}}, safetyIdentifier=null, serviceTier=default, status=completed, text=ResponseTextConfig{format=ResponseFormatTextConfig{text=ResponseFormatText{type=text, additionalProperties={}}}, verbosity=medium, additionalProperties={}}, topLogprobs=0, truncation=disabled, usage=ResponseUsage{inputTokens=16, inputTokensDetails=InputTokensDetails{cachedTokens=0, additionalProperties={}}, outputTokens=392, outputTokensDetails=OutputTokensDetails{reasoningTokens=384, additionalProperties={}}, totalTokens=408, additionalProperties={}}, user=null, additionalProperties={store=true, prompt_cache_retention=null, billing={payer=developer}}}
// text is text=Hackers,
// on one hand, when we are using OpenAI SDK we are adding one dependency and it makes the code bulky and on the other hand, we are writing only fewer lines of codes
// as we move towards SpringAI, number of lines will go down on the other hand, we have way more dependencies


public class OpenAISDKDemo {
    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.fromEnv();

        ResponseCreateParams params = ResponseCreateParams.builder()
                .input("name one movie for Software engineers, just the name")
                .model("gpt-5-nano")
                .build();

        Response response = client.responses().create(params);
        System.out.println(response);
        // System.out.println(response.outputText()); doesn't work from OpenAI website itself
    }
}