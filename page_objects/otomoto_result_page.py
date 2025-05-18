from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

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

    def get_offer_data(self, oferta):
        try:
            tytul_element = oferta.find_element(*self.tytul_locator)
            tytul = tytul_element.text.strip()
            cena = oferta.find_element(*self.cena_locator).text.strip()
            link = tytul_element.get_attribute("href")
            return {"Tytuł": tytul, "Cena": cena, "Link": link}
        except Exception as e:
            print(f"Błąd podczas pobierania danych oferty: {e}")
            return None

    def get_n_offers(self, n=10):
        oferty = WebDriverWait(self.driver, 10).until(
            ec.presence_of_all_elements_located(self.offer_item_locator)
        )
        dane_ofert = []
        liczba_ofert_do_pobrania = min(n, len(oferty))
        for i in range(liczba_ofert_do_pobrania):
            dane = self.get_offer_data(oferty[i])
            if dane:
                dane_ofert.append(dane)
        return dane_ofert