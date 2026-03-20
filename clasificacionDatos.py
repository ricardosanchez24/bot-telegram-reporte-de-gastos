import os
from dotenv import load_dotenv
from google import genai
#from prueba import lista_descripcion
load_dotenv()

def clasificacion_datos(lista_descripcion):
    api_key_gemini = os.environ.get('GEMINI_API_KEY')

    Cliente = genai.Client(api_key=api_key_gemini)

    promt = f'1. ROL Actúa como un experto en análisis de datos financieros y clasificación de transacciones bancarias en Venezuela.2. CONTEXTO Estás procesando movimientos bancarios de un estudiante de Ingeniería de Sistemas. Los datos provienen de transacciones de Pago Móvil, P2P y transferencias. 3. INSTRUCCIONES Clasifica la lista de DATOS DE ENTRADA basándote en el DICCIONARIO DE REGLAS.Si un comercio no está en el diccionario, usa el contexto de la descripción para inferir la categoría.Devuelve únicamente un JSON (lista de strings) con las categorías en el mismo orden.4. DICCIONARIO DE REGLAS (Prioridad Máxima)Alimentación: Si contiene "SUPERMERCADO", "PLAZAS", "AUTOMERCADOS", "PANADERIA", "RESTAURANTE", "PEDIDOSYA".Servicios: Si contiene "CANTV", "DIGITEL", "MOVISTAR", "CORPOELEC", "INTER", "NETUNO".Salud: Si contiene "FARMATODO", "FARMACIA", "LOCATEL", "CLINICA", "LABORATORIO".Transporte: Si contiene "GASOLINERA", "COMBUSTIBLE", "YUMMY RIDES", "REPUESTOS".Entretenimiento: Si contiene "NETFLIX", "SPOTIFY", "DISNEY", "CINES UNIDOS".Ingresos: Si contiene "NOMINA", "SUELDO", "BONO", "PAGO RECIBIDO".Otros: Si contiene "PAGO MOVIL A PERSONA" (sin comercio identificado) o "COMISION".Tecnologia: si contiene "monitor" "televisor","laptop","nevera","cafetera","audifonos".Cuidado personal: si contiene "campu","desodorante","perfume","pata dental".Ropa:si contiene "zapatos","camisa","pantalon","medias",sueter.5. RESTRICCIONES No incluyas texto fuera del JSON. No inventes categorías. Usa solo: [Alimentación, Servicios, Salud, Transporte, Entretenimiento, Ingresos, Otros].Si la descripción es solo un nombre de persona sin más contexto, clasifica como "Otros".6. DATOS DE ENTRADA{lista_descripcion}'

    response = Cliente.models.generate_content(
        model="gemini-3-flash-preview",contents=promt
    )
    return response.text

   