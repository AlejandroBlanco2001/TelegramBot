import logging
import config
import sys
import sympy as sp
import matplotlib.pyplot as plt
import networkx as nx

from utils import *
from telegram import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

logger = logging.getLogger(__name__)

bot = Bot(token=config.TOKEN)

def start(update: Update, context: CallbackContext) -> None:
    username = update.message.chat["first_name"]
    bot.send_message(chat_id=update.effective_chat.id, text=f"Aló, con Dorian, {username} \n" +
                                                                    "cuento con los siguentes comandos \n" +
                                                                    "\t /LlamaFiscalia \n" +
                                                                    "\t /recurrencia \n" +
                                                                    "\t /recurrenciaVi \n"
                                                                    "\t /grafo \n" +
                                                                    "\t /subsecuencia \n" +
                                                                    "\t /dameOpciones")

def echo(update: Update, context: CallbackContext) -> None:
    start(update, context)

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
        bot.send_message(
            chat_id=update.effective_chat.id, text=f"Elige una función,{query.data}")
    elif query.data == "1":
        bot.send_message(chat_id=update.effective_chat.id, text="El comando de Recurrencia sin valor inicial " +
                                                                        "se encarga de recibir una entrada de la forma" +
                                                                        "tal tal tal tal")
    elif query.data == "2":
        bot.send_message(chat_id=update.effective_chat.id, text="El comando de Recurrencia con valor inicial " +
                                                                        "se encarga de recibir una entrada de la forma" +
                                                                        "tal tal tal tal")
    elif query.data == "3":
        bot.send_message(chat_id=update.effective_chat.id, text="El comando de Grafo se encarga de generar un grafo simplemente \n" +
                                                                        "teniendo en cuenta el numero de vertices, aristas y grado de maximo de los vertices " +
                                                                        "para luego ser mostrado en pantalla \nFormato de la entrada \n" +
                                                                        "v e k \nDonde v es el numero de vertices, k el numero de aristas y k el grado maximo")
    else:
        bot.send_message(chat_id=update.effective_chat.id, text="El comando de Subsecuencia se encarga de recibir" +
                                                                        "tal tal tal tal")

def send_help(update: Update, context: CallbackContext) -> None:
    pass

def recurrencia(update: Update, context: CallbackContext) -> None:
    equation = " ".join(context.args).strip()
    function = resolve_characteristical_polynomial(equation)
    sp.preview(function,viewer="file",filename="function.png", euler=False,
            dvioptions=["-T", "tight", "-z", "0", "--truecolor", "-D 600", "-bg", "Transparent"])
    bot.send_photo(chat_id=update.effective_chat.id, photo=open(
            "function.png", 'rb'), caption=f"Función que representa el polinomio caracteristico {equation}")
    
def recurrencia_valor_inicial(update: Update, context: CallbackContext) -> None:
    equation = " ".join(context.args[0]).strip()
    initial_values = context.args[1]
    function = resolve_characteristical_polynomial_initial_value(equation,initial_values)
    sp.preview(function,viewer="file",filename="function.png", euler=False,
            dvioptions=["-T", "tight", "-z", "0", "--truecolor", "-D 600", "-bg", "Transparent"])
    bot.send_photo(chat_id=update.effective_chat.id, photo=open(
            "function.png", 'rb'), caption=f"Función que representa el polinomio caracteristico {equation}" +
                f"con valores iniciales {str(initial_values)}")
        
def grafo(update: Update, context: CallbackContext) -> None:
    vertices, aristas, maximum_degree = context.args
    try:
        vertices = int(vertices)
        aristas = int(aristas)
        maximum_degree = int(maximum_degree)
    except Exception:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="Alguno de los valores ingresados no es un numero")
    if vertices <= 0 or aristas <= 0 or maximum_degree <= 0:
        bot.send_message(chat_id=update.effective_chat.id, text="Algun valor ingresado es negativo,"
                                + "por favor ingresa numeros positivos")
    bot.send_message(chat_id=update.effective_chat.id,
                                text="Cogela con su avena y su pitillo, estoy procesando el grafo")
    Graph = generate_graph(vertices, aristas, maximum_degree)
    if Graph != None:
        plt.clf() # In case that the figure has something in it 
        nx.draw(Graph)
        plt.savefig("graph.png")
        plt.close()
        bot.send_photo(chat_id=update.effective_chat.id, photo=open(
            "graph.png", 'rb'), caption=f"Grafo con {vertices} vertices, {aristas} aristas y con un grado limite {maximum_degree}")
    else:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="No es posible hacer un grafo con los parametros dados.")

def fibonazzi(update: Update, context: CallbackContext) -> None:
    sequence = [int(number) for number in context.args]
    if checkOrder(sequence):
        subsequence = sub_fibonacci_sequence(sequence)
        bot.send_message(chat_id=update.effective_chat.id,
                                text="Una posible subsecuencia que cumpla el principio de fibonacci a partir de " + str(sequence) + " es: \n"+
                                str(subsequence))
    else:
        bot.send_message(chat_id=update.effective_chat.id, text="La secuencia debe estar en orden ascedente")
        
def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    updater = Updater(config.TOKEN, use_context=True)
    dp = updater.dispatcher

    # Helper functions
    dp.add_handler(CommandHandler('Timbrar', start))
    dp.add_handler(CommandHandler('LlamaFiscalia', send_help))
    dp.add_handler(CommandHandler("dameOpciones", send_options))

    # Math functions
    dp.add_handler(CommandHandler('grafo', grafo))
    dp.add_handler(CommandHandler('recurrencia', recurrencia))
    dp.add_handler(CommandHandler('fibonacci', fibonazzi))
    dp.add_handler(CommandHandler('recurrenciaVi', recurrencia_valor_inicial))

    # Listener of the toolbox command
    dp.add_handler(CallbackQueryHandler(menu))

    # Listener for not commands entry
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
