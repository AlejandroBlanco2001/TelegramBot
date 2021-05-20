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
    bot.sendAudio(chat_id=update.effective_chat.id, audio=open('Saludo.mp3','rb'))
    bot.send_message(chat_id=update.effective_chat.id, text=f"Aló, con Dorian. ¿Qué más {username}? ¿Todo bien? \n"+
                                                                "Estos son los comandos que puedes usar, anota que no repito: \n" +
                                                                "\t \t /recurrencia - Solución de una relación de recurrencia (Constantes no especificadas)\n" +
                                                                "\t \t /recurrenciaVi - Solución de una relación de recurrencia (Constantes especificadas) \n"
                                                                "\t \t /grafo -  Grafo simple con tus parámetros \n" +
                                                                "\t \t /fibonacci - Subsecuencia de Fibonacci en la secuencia que me des. \n" +
                                                                "Si no tienes conocimiento de qué puedo hacer " +  
                                                                "y cómo puedes pedirme que lo haga, tienes la libertad" +
                                                                "de escribir /LlamaFiscalia y te explicaré a detalle"+
                                                                " cada una de mis capacidades.")

def echo(update: Update, context: CallbackContext) -> None:
    start(update, context)

def send_help(update: Update, context: CallbackContext) -> None:
    bot.send_message(chat_id=update.effective_chat.id, text= f"/grafo \n \nEs el comando con el que me puedes pedir generar un grafo simple aleatorio "+
                    "donde tú brindas la cantidad de vertices a utilizar, la cantidad de aristas y el grado máximo que pueden "+
                    "presentar los vértices. \nEl comando se introduce con el siguente formato: "+
                    "\n \n \t \t /grafo v a k : 'v' son los vertices, 'a' las aristas, 'k' grado máximo, \n \t \t donde 'v' es estrictamente positvo y 'a' y 'k' deben ser mínimo 0 \n \n"+
                    "/recurrencia \n \nEncuentra la solución de una relación de recurrencia dado su polinomio característico, pero este comando no especifica las constantes de la solución,"
                    + "ya que no requiere ningún caso base. El comando se introduce con el siguiente formato"+
                    "\n \n \t \t /recurrencia polinomio : Donde 'polinomio' es el polinomio \n \t \t característico escrito por ejemplo de la forma x^2+1 \n \n"
                    "/recurrenciaVi \n \nEs el comando que te brinda la solución de la /recurrencia de la cuál tú brindas su polinimio característico y sus casos base."+
                    "\nEl comando se introduce con el siguiente formato: "+
                    "\n \n \t \t /recurrenciaVi polinomio casos : Donde 'polinomio' es el \n \t \t polinomio característico y 'casos' los valores iniciales para \n \t \t la recurrencia \n"+
                    "\t \t  Ejemplo de entrada: /recurrenciaVi x^3+2x^2 1,2,3 donde f_0 = 1 \n \t \t f_1 = 2 y f_2 = 3 \n \n"+
                    "/fibonacci \n \n Es el comando que te encuentra una subsecuencia de fibonacci tomando una secuencia ingresada por tí como base,"+
                    "\n es posible que te devuelva siempre una secuencia diferente en el caso de haber varias posibles. El comando se introduce con el siguiente formato: "
                    "\n \n \t \t /fibonacci secuencia : Donde 'secuencia' es la secuencia base a \n \t \t tomar, donde los números están separados por espacios.")
                                                        
def recurrencia(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0 or len(context.args) > 1:
        bot.send_message(chat_id=update.effective_chat.id,text="Por favor ingrese un parametro")
    equation = " ".join(context.args).strip()
    function = resolve_characteristical_polynomial(equation)
    sp.preview(function,viewer="file",filename="function.png", euler=False,
            dvioptions=["-T", "tight", "-z", "0", "--truecolor", "-D 600", "-bg", "Transparent"])
    bot.send_photo(chat_id=update.effective_chat.id, photo=open(
            "function.png", 'rb'), caption=f"Función que representa el polinomio característico {equation}")
    
def recurrencia_valor_inicial(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0 or len(context.args) > 2:
        bot.send_message(chat_id=update.effective_chat.id,text="Por favor ingrese dos parametro")
    equation = " ".join(context.args[0]).strip()
    initial_values = context.args[1]
    function = resolve_characteristical_polynomial_initial_value(equation,initial_values)
    sp.preview(function,viewer="file",filename="function.png", euler=False,
            dvioptions=["-T", "tight", "-z", "0", "--truecolor", "-D 600", "-bg", "Transparent"])
    bot.send_photo(chat_id=update.effective_chat.id, photo=open(
            "function.png", 'rb'), caption=f"Función que representa el polinomio característico {equation}" +
                f"con valores iniciales {str(initial_values)}")
        
def grafo(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 0 or len(context.args) > 3:
        bot.send_message(chat_id=update.effective_chat.id,text="Por favor ingrese tres parametros")
    vertices, aristas, maximum_degree = context.args
    try:
        vertices = int(vertices)
        aristas = int(aristas)
        maximum_degree = int(maximum_degree)
    except Exception:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="Alguno de los valores ingresados no es un numero.")
    if vertices <= 0 or aristas < 0 or maximum_degree < 0:
        bot.send_message(chat_id=update.effective_chat.id, text="Algun valor ingresado es negativo,"
                                + "por favor ingresa numeros positivos.")
    elif vertices <= 0:
        bot.send_message(chat_id=update.effective_chat.id, text="¿Por qué dibujar grafos nulos cuando puedes hacerlos simples?"+
                        "ingresa una cantidad de vértices mayor que 0.")
    bot.send_message(chat_id=update.effective_chat.id,
                                text="Cógela con su avena y su pitillo, estoy procesando el grafo.")
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
                                text="No es posible hacer un grafo simple con los parametros dados.")

def fibonazzi(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0 or len(context.args) < 2:
        bot.send_message(chat_id=update.effective_chat.id,text="Por favor ingrese una serie con más de dos valores")
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

    # Math functions
    dp.add_handler(CommandHandler('grafo', grafo))
    dp.add_handler(CommandHandler('recurrencia', recurrencia))
    dp.add_handler(CommandHandler('fibonacci', fibonazzi))
    dp.add_handler(CommandHandler('recurrenciaVi', recurrencia_valor_inicial))
    
    # Listener for not commands entry
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
