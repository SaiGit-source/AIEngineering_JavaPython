## https://platform.openai.com/docs/libraries?language=python
## we got to load .env file here as well to access the environment variable

from dotenv import load_dotenv
import os, requests
load_dotenv()  # take environment variables from .env.

api_key = os.getenv("OPENAI_API_KEY")


from openai import OpenAI
client = OpenAI()


response = client.responses.create(
    model="gpt-5-nano",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)

## Output
## Under a quilt of stars, a gentle unicorn brushed the moonlight from its silver mane and drifted softly into dreams.

