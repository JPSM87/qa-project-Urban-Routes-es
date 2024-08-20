import UrbanRoutesP
import data
from selenium import webdriver
from selenium.webdriver.common.by import By
import locators



class TestUrbanRoutes:

    driver = None


    @classmethod

    def setup_class(cls):

        from selenium.webdriver.chrome.options import Options

        options = Options()

        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        cls.driver = webdriver.Chrome(options=options)


    def test_set_route(cls):

        cls.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesP.UrbanRoutesPage(cls.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        #Confirmación de la acción
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to


    def test_select_comfort_tariff(cls):

        order_cab_click = UrbanRoutesP.UrbanRoutesPage(cls.driver)
        order_cab_click.select_comfort_tariff()
        # Aserción para verificar si se ha seleccionado la tarifa
        #Al intentar ocupar el selector como CSS y como CLASS_NAME 'tcard active', no lo me lo toma, así que recurrí a este método utilizando la presencia de la opción de mantas y pañuelos en el workflow.
        selected_tariff = cls.driver.find_element(By.CSS_SELECTOR,'.r-sw-label')
        assert "Manta y pañuelos" in selected_tariff.text, "Expected 'Comfort' tariff to be selected"


    def test_add_phone_number(cls):

        add_phone_number = UrbanRoutesP.UrbanRoutesPage(cls.driver)
        phone_number = data.phone_number
        add_phone_number.set_phone_number(phone_number)

    def test_confirm_phone_number(cls):

        comfirmation_code = UrbanRoutesP.UrbanRoutesPage(cls.driver)
        comfirmation_code.confirm_phone_number()
        phone_number = data.phone_number
        phone_number_locator = locators.UrbanRoutesLocators.phone_number_button
        # Verificación final del texto dentro del elemento
        entered_phone = cls.driver.find_element(*phone_number_locator).text
        assert phone_number in entered_phone, f"Expected phone number to be {phone_number}, but got {entered_phone}"

    def test_pay_method(cls):

        add_credit_card = UrbanRoutesP.UrbanRoutesPage(cls.driver)
        card_number = data.card_number
        card_code = data.card_code
        add_credit_card.add_credit_card(card_number, card_code)
        # Aserción para verificar si se ha añadido la tarjeta
        added_card = locators.UrbanRoutesLocators.pay_method_button
        card_message = cls.driver.find_element(*added_card).text
        assert "Tarjeta" in card_message, "Expected card to be added successfully"


    def test_add_driver_comment(cls):

        add_comment = UrbanRoutesP.UrbanRoutesPage(cls.driver)
        message_for_driver = data.message_for_driver
        add_comment.set_message_for_driver(message_for_driver)
        #Aserción para mensaje al conductor
        entered_message = cls.driver.find_element(By.ID, 'comment').get_attribute('value')
        assert entered_message == message_for_driver, f"Expected message for driver to be {message_for_driver}"


    def test_add_tissue_and_blanket(cls):

        add_tissue_and_blanket = UrbanRoutesP.UrbanRoutesPage(cls.driver)
        add_tissue_and_blanket.request_blanket_and_tissues()
        #Aserción para el botón de manta y pañuelos
        blank_and_tiss = add_tissue_and_blanket.switch_blanket_and_tissues()
        assert blank_and_tiss == True, f"Expected switch to be ON"


    def test_add_ice_cream(cls):

        add_ice_cream = UrbanRoutesP.UrbanRoutesPage(cls.driver)
        add_ice_cream.request_ice_cream()
        #Aserción para el contador de helados
        ic_counter_locator= locators.UrbanRoutesLocators.ice_cream_counter
        ic_counter_element = cls.driver.find_element(*ic_counter_locator)
        ic_counter_value = int(ic_counter_element.text)
        assert ic_counter_value == 2, "Expected number of ice cream"


    def test_order_taxi(cls):

        order_taxi = UrbanRoutesP.UrbanRoutesPage(cls.driver)
        order_taxi.submit_final_order()
        # Aserción para verificar si el pedido de taxi se ha enviado
        confirmation_message = cls.driver.find_element(By.CLASS_NAME,'order-header-title').text
        assert "Buscar automóvil" in confirmation_message, "Expected taxi order to be placed successfully"


    @classmethod

    def teardown_class(cls):

        cls.driver.quit()
