
from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

api_key = os.getenv("OPENAI_API_KEY")
from langchain_core.prompts import ChatPromptTemplate
## one is the PromptTemplate from langchain_core.prompts
## another is ChatPromptTemplate from langchain.prompts.chat
## if you want to build a chat application, always use the ChatPromptTemplate
from langchain_openai import ChatOpenAI


# prompt = "What is the capital of France?"
## User prompts are something you get from user directly
## System prompts are pre-defined instructions for the AI model, they will help you talk to LLMs about their roles, limitations etc
## we can use templates to add additional texts to prompts

prompt = ChatPromptTemplate.from_messages("Tell me a joke about tech")

