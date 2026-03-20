'''
# 1. Hacer clic para abrir el desplegable
    dropdown = driver.find_element(By.ID, "mat-select-0")
    dropdown.click()

    # 2. Seleccionar la opción "Cuenta" (que suele ser la primera opción)
    opcion_cuenta = driver.find_element(By.ID, "mat-option-0")
    opcion_cuenta.click()

    #driver.implicitly_wait(10)
    
    dropdown2 = driver.find_element(By.ID, "mat-select-1")
    dropdown2.click()
    
    dropdown2 = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.ID, "mat-select-1")))
    dropdown2.click()
    opcion_nacional = driver.find_element(By.ID, "mat-option-0")
    opcion_nacional.click()

    #driver.implicitly_wait(10)
    
    dropdown3 = driver.find_element(By.ID, "mat-select-2")
    dropdown3.click()
    
    dropdown3 = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.ID, "mat-select-2")))
    dropdown3.click()
    opcion_ahorro = driver.find_element(By.ID, "mat-option-5")
    opcion_ahorro.click()

    #driver.implicitly_wait(10)

    ult_3meses = driver.find_element(By.ID, "mat-radio-5-input")
    ult_3meses.click()

    #driver.implicitly_wait(10)

    boton_procesar = driver.find_element(By.XPATH, "//button[contains(., 'Procesar')]")
    boton_procesar.click()
'''