from groq import Groq
from telegram import Update
from telegram.ext import ContextTypes
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
# loading variables from .env file
load_dotenv() 

# accessing the bot token from .env file
openaiToken = os.getenv("OPENAI_TOKEN")
metaToken = os.getenv("METAAI_TOKEN")
groqToken = os.getenv("GROQ_TOKEN")
#print("BOT_TOKEN = ", botToken)
#print("OPENAI_TOKEN = ", botToken)


def botReply(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Getting the user input from the message
        prompt = update.message.text[3:]
        print("User Input = ", prompt)
        try:
            reply = func(prompt)
        except:
            reply = "Something is wrong. Check with the developer."
        print(reply)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
    return wrapper

@botReply
def groq(prompt):
    client = Groq(
        api_key=groqToken
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    reply = chat_completion.choices[0].message.content
    return reply
    

@botReply
def metaAI(prompt):
    endpoint = "https://api.meta.ai/text/generate"

    headers = {"Authorization": f"Bearer {metaToken}"}
    data = {"prompt": prompt}

    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        print(result["text"])
    else:
        print("Error:", response.status_code)
    
    return result["text"]


async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Getting the user input from the message
    prompt = update.message.text[3:]
    print("User Input = ", prompt)
    
    # Creating OpenAI Client
    base_url = "https://api.aimlapi.com"
    client = OpenAI(api_key = openaiToken, base_url=base_url)
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    )
    
    # Replying to user prompt
    reply = completion.choices[0].message.content
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)