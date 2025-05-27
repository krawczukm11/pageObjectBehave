from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class OtomotoMainPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.marka_pojazdu_button_locator = (By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/main[1]/div[1]/article[1]/article[1]/fieldset[1]/form[1]/section[1]/div[1]")
        self.marka_pojazdu_input_locator = (By.CLASS_NAME, "ooa-4ehujk")
        self.marka_bmw_option_locator = (By.CLASS_NAME, "ooa-18p1sko")
        self.model_pojazdu_button_locator = (By.XPATH, "(//div[@class='ooa-1xfqg6o'])[2]")
        self.model_pojazdu_input_locator = (By.XPATH, "//div[@aria-expanded='true']//input[@type='text']")
        self.model_m3_option_locator = (By.CLASS_NAME, "ooa-1w8r0f0")
        self.pokaz_ogloszenia_button_locator = (By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/main[1]/div[1]/article[1]/article[1]/fieldset[1]/form[1]/section[2]/button[1]")
        self.ochrona_danych_locator = (By.ID, "onetrust-button-group-parent")
        self.accept_button_locator = (By.ID, "onetrust-accept-btn-handler")

    def accept_cookies(self):
        WebDriverWait(self.driver, 30).until(
            ec.visibility_of_element_located(self.ochrona_danych_locator)
        ).find_element(*self.accept_button_locator).click()

    def open_marka_list(self):
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.marka_pojazdu_button_locator)
        ).click()

    def enter_marka(self, marka):
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.marka_pojazdu_input_locator)
        ).send_keys(marka)

    def select_marka(self):
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_all_elements_located(self.marka_bmw_option_locator)
        )[0].click()

    def open_model_list(self):
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.model_pojazdu_button_locator)
        ).click()

    def enter_model(self, model):
        WebDriverWait(self.driver, 60).until(
            ec.element_to_be_clickable(self.model_pojazdu_input_locator)
        ).send_keys(model)

    def select_model(self):
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_all_elements_located(self.model_m3_option_locator)
        )[0].click()

    def click_pokaz_ogloszenia(self):
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.pokaz_ogloszenia_button_locator)
        ).click()
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//input[@placeholder='Stan uszkodzeń']"))
        )