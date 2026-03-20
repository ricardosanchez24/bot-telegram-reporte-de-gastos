import os
from dotenv import load_dotenv

import logging
from telegram import Update , InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters,MessageHandler,ApplicationBuilder,ContextTypes,CommandHandler, InlineQueryHandler
from uuid import uuid4

import matplotlib.pyplot as plt
import numpy as np

from graficador_datos import graficador

load_dotenv()
token = os.environ.get('TOKEN_BOT')

#datos_graficados = graficador

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text='Este es mi mensaje de Bot Felicidades eres increible')

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    datos_graficados = graficador()

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=datos_graficados ,caption="Aqui esta el reporte de los gastos")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text )    


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper() # context.args crea una lista de str que se pega al lado de un comando, gracias a join se usa un espacio como delimitador
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return

    result = []
    result.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='caps',
            input_message_content=InputTextMessageContent(query.upper())
        )    
    )
    await context.bot.answer_inline_query(update.inline_query.id, result)

# este controlador debe agg siempre al final
async def unknow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Lo siento ese comando no es reconocido')    

if __name__ == '__main__':
    app = ApplicationBuilder().token(token=token).build()

    accion_esperada = CommandHandler('start',start)
    caps = CommandHandler('caps',caps)
    r = CommandHandler('report',report)
    eco = MessageHandler(filters.TEXT & (~filters.COMMAND),echo)
    inline = InlineQueryHandler(inline_caps)
    comando_no_reconocido = MessageHandler(filters.COMMAND,unknow)


    app.add_handler(accion_esperada)
    app.add_handler(caps)
    app.add_handler(r)
    app.add_handler(eco)
    app.add_handler(inline)
    # este controlador debe agg al final siempre
    app.add_handler(comando_no_reconocido)

    app.run_polling()
    