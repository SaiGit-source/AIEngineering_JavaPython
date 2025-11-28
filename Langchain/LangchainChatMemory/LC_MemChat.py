
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
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import MessagesPlaceholder

# prompt = "What is the capital of France?"
## User prompts are something you get from user directly
## System prompts are pre-defined instructions for the AI model, they will help you talk to LLMs about their roles, limitations etc
## we can use templates to add additional texts to prompts

## prompt = ChatPromptTemplate.from_messages("Tell me a joke about tech")
# ...existing code...
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Answer concisely."),
    MessagesPlaceholder("history"),
    ("user", "{input}")
])  # for continuous chat
# ...existing code...
 ## for continuous chat
## send info from previous chat

llm = ChatOpenAI(model="gpt-4o")

parser = StrOutputParser()
## Note: HTTPProtocol and Server are stateless. Each request is independent and does not retain any information from previous requests.
## So, to maintain context in a chat application, you need to explicitly pass the conversation history
## LLMs are stateless by default

## In Langchain, no such thing as Advisors or short-cut, unlike SpringAI

print("Chat with AI (type 'exit' or 'quit' to quit)\n")


store = {} ## to store chat history
## Redis or MongoDB can be used for production level applications to store chat history
session_id = "sai_session_1"  ## in real-world applications, you can use user_id or generate a unique session id for each user

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store.get(session_id, [])

chain  = prompt | llm | parser
chain_with_history = RunnableWithMessageHistory(chain, 
                                                get_session_history,
                                                input_messages_key="input",
                                                history_messages_key="history")

while True:
    value = input("you: ")
    if (value.lower() == "exit" or value.lower() == "quit"):
        break
    
    response = chain_with_history.invoke({"input": value},
                                         config={"configurable": {"session_id": session_id}}) ## instead of just sending the value we have to send the previous chat history
    
    print("AI: "+ response)


## LCEL
## you create a chain of things then you provide the prompt, meaning output of the prompt will become input for the model, output of the model becomes output of the chain

### Output
### Chat with memory
"""
you: What's LLM in one line
AI: LLM stands for "Large Language Model," which is an AI model designed to understand and generate human-like text based on vast amounts of language data.
you: What's RNN in one line?
AI: RNN stands for "Recurrent Neural Network," which is a type of artificial neural network designed to process sequential data by using feedback loops to maintain context across time steps.
you: How are they two related?
AI: Both RNNs and LLMs are types of neural networks used in natural language processing, but LLMs often rely on more advanced architectures like Transformers, which have largely replaced traditional RNNs due to their superior ability to handle long-range dependencies and parallelize training.
"""