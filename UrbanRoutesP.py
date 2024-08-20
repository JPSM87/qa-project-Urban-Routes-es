from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import helpers
from locators import UrbanRoutesLocators

class UrbanRoutesPage:

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

        self.wait_for_element(*UrbanRoutesLocators.from_field)

        self.driver.find_element(*UrbanRoutesLocators.from_field).send_keys(from_address)

        self.wait_for_element(*UrbanRoutesLocators.to_field)

        self.driver.find_element(*UrbanRoutesLocators.to_field).send_keys(to_address)


    def get_from(self):

        """Obtiene la dirección ingresada en el campo 'Desde'."""

        return self.driver.find_element(*UrbanRoutesLocators.from_field).get_property('value')


    def get_to(self):

        """Obtiene la dirección ingresada en el campo 'Hasta'."""

        return self.driver.find_element(*UrbanRoutesLocators.to_field).get_property('value')


    def select_comfort_tariff(self):

        """Selecciona la tarifa Comfort después de hacer clic en el botón 'Pedir un taxi'."""

        self.wait_for_element(*UrbanRoutesLocators.order_cab)

        self.driver.find_element(*UrbanRoutesLocators.order_cab).click()

        self.wait_for_element(*UrbanRoutesLocators.comfort_tariff)

        self.driver.find_element(*UrbanRoutesLocators.comfort_tariff).click()


    def set_phone_number(self, phone_number):

        """Ingresa el número de teléfono y continúa con la verificación."""

        self.wait_for_element(*UrbanRoutesLocators.phone_number_button)

        self.driver.find_element(*UrbanRoutesLocators.phone_number_button).click()

        self.wait_for_element(*UrbanRoutesLocators.phone_number_field)

        self.driver.find_element(*UrbanRoutesLocators.phone_number_field).send_keys(phone_number)

        self.driver.find_element(*UrbanRoutesLocators.phone_button_next).click()


    def confirm_phone_number(self):

        """Confirma el código recibido después de ingresar el número de teléfono."""

        code = helpers.retrieve_phone_code(self.driver)  # Obtén el código de confirmación

        self.wait_for_element(*UrbanRoutesLocators.phone_number_confirmation_code)

        self.driver.find_element(*UrbanRoutesLocators.phone_number_confirmation_code).send_keys(code)

        self.driver.find_element(*UrbanRoutesLocators.phone_code_confirmation_button).click()



    def add_credit_card(self, card_number, card_code):

        """Añade una nueva tarjeta de crédito."""

        self.wait_for_element(*UrbanRoutesLocators.pay_method_button)

        self.driver.find_element(*UrbanRoutesLocators.pay_method_button).click()

        self.wait_for_element(*UrbanRoutesLocators.add_new_card)

        self.driver.find_element(*UrbanRoutesLocators.add_new_card).click()

        self.wait_for_element(*UrbanRoutesLocators.card_number)

        self.driver.find_element(*UrbanRoutesLocators.card_number).send_keys(card_number)

        self.wait_for_element(*UrbanRoutesLocators.code_number)

        self.driver.find_element(*UrbanRoutesLocators.code_number).send_keys(card_code)

        self.driver.find_element(*UrbanRoutesLocators.outer_card_click).click()

        self.driver.find_element(*UrbanRoutesLocators.add_card).click()

        self.driver.find_element(*UrbanRoutesLocators.close_pay_method).click()


    def set_message_for_driver(self, message):

        """Ingresa un mensaje para el conductor."""

        self.wait_for_element(*UrbanRoutesLocators.driver_comment)

        self.driver.find_element(*UrbanRoutesLocators.driver_comment).send_keys(message)


    def request_blanket_and_tissues(self):
        """Selecciona las opciones de manta y pañuelos."""
        self.wait_for_element(*UrbanRoutesLocators.blanket_and_tissue)
        self.driver.find_element(*UrbanRoutesLocators.blanket_and_tissue).click()


    def switch_blanket_and_tissues(self):

        self.wait_for_element(*UrbanRoutesLocators.blanket_and_tissue)  # Asegúrate de que `wait_for_element` esté definido en `UrbanRoutesPage`
        switch = self.driver.find_element(*UrbanRoutesLocators.blanket_and_tissue_checkbox)
        return switch.is_selected()


    def request_ice_cream(self):

        """Selecciona la opción de helado."""
        self.wait_for_element(*UrbanRoutesLocators.ice_cream_button)
        self.driver.find_element(*UrbanRoutesLocators.ice_cream_button).click()
        self.driver.find_element(*UrbanRoutesLocators.ice_cream_button).click()


    def submit_final_order(self):

        """Envía la solicitud final de taxi."""

        self.wait_for_element(*UrbanRoutesLocators.final_order_cab)

        self.driver.find_element(*UrbanRoutesLocators.final_order_cab).click()
