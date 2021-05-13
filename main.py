import requests
import logging  

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

bot = Bot(token=TOKEN)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = loggin.getLogger(__name__)

def main():
    updater = Updater("TOKEN", user_context=true)
    dp = updater.dispatcher
    
if __name__ == '__main__':
    main()
