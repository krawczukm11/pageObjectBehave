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
            self.wiecej_filtrow_locator = (By.XPATH, "(//div[@class='ooa-1md513v e1h8zeny4'])[1]")
            self.status_pojazdu_locator = (By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/section[1]/article[2]/div[2]/div[1]/div[1]/button[1]")
            self.bezwypadkowy_locator = (By.XPATH, "(//input[@id='Bezwypadkowy'])[1]")
            self.pokaz_wyniki_locator = (By.XPATH, "//button")
            self.links_locator = (By.XPATH, './/div[@class="etydmma0 ooa-16c293i"]/a')

        def select_bezwypadkowy(self):
            WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(self.wiecej_filtrow_locator)
            ).click()
            WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(self.status_pojazdu_locator)
            ).click()
            WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(self.bezwypadkowy_locator)
            ).click()
            WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(self.pokaz_wyniki_locator)
            ).click()
            WebDriverWait(self.driver, 30)

        def scrap_data(self):
            links = driver.find_elements(By.XPATH, '//div[@class="ooa-r53y0q e1612gp011"]//a[@href]')
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