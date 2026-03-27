import os
from dotenv import load_dotenv

import logging
from telegram import Update , InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters,MessageHandler,ApplicationBuilder,ContextTypes,CommandHandler, InlineQueryHandler
from uuid import uuid4

import matplotlib.pyplot as plt
import numpy as np

# =========================================================
# IMPORTACIONES DE MÓDULOS DE NEGOCIO (Nuestra Orquesta)
# =========================================================
# Importamos cada función específica en lugar del módulo completo 
# para mantener el espacio de nombres limpio y saber exactamente qué usamos.
from datos_banco_BDV import procesar_estado_cuenta
from procesador_datos import procesador
from graficador_datos import graficador

load_dotenv()
token = os.environ.get('TOKEN_BOT')
telegram_id = os.environ.get('TELEGRAM_ID')

#datos_graficados = graficador

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text='Este es mi mensaje de Bot Felicidades eres increible')

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Controlador del comando /report.
    Actúa como Orquestador: delega tareas a los módulos especializados
    y pasa los resultados en cadena.
    """
    # Guardamos el ID del chat en una variable para no repetirlo múltiples veces. (Principio DRY: Don't Repeat Yourself)
    chat_id = update.effective_chat.id
    
    if str(chat_id) != str(telegram_id):
        await context.bot.send_message(chat_id=chat_id, text='Lo siento pero no tiene autorizacion para usar este bot')
        return
    # 1. Feedback inmediato: Los procesos con LLMs (Gemini) o archivos tardan. 
    # Siempre debemos avisar al usuario para que no crea que el bot "se colgó".
    await context.bot.send_message(
        chat_id=chat_id, 
        text="⏳ Iniciando la generación de tu reporte. Procesando documentos..."
    )

    # 2. Bloque Try/Except: Al centralizar, si el PDF falla, o Gemini no responde, 
    # el programa no "explota" crasheando el bot entero. Capturamos el error aquí.
    try:
        # --- FASE 1: EXTRACCIÓN ---
        # Llamamos al módulo de PDF. Esperamos que devuelva la ruta del archivo.
        ruta_archivo_csv = procesar_estado_cuenta()
        
        # Validación Temprana (Guard Clause): Si no hay ruta, abortamos limpiamente.
        if not ruta_archivo_csv:
            await context.bot.send_message(chat_id=chat_id, text="❌ Error: No se encontró un estado de cuenta válido en tus Descargas.")
            return # El return evita que el código siga ejecutándose hacia abajo.

        # --- FASE 2: PROCESAMIENTO E IA ---
        # Le pasamos la ruta al procesador para que hable con Gemini y nos devuelva la lista.
        datos_procesados = procesador(ruta_archivo_csv)
        
        if not datos_procesados:
            await context.bot.send_message(chat_id=chat_id, text="❌ Error: Hubo un problema clasificando los datos.")
            return

        # --- FASE 3: VISUALIZACIÓN ---
        # Pasamos los datos limpios al graficador. 
        # (Nota: Esto fallará si probamos AHORA MISMO porque graficador_datos.py aún no acepta parámetros. Lo arreglaremos en el siguiente paso).
        imagen_grafico = graficador(datos_procesados)

        # --- FASE 4: ENTREGA ---
        # Todo salió bien, enviamos la imagen.
        await context.bot.send_photo(
            chat_id=chat_id, 
            photo=imagen_grafico, 
            caption="📊 Aquí tienes el reporte clasificado de tus gastos."
        )

    except Exception as error_inesperado:
        # Si algo rarísimo pasa (ej. se cae el internet), el bot responde educadamente
        # e imprime el error técnico en la consola del servidor para que nosotros (los devs) lo veamos.
        print(f"ERROR CRÍTICO en /report: {error_inesperado}")
        await context.bot.send_message(
            chat_id=chat_id, 
            text="⚠️ Ocurrió un error inesperado en los sistemas. Por favor, intenta de nuevo más tarde."
        )

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
    