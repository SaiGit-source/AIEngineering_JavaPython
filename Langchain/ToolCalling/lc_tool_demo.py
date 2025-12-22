from langchain_core.tools import tool
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()


@tool("get_current_date_time")
def get_current_date_time() -> str:
    """Get the current date and time in the format YYYY-MM-DD HH:MM:SS."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

messages = []

query = "What is the current date and time?"

messages.append(HumanMessage(content=query))

## User sends request to LLM
## LLM should send you a response LLM -> calls a tool
## tool -> returns the current date and time
## LLM -> returns the response to the user

## User message is the user query
## System message is you as a developer will set in the system
## The AI message is the message you receive from the LLM
## Tool message is the message you receive from the tool

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools([get_current_date_time])
#response = llm.invoke(query)

ai_msg = llm_with_tools.invoke(messages)
## we need to send human_message, tool_message and ai_msg to the LLM
messages.append(ai_msg)    

if ai_msg.tool_calls[0]["name"] == "get_current_date_time":
    tool_message = get_current_date_time.invoke({})
    messages.append(ToolMessage(content=tool_message, tool_call_id=ai_msg.tool_calls[0]["id"]))
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)

print(messages)

## Output
'''
I'm unable to provide real-time information, including the current date and time. However, you can easily check this on your device or by using a search engine.
'''

'''
content="I'm unable to provide real-time information or the current date and time. You can check the date and time on your device or use an online clock for the most accurate information." additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 35, 'prompt_tokens': 15, 'total_tokens': 50, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_deacdd5f6f', 'id': 'chatcmpl-Cpgu7DohNRuihlg7uIubA3KHjC50S', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019b47c5-86d5-7cf0-999e-250ebacf192e-0' usage_metadata={'input_tokens': 15, 'output_tokens': 35, 'total_tokens': 50, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
'''
## if 'finish_call' is 'tool_calls' it will not give content
## we are not using Agent executor or AgenticAI, so we have to do certain things manually


### After modifications, the output should be:
'''
m_fingerprint': 'fp_deacdd5f6f', 'id': 'chatcmpl-CphGy8G658GvcnSnyByW7m0YH5Zz6', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--019b47db-232f-70d0-b2f6-17c8563cedd0-0', tool_calls=[{'name': 'get_current_date_time', 'args': {}, 'id': 'call_ysqMFacdcdRC2u3l6XdZGzpV', 'type': 'tool_call'}], usage_metadata={'input_tokens': 59, 'output_tokens': 12, 'total_tokens': 71, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}), ToolMessage(content='2025-12-22 15:58:24', tool_call_id='call_ysqMFacdcdRC2u3l6XdZGzpV'), AIMessage(content='The current date and time is 2025-12-22 15:58:24.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 21, 'prompt_tokens': 93, 'total_tokens': 114, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_deacdd5f6f', 'id': 'chatcmpl-CphH0BzV7FJYodQGrDVlqzOho47zB', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019b47db-2aab-7323-b126-bdf4a489b756-0', usage_metadata={'input_tokens': 93, 'output_tokens': 21, 'total_tokens': 114, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]
'''

### AIMessage(content='The current date and time is 2025-12-22 15:58:24.' it got the content