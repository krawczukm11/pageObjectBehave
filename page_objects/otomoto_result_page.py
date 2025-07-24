from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from typing import List
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
service = Service(ChromeDriverManager().install())

with webdriver.Chrome(service=service) as driver:
    class OtomotoResultsPage:
        def __init__(self, driver: WebDriver):
            self.driver = driver
            self.stan_auta_button_locator = (By.XPATH, "(//div[contains(@role,'group')])[12]")
            self.nieuszkodzony_option_locator = (By.CSS_SELECTOR, 'input[value="Nieuszkodzony"]') ###ISSUE IS HERE!!!1
            self.links_locator = (By.XPATH, './/div[@class="etydmma0 ooa-16c293i"]/a')

        def click_nieuszkodzony_filter(self):
            button = self.driver.find_element(*self.stan_auta_button_locator)
            button.click()
            option = self.driver.find_element(*self.nieuszkodzony_option_locator)
            option.click()

        def select_nieuszkodzony(self):
            WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(self.stan_auta_button_locator)
            ).click()
            WebDriverWait(self.driver, 10).until(
                ec.visibility_of_element_located(self.nieuszkodzony_option_locator)
            ).click()
            WebDriverWait(self.driver, 30)

        def link(self):
            links = driver.find_elements(By.XPATH, '//section[@class="ooa-o5rf8l e14w1bje0"]//a[@href]')
            hrefs = []

            for link in links:
                hrefs.append(link.get_attribute('href'))

            nazwy = driver.find_elements(By.XPATH, '//div[@class="ooa-j7qwjs e1owtbrj0"]//h2')
            nazw = []

            for nazwa in nazwy:
                nazw.append(nazwa.text)

            obrazki = driver.find_elements(By.XPATH, '//article[@class="e1or3qgp1 ooa-yjw0j9 e1or3qgp0"]//img')
            zdjecia = []

            for obrazek in obrazki:
                src = obrazek.get_attribute("src")
                zdjecia.append(src)

            ceny = driver.find_elements(By.XPATH, '//section[@class="ooa-k008qs e1rwha5u1"]//h4//span')
            cena = []

            for cenka in ceny:
                cena.append(cenka.text)


            print(hrefs)
            print(nazw)
            print(zdjecia)
            print(cena)