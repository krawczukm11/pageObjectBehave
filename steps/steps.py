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

# Konfiguracja bazy danych - używaj zmiennych środowiskowych w produkcji
DB_HOST = ('DB_HOST', 'ep-restless-shadow-a937m71a-pooler.gwc.azure.neon.tech')
DB_PORT = ('DB_PORT', '5432')
DB_USER = ('DB_USER', 'neondb_owner')
DB_PASSWORD = ('DB_PASSWORD', 'npg_A2Snkh5ZTLvG')  # UWAGA: Ustaw w zmiennych środowiskowych!
DB_NAME = ('DB_NAME', 'neondb')

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

@When("listuje i zapisuje 10 aut")
def step_list_and_save_cars(context):
    context.results_page.select_nieuszkodzony()
    context.results_page.link()

@Then('close browser')
def step_close_browser(context):
    """Zamyka przeglądarkę"""
    if hasattr(context, 'driver'):
        context.driver.quit()
        print("🔚 Przeglądarka została zamknięta")



