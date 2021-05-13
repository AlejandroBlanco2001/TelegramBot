import requests
import logging  
import config

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = loggin.getLogger(__name__)

def start(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="SIUUU")

def main():
    
    updater = Updater(config.TOKEN, user_context=true)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))
    updater.start_polling()

if __name__ == '__main__':
    main()
