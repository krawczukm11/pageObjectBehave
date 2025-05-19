from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("OtomotoScraper")

class OfferDataExtractionError(Exception):
    """Custom exception for data extraction errors with detailed information"""
    def __init__(self, message, offer_index=None, error_type=None, original_exception=None):
        self.message = message
        self.offer_index = offer_index
        self.error_type = error_type
        self.original_exception = original_exception
        super().__init__(self.message)

class OtomotoResultsPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.offer_item_locator = (By.CSS_SELECTOR, 'article.offer-item')
        self.tytul_locator = (By.CSS_SELECTOR, 'h2 a')
        self.cena_locator = (By.CSS_SELECTOR, '.offer-price__number')
        self.link_locator = (By.TAG_NAME, 'a')
        self.stan_auta_button_locator = (By.XPATH, "//input[@placeholder='Stan uszkodzeń']")
        self.nieuszkodzony_option_locator = (By.XPATH, "//span[contains(text(),'Nieuszkodzony')]")

    def select_nieuszkodzony(self):
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.stan_auta_button_locator)
        ).click()
        WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located(self.nieuszkodzony_option_locator)
        ).click()

    def get_offer_data(self, oferta, index=None):
        try:
            tytul_element = oferta.find_element(*self.tytul_locator)
            tytul = tytul_element.text.strip()
            cena = oferta.find_element(*self.cena_locator).text.strip()
            link = tytul_element.get_attribute("href")
            return {"Tytuł": tytul, "Cena": cena, "Link": link}
        except NoSuchElementException as e:
            error_msg = f"Element not found: {e.msg}"
            logger.error(error_msg)
            raise OfferDataExtractionError(
                message=error_msg,
                offer_index=index,
                error_type="ElementNotFound",
                original_exception=e
            )
        except StaleElementReferenceException as e:
            error_msg = "Element reference is stale (page may have changed)"
            logger.error(error_msg)
            raise OfferDataExtractionError(
                message=error_msg,
                offer_index=index,
                error_type="StaleElement",
                original_exception=e
            )
        except Exception as e:
            error_msg = f"Unexpected error extracting offer data: {str(e)}"
            logger.error(error_msg)
            raise OfferDataExtractionError(
                message=error_msg,
                offer_index=index,
                error_type="Unknown",
                original_exception=e
            )

    def get_n_offers(self, n=10):
        oferty = WebDriverWait(self.driver, 10).until(
            ec.presence_of_all_elements_located(self.offer_item_locator)
        )
        dane_ofert = []
        liczba_ofert_do_pobrania = min(n, len(oferty))
        failed_offers = []

        logger.info(f"Attempting to extract data from {liczba_ofert_do_pobrania} offers")

        for i in range(liczba_ofert_do_pobrania):
            try:
                dane = self.get_offer_data(oferty[i], index=i)
                dane_ofert.append(dane)
                logger.info(f"Successfully extracted data from offer {i+1}")
            except OfferDataExtractionError as e:
                failed_offers.append({
                    "index": i,
                    "error_type": e.error_type,
                    "message": e.message
                })
                logger.warning(f"Failed to extract data from offer {i+1}: {e.message}")
                # Continue with next offer instead of silently failing

        if failed_offers:
            logger.warning(f"Failed to extract data from {len(failed_offers)} out of {liczba_ofert_do_pobrania} offers")

        return dane_ofert