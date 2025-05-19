from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException,
    ElementClickInterceptedException
)
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class OtomotoMainPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
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
        try:
            self.logger.info("Accepting cookies")
            cookie_container = WebDriverWait(self.driver, 30).until(
                ec.visibility_of_element_located(self.ochrona_danych_locator)
            )
            accept_button = cookie_container.find_element(*self.accept_button_locator)
            accept_button.click()
            self.logger.info("Cookies accepted successfully")
        except TimeoutException:
            self.logger.error("Timeout waiting for cookie consent dialog to appear")
            raise
        except NoSuchElementException:
            self.logger.error(f"Accept button not found within cookie consent dialog")
            raise
        except (ElementNotInteractableException, ElementClickInterceptedException) as e:
            self.logger.error(f"Unable to click accept button: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while accepting cookies: {str(e)}")
            raise

    def open_marka_list(self):
        try:
            self.logger.info("Opening vehicle make dropdown")
            marka_button = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(self.marka_pojazdu_button_locator)
            )
            marka_button.click()
            self.logger.info("Vehicle make dropdown opened successfully")
        except TimeoutException:
            self.logger.error("Timeout waiting for vehicle make dropdown to be clickable")
            raise
        except (ElementNotInteractableException, ElementClickInterceptedException) as e:
            self.logger.error(f"Unable to click vehicle make dropdown: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while opening vehicle make dropdown: {str(e)}")
            raise

    def enter_marka(self, marka):
        try:
            self.logger.info(f"Entering vehicle make: {marka}")
            input_field = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(self.marka_pojazdu_input_locator)
            )
            input_field.send_keys(marka)
            self.logger.info(f"Vehicle make '{marka}' entered successfully")
        except TimeoutException:
            self.logger.error("Timeout waiting for vehicle make input to be clickable")
            raise
        except ElementNotInteractableException as e:
            self.logger.error(f"Unable to interact with vehicle make input: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while entering vehicle make: {str(e)}")
            raise

    def select_marka(self):
        try:
            self.logger.info("Selecting vehicle make option")
            options = WebDriverWait(self.driver, 10).until(
                ec.presence_of_all_elements_located(self.marka_bmw_option_locator)
            )

            if not options:
                raise NoSuchElementException("No vehicle make options found")

            options[0].click()
            self.logger.info("Vehicle make option selected successfully")
        except TimeoutException:
            self.logger.error("Timeout waiting for vehicle make options to appear")
            raise
        except IndexError:
            self.logger.error("Vehicle make options list is empty")
            raise
        except (ElementNotInteractableException, ElementClickInterceptedException) as e:
            self.logger.error(f"Unable to click on vehicle make option: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while selecting vehicle make: {str(e)}")
            raise

    def open_model_list(self):
        try:
            self.logger.info("Opening vehicle model dropdown")
            model_button = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(self.model_pojazdu_button_locator)
            )
            model_button.click()
            self.logger.info("Vehicle model dropdown opened successfully")
        except TimeoutException:
            self.logger.error("Timeout waiting for vehicle model dropdown to be clickable")
            raise
        except (ElementNotInteractableException, ElementClickInterceptedException) as e:
            self.logger.error(f"Unable to click vehicle model dropdown: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while opening vehicle model dropdown: {str(e)}")
            raise

    def enter_model(self, model):
        try:
            self.logger.info(f"Entering vehicle model: {model}")
            input_field = WebDriverWait(self.driver, 60).until(
                ec.element_to_be_clickable(self.model_pojazdu_input_locator)
            )
            input_field.send_keys(model)
            self.logger.info(f"Vehicle model '{model}' entered successfully")
        except TimeoutException:
            self.logger.error("Timeout waiting for vehicle model input to be clickable")
            raise
        except ElementNotInteractableException as e:
            self.logger.error(f"Unable to interact with vehicle model input: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while entering vehicle model: {str(e)}")
            raise

    def select_model(self):
        try:
            self.logger.info("Selecting vehicle model option")
            options = WebDriverWait(self.driver, 10).until(
                ec.presence_of_all_elements_located(self.model_m3_option_locator)
            )

            if not options:
                raise NoSuchElementException("No vehicle model options found")

            options[0].click()
            self.logger.info("Vehicle model option selected successfully")
        except TimeoutException:
            self.logger.error("Timeout waiting for vehicle model options to appear")
            raise
        except IndexError:
            self.logger.error("Vehicle model options list is empty")
            raise
        except (ElementNotInteractableException, ElementClickInterceptedException) as e:
            self.logger.error(f"Unable to click on vehicle model option: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while selecting vehicle model: {str(e)}")
            raise

    def click_pokaz_ogloszenia(self):
        try:
            self.logger.info("Clicking 'Show listings' button")
            show_button = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(self.pokaz_ogloszenia_button_locator)
            )
            show_button.click()

            # Wait for results page to load
            self.logger.info("Waiting for results page to load")
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, "//input[@placeholder='Stan uszkodzeń']"))
            )
            self.logger.info("Results page loaded successfully")
        except TimeoutException as e:
            if "pokaz_ogloszenia_button_locator" in str(e):
                self.logger.error("Timeout waiting for 'Show listings' button to be clickable")
            else:
                self.logger.error("Timeout waiting for results page to load")
            raise
        except (ElementNotInteractableException, ElementClickInterceptedException) as e:
            self.logger.error(f"Unable to click 'Show listings' button: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while showing listings: {str(e)}")
            raise