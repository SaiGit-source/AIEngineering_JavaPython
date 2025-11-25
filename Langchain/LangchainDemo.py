
from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

api_key = os.getenv("OPENAI_API_KEY")
from langchain_core.prompts import ChatPromptTemplate
## one is the PromptTemplate from langchain_core.prompts
## another is ChatPromptTemplate from langchain.prompts.chat
## if you want to build a chat application, always use the ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser  ## it gives answer in proper format

# prompt = "What is the capital of France?"
## User prompts are something you get from user directly
## System prompts are pre-defined instructions for the AI model, they will help you talk to LLMs about their roles, limitations etc
## we can use templates to add additional texts to prompts

prompt = ChatPromptTemplate.from_messages("Tell me a joke about tech")
## prompt = ChatPromptTemplate.from_messages({inp}) ## for continuous chat

llm = ChatOpenAI(model="gpt-4o")

parser = StrOutputParser()


## LCEL
## you create a chain of things then you provide the prompt, meaning output of the prompt will become input for the model, output of the model becomes output of the chain

chain = prompt | llm | parser ## output of prompt becomes input of llm
## there is a concept called "Runnable"
## this prompt and llm are both Runnables
## when you use the pipe operator, it creates a new Runnable that chains them together
# response = chain.invoke({})

response = chain.invoke({"subject": "Java"})

print(response)

## Output
"""content="Sure! Here's a joke about tech:\n\nWhy do programmers prefer dark mode?\n\nBecause light attracts bugs!" 
additional_kwargs={'refusal': None} 
response_metadata={'token_usage': {'completion_tokens': 20, 'prompt_tokens': 128, 'total_tokens': 148, 
'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 
'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_c98e05ca17', 'id': 'chatcmpl-CfeGev6DHsZhVTpbw1qQEVud9v6NE', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} 
id='lc_run--a411c8ba-e64c-4856-b5b1-5bb8d2a71b3b-0' 
usage_metadata={'input_tokens': 128, 'output_tokens': 20, 'total_tokens': 148, 
'input_token_details': {'audio': 0, 'cache_read': 0}, 
'output_token_details': {'audio': 0, 'reasoning': 0}}
"""


"""
content='Why did the web developer go broke? \n\nBecause they used up all their cache!
"""


"""
Sure, here's a lighthearted tech joke for you:

Why do programmers prefer dark mode?

Because the light attracts bugs!
    """
    
"""
    Why did the scarecrow win an award? Because he was outstanding in his field!

Okay, now tell me about your tech joke!
    """