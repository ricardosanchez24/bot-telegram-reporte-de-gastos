import os
import glob
import pandas as pd
import pdfplumber
import re

def procesar_estado_cuenta():
    # 1. Ubicar la carpeta de Descargas
    carpeta_descargas = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    patron_busqueda = os.path.join(carpeta_descargas, 'persona_bdv_cuenta_*.pdf')
    archivos_pdf = glob.glob(patron_busqueda)
    
    if not archivos_pdf:
        print("Error: No se encontró ningún PDF del banco en la carpeta de Descargas.")
        return

    archivo_objetivo = max(archivos_pdf, key=os.path.getctime)
    print(f"Procesando archivo: {os.path.basename(archivo_objetivo)}")

    datos_extraidos = []

    # 2. Abrir el PDF y extraer sin depender de las cabeceras
    with pdfplumber.open(archivo_objetivo) as pdf:
        for pagina in pdf.pages:
            tablas = pagina.extract_tables()
            
            for tabla in tablas:
                for fila in tabla:
                    # Nos aseguramos de que la fila no esté vacía y tenga al menos 5 columnas (para llegar a Débito)
                    if not fila or len(fila) < 5:
                        continue
                    
                    # Limpiamos los valores por si vienen como None
                    desc = str(fila[1] or "").replace('\n', ' ').strip()
                    fecha = str(fila[2] or "").strip()
                    debito = str(fila[4] or "").strip()

                    # 3. La magia: Si la columna fecha tiene formato DD/MM/AAAA y no es el saldo inicial
                    if re.search(r'\d{2}/\d{2}/\d{4}', fecha) and "SALDO INICIAL" not in desc:
                        # Filtramos los que tengan débito 0
                        if debito and debito not in ["0,00", "0.00"]:
                            datos_extraidos.append({
                                "Fecha": fecha,
                                "descripcion": desc,
                                "monto": debito
                            })

    # 4. Guardar los datos en el CSV
    if datos_extraidos:
        df = pd.DataFrame(datos_extraidos)
        ruta_csv = os.path.join(carpeta_descargas, 'datos_banco_procesados.csv')
        
        
        df.to_csv(ruta_csv, index=False, encoding='utf-8-sig', sep=',') 
        print(f"¡Éxito! Se extrajeron {len(df)} registros. Archivo guardado en: {ruta_csv}")
        return ruta_csv
    else:
        print("El script se ejecutó, pero no se encontraron datos de débito válidos.")

