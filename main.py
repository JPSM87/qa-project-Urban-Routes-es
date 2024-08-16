from selenium.common import TimeoutException
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string."""
    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code

class UrbanRoutesPage:
    # Localizadores de elementos en la página
    from_field = (By.ID, 'from')  # Campo para ingresar la dirección "Desde"
    to_field = (By.ID, 'to')  # Campo para ingresar la dirección "Hasta"
    order_cab = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')  # Botón para pedir taxi
    comfort_tariff = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')  # Botón de la tarifa comfort
    phone_number_button = (By.CLASS_NAME, 'np-text')  # Botón para abrir la ventana de número de teléfono
    phone_number_field = (By.ID, 'phone')  # Campo de entrada del número de teléfono
    phone_button_next = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')  # Botón "Siguiente" después de ingresar el número de teléfono
    phone_number_confirmation_code = (By.XPATH, '//*[@id="code"]')  # Campo para el código de confirmación
    phone_code_confirmation_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')  # Botón para confirmar el código de teléfono
    pay_method_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]')  # Botón para seleccionar el método de pago
    add_new_card = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]')  # Botón para añadir una nueva tarjeta
    card_number = (By.CSS_SELECTOR, '.card-wrapper .card-input')  # Campo para ingresar el número de la tarjeta
    code_number = (By.CSS_SELECTOR, "input[placeholder='12']")  # Campo para el código de la tarjeta
    outer_card_click = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form')  # Área para hacer clic fuera de los campos de la tarjeta
    add_card = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')  # Botón para añadir la tarjeta
    close_pay_method = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')  # Botón para cerrar la ventana de método de pago
    driver_comment = (By.XPATH,'//*[@id="comment"]')  # Campo para añadir un comentario al conductor
    blanket_and_tissue = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')  # Botón para seleccionar manta y pañuelos
    ice_cream_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')  # Botón para añadir helado
    final_order_cab = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')  # Botón final para pedir el taxi

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by, value, timeout=20):
        """Método auxiliar para esperar a que un elemento esté presente y visible."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
        except TimeoutException:
            print(f"Timeout: Elemento con selector ({by}, {value}) no encontrado.")
            self.driver.get_screenshot_as_file("timeout_error.png")  # Captura de pantalla para depuración

    def set_route(self, from_address, to_address):
        """Establece la ruta ingresando las direcciones 'Desde' y 'Hasta'."""
        self.wait_for_element(*self.from_field)
        self.driver.find_element(*self.from_field).send_keys(from_address)
        self.wait_for_element(*self.to_field)
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        """Obtiene la dirección ingresada en el campo 'Desde'."""
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        """Obtiene la dirección ingresada en el campo 'Hasta'."""
        return self.driver.find_element(*self.to_field).get_property('value')

    def select_comfort_tariff(self):
        """Selecciona la tarifa Comfort después de hacer clic en el botón 'Pedir un taxi'."""
        self.wait_for_element(*self.order_cab)
        self.driver.find_element(*self.order_cab).click()
        self.wait_for_element(*self.comfort_tariff)
        self.driver.find_element(*self.comfort_tariff).click()

    def set_phone_number(self, phone_number):
        """Ingresa el número de teléfono y continúa con la verificación."""
        self.wait_for_element(*self.phone_number_button)
        self.driver.find_element(*self.phone_number_button).click()
        self.wait_for_element(*self.phone_number_field)
        self.driver.find_element(*self.phone_number_field).send_keys(phone_number)
        self.driver.find_element(*self.phone_button_next).click()

    def confirm_phone_number(self):
        """Confirma el código recibido después de ingresar el número de teléfono."""
        code = retrieve_phone_code(self.driver)  # Obtén el código de confirmación
        self.wait_for_element(*self.phone_number_confirmation_code)
        self.driver.find_element(*self.phone_number_confirmation_code).send_keys(code)
        self.driver.find_element(*self.phone_code_confirmation_button).click() #Corre

    def add_credit_card(self, card_number, card_code):
        """Añade una nueva tarjeta de crédito."""
        self.wait_for_element(*self.pay_method_button)
        self.driver.find_element(*self.pay_method_button).click()
        self.wait_for_element(*self.add_new_card)
        self.driver.find_element(*self.add_new_card).click()
        self.wait_for_element(*self.card_number)
        self.driver.find_element(*self.card_number).send_keys(card_number)
        self.wait_for_element(*self.code_number)
        self.driver.find_element(*self.code_number).send_keys(card_code)
        self.driver.find_element(*self.outer_card_click).click()
        self.driver.find_element(*self.add_card).click()
        self.driver.find_element(*self.close_pay_method).click()

    def set_message_for_driver(self, message):
        """Ingresa un mensaje para el conductor."""
        self.wait_for_element(*self.driver_comment)
        self.driver.find_element(*self.driver_comment).send_keys(message)

    def request_blanket_and_tissues(self):
        """Selecciona las opciones de manta y pañuelos."""
        self.wait_for_element(*self.blanket_and_tissue)
        self.driver.find_element(*self.blanket_and_tissue).click()

    def request_ice_cream(self):
        """Selecciona la opción de helado."""
        self.wait_for_element(*self.ice_cream_button)
        self.driver.find_element(*self.ice_cream_button).click()

    def submit_final_order(self):
        """Envía la solicitud final de taxi."""
        self.wait_for_element(*self.final_order_cab)
        self.driver.find_element(*self.final_order_cab).click()
class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_tariff(self):
        order_cab_click = UrbanRoutesPage(self.driver)
        order_cab_click.select_comfort_tariff()

    def test_add_phone_number(self):
        add_phone_number = UrbanRoutesPage(self.driver)
        phone_number = data.phone_number  # Asume que tiessssaaaaaaero de teléfono almacenado en el archivo `data.py`
        add_phone_number.set_phone_number(phone_number)

    def test_comfirm_phone_number(self):
        comfirmation_code = UrbanRoutesPage(self.driver)
        comfirmation_code.confirm_phone_number()

    def test_pay_method(self):
        # Crear una instancia de UrbanRoutesPage
        add_credit_card = UrbanRoutesPage(self.driver)
        card_number = data.card_number  # Debes tener estos valores en tu archivo `data.py`
        card_code = data.card_code  # Debes tener estos valores en tu archivo `data.py`
        add_credit_card.add_credit_card(card_number, card_code)

    def test_add_driver_comment(self):
        add_comment = UrbanRoutesPage(self.driver)
        message_for_driver = data.message_for_driver  # Obtén el mensaje desde data.py
        add_comment.set_message_for_driver(message_for_driver)

    def test_add_tissue_and_blanket(self):
        add_tissue_and_blanket = UrbanRoutesPage(self.driver)
        add_tissue_and_blanket.request_blanket_and_tissues()

    def test_add_ice_cream(self):
        add_ice_cream = UrbanRoutesPage(self.driver)
        add_ice_cream.request_ice_cream()

    def test_order_taxi(self):
        order_taxi = UrbanRoutesPage(self.driver)
        order_taxi.submit_final_order()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
