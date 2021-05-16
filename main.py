import logging
import config
from utils import *
from telegram import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

logger = logging.getLogger(__name__)


def start(update, context):
    username = update.message.chat["first_name"]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Aló, con Dorian, {username} \n" +
                                                                    "cuento con los siguentes comandos \n" +
                                                                    "\t /LlamaFiscalia \n" +
                                                                    "\t /recurrencia \n" +
                                                                    "\t /recurrenciaVi \n"
                                                                    "\t /grafo \n" +
                                                                    "\t /subsecuencia \n" +
                                                                    "\t /dameOpciones")

def echo(update,context):
    start(update,context)

def send_options(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("LlamaFiscalia", callback_data='0'),
            InlineKeyboardButton("Recurrencia", callback_data='1'),
            InlineKeyboardButton(
                "Recurrencia con valor inicial", callback_data='2'),
            InlineKeyboardButton("Grafo", callback_data='3'),
            InlineKeyboardButton("Subsecuencia", callback_data='4'),
        ]
    ]
    reply = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Elige una función", reply_markup=reply)


def send_help(update: Update, context: CallbackContext) -> None:
    return None


def menu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == "0":
        context.bot.send_message(chat_id=update.effective_chat.id, text= f"Elige una función,{query.data}")
    elif query.data == "1":
        context.bot.send_message(chat_id=update.effective_chat.id, text= "El comando de Recurrencia sin valor inicial " + 
                                                                        "se encarga de recibir una entrada de la forma" +
                                                                        "tal tal tal tal")
    elif query.data == "2":
        context.bot.send_message(chat_id=update.effective_chat.id, text= "El comando de Recurrencia con valor inicial " + 
                                                                        "se encarga de recibir una entrada de la forma" +
                                                                        "tal tal tal tal")
    elif query.data == "3":
        context.bot.send_message(chat_id=update.effective_chat.id, text= "El comando de Grafo se encarga de generar un grafo simplemente \n" + 
                                                                        "teniendo en cuenta el numero de vertices, aristas y grado de maximo de los vertices " +
                                                                        "para luego ser mostrado en pantalla \nFormato de la entrada \n" +
                                                                        "v e k \nDonde v es el numero de vertices, k el numero de aristas y k el grado maximo")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text= "El comando de Subsecuencia se encarga de recibir" + 
                                                                        "tal tal tal tal")


def send_help(update: Update, context: CallbackContext) -> None:
    pass

def grafo(update, context):
    vertices,aristas,maximum_degree =  " ".join(context.args).strip().split(" ")
    try:
        vertices = int(vertices)
        aristas = int(aristas)
        maximum_degree = int(maximum_degree)
    except Exception:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Alguno de los valores ingresados no es un numero")
    if vertices < 0 or aristas < 0 or maximum_degree < 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Algun valor ingresado es negativo," 
                                + "por favor ingresa numeros positivos")
    Graph = generate_graph(vertices,aristas,maximum_degree)



def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    updater = Updater(config.TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('Timbrar', start))
    dp.add_handler(CommandHandler('LlamaFiscalia', send_help))
    dp.add_handler(CommandHandler("dameOpciones", send_options))
    dp.add_handler(CommandHandler('grafo', grafo))
    # Listener of the toolbox command
    dp.add_handler(CallbackQueryHandler(menu))
    # Listener for not commands entry 
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    dp.add_handler(CommandHandler('test', help))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
