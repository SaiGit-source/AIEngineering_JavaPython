
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from pathlib import Path
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()
## We have to use Chroma because MariaDB is not updated for Langchain
### Load documents first

data_path = Path(__file__).resolve().parent / "product_details.txt"
if not data_path.exists():
    raise FileNotFoundError(f"{data_path} not found. Place product_details.txt next to rag_example.py or update the path.")
loader = TextLoader(str(data_path), encoding="utf8")  ## encoding very important
docs = loader.load()
# print(type(docs[0]))

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50) ## chunk_size is number of chars you want in one line, chunk_overlap is number of chars to overlap between lines, some characters from previous line/chunk will be repeated in next line
splits = splitter.split_documents(docs)
# print(splits[0].page_content)
"""Title: "Bluetooth Wireless Earbuds"
Description: Noise-canceling earbuds with up to 30 hours battery life and fast charging support. Sweat and water-resistant.
Price: $49.99
Category: Electronics
Features: Touch controls, Charging case, Bluetooth 5.3, Built-in microphone
"""
vectordb = Chroma.from_documents(documents=splits, 
                                 embedding=OpenAIEmbeddings(),
                                 persist_directory="chroma_db")  ## embedding_function=None uses default OpenAI embeddings

retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k":2})  ## k is number of similar documents to retrieve

## question from user and matches or context from the vectorstore
template = """You are a helpful e-commerce product assistant. Use the following product details to answer the question.
If the answer is not contained within the product details, respond with "I don't know".
{context}
Question: {question}
Answer in a concise manner."""

prompt = PromptTemplate.from_template(template)
llm = ChatOpenAI(temperature=0, model_name="gpt-4o")  ## temperature 0 for deterministic output 
parser = StrOutputParser()

chain = (
        {"context": retriever, "question": RunnablePassthrough()}  # retriever is runnable
        | prompt 
        | llm 
        | parser) ## this chain is possible because they are runnable

response = chain.invoke("Suggest products for vacation")
print(response)

### Output
""""Waterproof Travel Backpack" and "Mini Air Purifier" are suitable products for vacation.
"""