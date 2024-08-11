import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# no modificar
def retrieve_phone_code(driver) -> str:
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
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    comfort_tariff = (By.CSS_SELECTOR, ".tariff-comfort")
    phone_field = (By.ID, 'phone')
    card_field = (By.ID, 'card')
    cvv_field = (By.ID, 'code')
    link_button = (By.ID, 'link-button')
    message_field = (By.ID, 'message')
    blanket_checkbox = (By.ID, 'blanket')
    tissues_checkbox = (By.ID, 'tissues')
    ice_cream_checkbox = (By.ID, 'ice-cream')
    driver_info_modal = (By.ID, 'driver-info-modal')

    def __init__(self, driver):
        self.driver = driver

    def set_route(self, from_address, to_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def select_comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff).click()

    def set_phone_number(self, phone_number):
        self.driver.find_element(*self.phone_field).send_keys(phone_number)

    def add_credit_card(self, card_number, card_code):
        self.driver.find_element(*self.card_field).send_keys(card_number)
        self.driver.find_element(*self.cvv_field).send_keys(card_code)
        self.driver.find_element(*self.cvv_field).send_keys(Keys.TAB)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.link_button)
        ).click()

    def set_message_for_driver(self, message):
        self.driver.find_element(*self.message_field).send_keys(message)

    def request_blanket_and_tissues(self):
        self.driver.find_element(*self.blanket_checkbox).click()
        self.driver.find_element(*self.tissues_checkbox).click()

    def request_two_ice_creams(self):
        ice_cream_field = self.driver.find_element(*self.ice_cream_checkbox)
        ice_cream_field.click()
        ice_cream_field.click()

    def wait_for_driver_info(self):
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.driver_info_modal)
        )

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_tariff(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_comfort_tariff()
        # Aquí podrías agregar una verificación adicional si hay algún indicador visual de selección.

    def test_set_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_phone_number(data.phone_number)
        # Verifica si el número de teléfono se ingresó correctamente, si es necesario.

    def test_add_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_credit_card(data.card_number, data.card_code)
        # Aquí podrías verificar si el botón se activó correctamente o si la tarjeta se agregó correctamente.

    def test_set_message_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_message_for_driver(data.message_for_driver)
        # Verifica si el mensaje se ingresó correctamente, si es necesario.

    def test_request_blanket_and_tissues(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.request_blanket_and_tissues()
        # Verifica si los elementos fueron seleccionados correctamente.

    def test_request_two_ice_creams(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.request_two_ice_creams()
        # Verifica si se seleccionaron dos helados correctamente.

    def test_wait_for_driver_info(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_driver_info()
        # Aquí podrías verificar si la información del conductor se muestra correctamente.

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
