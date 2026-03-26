import os
from dotenv import load_dotenv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

load_dotenv()
usuario = os.environ.get('USER_BANCO')
contraseña = os.environ.get('CONTRASEÑA_BANCO')

def scraper():

    driver = webdriver.Chrome()

    url = "https://bdvenlinea.banvenez.com/"

    driver.get(url)

    driver.implicitly_wait(5)

    campo_user = driver.find_element(by=By.ID,value="mat-input-0")

    campo_user.send_keys(usuario)

    boton = driver.find_element(By.TAG_NAME,"button")
    boton.click()

    driver.implicitly_wait(5)

    campo_contraseña = driver.find_element(By.ID, "mat-input-1")
    campo_contraseña.send_keys(contraseña)

    # Definimos un wait estándar para reutilizar
    wait = WebDriverWait(driver, 2.5)

    boton_contraseña = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]")))
    boton_contraseña.click()

    driver.implicitly_wait(1)

    barra_opciones = driver.find_elements(By.CLASS_NAME, "mat-button")
    boton_solicitudes = barra_opciones[4]
    boton_solicitudes.click()

    time.sleep(1.5)
    
    opciones_solicitudes = driver.find_elements(By.CLASS_NAME,"mat-menu-item")
    estados_financieros_page = opciones_solicitudes[5]
    estados_financieros_page.click()
    
    
    '''
    estados_financieros_page = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Estados financieros')]")))
    estados_financieros_page.click()
    #driver.implicitly_wait(5)
    '''
    # --- SECCIÓN CORREGIDA PARA SELECCIÓN DE ESTADOS FINANCIEROS ---

    # 1. Seleccionar tipo de instrumento (Cuenta)
    dropdown = wait.until(EC.element_to_be_clickable((By.ID, "mat-select-0")))
    dropdown.click()
    
    opcion_cuenta = wait.until(EC.element_to_be_clickable((By.ID, "mat-option-0")))
    opcion_cuenta.click()
    '''
    # --- BLOQUE PARA SALTAR TÉRMINOS Y CONDICIONES ---
    try:
        # Esperamos unos segundos a ver si aparece el checkbox de "Aceptar términos"
        # Usamos un tiempo corto (3 seg) para no retrasar el script si no aparece
        check_terminos = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//mat-checkbox[contains(., 'Aceptar términos')]"))
        )
        print("Validación de términos detectada. Aceptando...")
        check_terminos.click()
        
        # Si después de marcar el check aparece otro botón de confirmar, lo clickeamos:
        # boton_confirmar = driver.find_element(By.XPATH, "//button[contains(., 'Confirmar')]")
        # boton_confirmar.click()

    except Exception:
        # Si no aparece en 3 segundos, asumimos que no salió y seguimos
        print("No se detectó validación de términos, continuando...")
    # ------------------------------------------------
    '''
    
    # 2. Seleccionar tipo de moneda (Nacional)
    # Esperamos a que el segundo select sea clickeable (esto indica que el primero ya procesó)
    dropdown2 = wait.until(EC.element_to_be_clickable((By.ID, "mat-select-1")))
    dropdown2.click()
    
    # IMPORTANTE: El ID de la opción puede ser mat-option-0 nuevamente si el DOM se refresca
    opcion_nacional = wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-option//span[contains(text(), 'Nacional')]")))
    opcion_nacional.click()

    # 3. Seleccionar el Instrumento Origen (Tu cuenta específica)
    dropdown3 = wait.until(EC.element_to_be_clickable((By.ID, "mat-select-2")))
    dropdown3.click()
    
    # Usamos el ID que tenías (mat-option-5), pero con wait para asegurar que cargó la lista de cuentas
    opcion_ahorro = wait.until(EC.element_to_be_clickable((By.ID, "mat-option-5")))
    opcion_ahorro.click()

    # 4. Seleccionar período (Últimos 3 meses)
    # A veces el radio button está tapado por su propio label, usamos el ID del contenedor o clic forzado
    ult_3meses = wait.until(EC.element_to_be_clickable((By.ID, "mat-radio-5")))
    ult_3meses.click()

    # 5. Botón Procesar
    # Esperamos a que el botón no solo esté, sino que esté habilitado
    boton_procesar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Procesar')]")))
    boton_procesar.click()

    driver.implicitly_wait(5)

    # --- FIN DE LA SECCIÓN CORREGIDA ---
    #wait_salir = WebDriverWait(driver,5)
    boton_salir = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'salir')]")))
    boton_salir.click()

    #"ng-star-inserted" [ class=mat-select-0, [div clas=mat-form-field-infix, [ id=mat-radio-5-input


scraper()