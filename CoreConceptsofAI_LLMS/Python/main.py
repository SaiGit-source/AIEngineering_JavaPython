## install Python
## install uv
## uv is very fast compared to pyenv, poetry, pipenv
## i created a virtual environment with `python -m venv .venv` and activated it
## instead of venv, use uv venv command
## then installed uv with `python -m pip install uv`
## (.venv)  uv init
## Initialized project `aiengineering-javapython`
# """
# (.venv) uv add python-dotenv
# Resolved 2 packages in 443ms
# Prepared 1 package in 243ms
# Installed 1 package in 206ms
#  + python-dotenv==1.2.1
#  """
 
# """ 
# python -m uv venv                                                                                            Using CPython 3.12.5 interpreter at: C:\Users\saito\AppData\Local\Programs\Python\Python312\python.exe
# Creating virtual environment at: .venv
# Activate with: .venv\Scripts\activate
# """
## dont forget to run uv init before 'uv add python-dotenv'
## create .env file for environment variables
## in .env file, add OPENAI_API_KEY=your_api_key
## then in python code, load the .env file and access the environment variable
## uv add requests

from dotenv import load_dotenv
import os, requests
load_dotenv()  # take environment variables from .env.

api_key = os.getenv("OPENAI_API_KEY")
#print("API Key:", api_key)

# Now you can use
# api_key to authenticate with OpenAI's services
uri = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

payload = {
    "model": "gpt-4o",
    "messages": [
        {"role": "user", "content": "name one good Hollywood movie about space exploration"}
    ],
}
     
     
response = requests.post(uri, headers=headers, json=payload)   

print(response.json()["choices"][0]["message"]["content"])    

## Output: obviously the one-of-a-kind great movie
## One highly acclaimed Hollywood movie about space exploration is "Interstellar" (2014), directed by Christopher Nolan. The film explores the journey of a group of astronauts who travel through a wormhole in search of a new home for humanity as Earth becomes uninhabitable. It combines scientifically grounded concepts with emotional storytelling and impressive visual effects.  





