import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from functions import *
# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

# accessing the bot token from .env file
botToken = os.getenv("BOT_TOKEN")


# Logging the updates. This helps in debugging the code.
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )
if __name__ == '__main__':
    application = ApplicationBuilder().token(token=botToken).build()
    openAI_handler = CommandHandler('ai', groq)
    metaAI_handler = CommandHandler('fb', metaAI)
    application.add_handler(openAI_handler)
    application.add_handler(metaAI_handler)
    application.run_polling()