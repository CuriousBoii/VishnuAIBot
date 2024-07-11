import os
from dotenv import load_dotenv
from openai import OpenAI

# load_dotenv() loads the environment variables from the .env file into the environment
load_dotenv()

# Declare OpenAI object with api token
base_url = "https://api.aimlapi.com"
client = OpenAI(api_key = os.getenv("OPENAI_TOKEN"), base_url=base_url)


completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message.content)
