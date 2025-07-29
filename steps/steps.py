import os
import csv
import time
import psycopg2
from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from page_objects.otomoto_main_page import OtomotoMainPage
from page_objects.otomoto_result_page import OtomotoResultsPage
from configuration import polacz, stworz_tabele
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
service = Service(ChromeDriverManager().install())


@Given('baza polaczona')
def step_impl(context):
    conn = polacz()
    if conn:
        stworz_tabele(conn)
        conn.close()
if __name__ == "__main__":
    step_impl

@Given('launch chrome browser')
def step_impl(context):
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument("--incognito")
    context.driver=webdriver.Chrome(options=chrome_options)
    context.driver.maximize_window()
    context.main_page = OtomotoMainPage(context.driver)
    context.results_page = OtomotoResultsPage(context.driver)

@When('open otomoto')
def step_impl(context):
    context.driver.get("https://www.otomoto.pl")

@When('ochrona') ##zamyka pop-up
def step_impl(context):
    context.main_page.accept_cookies()

@When("wyszukuje marke i model")
def step_impl(context):
    context.main_page.open_marka_list()
    context.main_page.enter_marka("BMW")
    context.main_page.select_marka()
    context.main_page.open_model_list()
    context.main_page.enter_model("M3")
    context.main_page.select_model()
    context.main_page.click_pokaz_ogloszenia()

@When("listuje auta")
def step_list_and_save_cars(context):
    context.results_page.select_bezwypadkowy()
    context.driver.execute_script("window.scrollBy(0, 300);")
    context.results_page.select_najtansze()
    time.sleep(30)

@When("zapisuje linki")
def scrap_data(context):
    with webdriver.Chrome(service=service) as driver:
        time.sleep(30)
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

@Then('close browser')
def step_close_browser(context):
    if hasattr(context, 'driver'):
        context.driver.quit()



