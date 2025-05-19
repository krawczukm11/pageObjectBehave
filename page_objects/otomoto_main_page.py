from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class OtomotoMainPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.marka_pojazdu_button_locator = (By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/main[1]/div[1]/article[1]/article[1]/fieldset[1]/form[1]/section[1]/div[1]")
        self.marka_pojazdu_input_locator = (By.CLASS_NAME, "ooa-4ehujk")
        self.option_item_class_locator = (By.CLASS_NAME, "ooa-18p1sko")  # Generic option class
        self.model_pojazdu_button_locator = (By.XPATH, "(//div[@class='ooa-1xfqg6o'])[2]")
        self.model_pojazdu_input_locator = (By.XPATH, "//div[@aria-expanded='true']//input[@type='text']")
        self.model_option_class_locator = (By.CLASS_NAME, "ooa-1w8r0f0")  # Generic model option class
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

    def select_marka(self, index=0, text=None):
        """
        Select the brand (marka) from the dropdown options.

        Args:
            index: The index of the option to select (default 0 for first option)
            text: The text of the option to select (overrides index if provided)
        """
        options = WebDriverWait(self.driver, 10).until(
            ec.presence_of_all_elements_located(self.option_item_class_locator)
        )

        if text:
            # Try to find option by text
            for option in options:
                if text.lower() in option.text.lower():
                    option.click()
                    return
            raise ValueError(f"No option containing text '{text}' found")
        else:
            # Use index-based selection
            if index < len(options):
                options[index].click()
            else:
                raise IndexError(f"Index {index} out of range. Only {len(options)} options available.")

    def open_model_list(self):
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.model_pojazdu_button_locator)
        ).click()

    def enter_model(self, model):
        WebDriverWait(self.driver, 60).until(
            ec.element_to_be_clickable(self.model_pojazdu_input_locator)
        ).send_keys(model)

    def select_model(self, index=0, text=None):
        """
        Select the model from the dropdown options.

        Args:
            index: The index of the option to select (default 0 for first option)
            text: The text of the option to select (overrides index if provided)
        """
        options = WebDriverWait(self.driver, 10).until(
            ec.presence_of_all_elements_located(self.model_option_class_locator)
        )

        if text:
            # Try to find option by text
            for option in options:
                if text.lower() in option.text.lower():
                    option.click()
                    return
            raise ValueError(f"No option containing text '{text}' found")
        else:
            # Use index-based selection
            if index < len(options):
                options[index].click()
            else:
                raise IndexError(f"Index {index} out of range. Only {len(options)} options available.")

    def click_pokaz_ogloszenia(self):
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.pokaz_ogloszenia_button_locator)
        ).click()
        # Zamiast czekać na zmianę URL, czekaj na załadowanie elementu na stronie wyników
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//input[@placeholder='Stan uszkodzeń']"))
        )