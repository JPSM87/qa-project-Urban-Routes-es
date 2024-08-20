from selenium.webdriver.common.by import By


class UrbanRoutesLocators:
    """Intenté cambiar la mayoría de los Xpath, pero habían algunos que no me funcionaban con otros tipos de selectores"""
    # Localizadores de elementos en la página

    from_field = (By.ID, 'from')  # Campo para ingresar la dirección "Desde"

    to_field = (By.ID, 'to')  # Campo para ingresar la dirección "Hasta"

    order_cab = (By.CSS_SELECTOR,'.button.round ')  # Botón para pedir taxi

    comfort_tariff = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')  # Botón de la tarifa comfort

    comfort_tariff_check = (By.CLASS_NAME,'tcard-title')

    phone_number_button = (By.CLASS_NAME, 'np-text')  # Botón para abrir la ventana de número de teléfono

    phone_number_field = (By.ID, 'phone')  # Campo de entrada del número de teléfono

    phone_button_next = (By.CSS_SELECTOR, '.button.full')  # Botón "Siguiente" después de ingresar el número de teléfono

    phone_number_confirmation_code = (By.CSS_SELECTOR,'input[placeholder="xxxx"]')  # Campo para el código de confirmación

    phone_code_confirmation_button = (By.CSS_SELECTOR,'.section.active>form>.buttons>:nth-child(1)')  # Botón para confirmar el código de teléfono

    pay_method_button = (By.CSS_SELECTOR,'.pp-value-text ')  # Botón para seleccionar el método de pago ACTUALIZADO

    add_new_card = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]')  # Botón para añadir una nueva tarjeta

    card_number = (By.CSS_SELECTOR, '.card-wrapper .card-input')  # Campo para ingresar el número de la tarjeta

    code_number = (By.CSS_SELECTOR, "input[placeholder='12']")  # Campo para el código de la tarjeta

    outer_card_click = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form')  # Área para hacer clic fuera de los campos de la tarjeta

    add_card = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')  # Botón para añadir la tarjeta

    close_pay_method = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')  # Botón para cerrar la ventana de método de pago

    driver_comment = (By.XPATH,'//*[@id="comment"]')  # Campo para añadir un comentario al conductor

    blanket_and_tissue = (By.CLASS_NAME, 'r-sw')  # Botón para seleccionar manta y pañuelos

    blanket_and_tissue_checkbox = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/input") #Casilla activa

    ice_cream_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')  # Botón para añadir helado

    ice_cream_counter = (By.XPATH,'//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]') #Contador de helados

    final_order_cab = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')  # Botón final para pedir el taxi

    searching_driver = (By.CLASS_NAME,'order-header-title')
