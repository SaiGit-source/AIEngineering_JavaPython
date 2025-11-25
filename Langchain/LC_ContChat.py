
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

## prompt = ChatPromptTemplate.from_messages("Tell me a joke about tech")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Answer concisely."),
    ("user", "{input}")
]) ## for continuous chat

llm = ChatOpenAI(model="gpt-4o")

parser = StrOutputParser()

print("Chat with AI (type 'exit' or 'quit' to quit)\n")
while True:
    inp = input("you: ")
    if (inp.lower() == "exit" or inp.lower() == "quit"):
        break
    chain  = prompt | llm | parser
    
    response = chain.invoke({"input": inp})

    print("AI: "+ response)
    


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
"""
you: Hello
AI: Hello! How can I assist you today?
you: What's Java in one line?
AI: Java is a high-level, object-oriented programming language known for its platform independence and "write once, run anywhere" capability.
you: what's 2+2
AI: 2 + 2 equals 4.
you:
    """
    