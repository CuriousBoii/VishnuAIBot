import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

# accessing the bot token from .env file
botToken = os.getenv("BOT_TOKEN")
openaiToken = os.getenv("OPENAI_TOKEN")
#print("BOT_TOKEN = ", botToken)
#print("OPENAI_TOKEN = ", botToken)

# Creating OpenAI Client
from openai import OpenAI
base_url = "https://api.aimlapi.com"
client = OpenAI(api_key = os.getenv("OPENAI_TOKEN"), base_url=base_url)

# Logging the updates. This helps in debugging the code.
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Getting the user input from the message
    user_input = update.message.text[3:]
    print("User Input = ", user_input)
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input}
    ]
    )
    reply = completion.choices[0].message.content
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

if __name__ == '__main__':
    application = ApplicationBuilder().token(token=botToken).build()
    
    start_handler = CommandHandler('ai', ai)
    application.add_handler(start_handler)
    
    application.run_polling()