from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
from page_objects.otomoto_main_page import OtomotoMainPage
from page_objects.otomoto_result_page import OtomotoResultsPage
import psycopg2

# Dane dostępowe z Neon Console
DB_HOST = 'ep-restless-shadow-a937m71a-pooler.gwc.azure.neon.tech'
DB_PORT = '5432'
DB_USER = 'neondb_owner'
DB_PASSWORD = 'npg_A2Snkh5ZTLvG'
DB_NAME = 'neondb'


def polacz():
    conn = None  # Inicjalizuj conn na None
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"Połączono z PostgreSQL w Neon Tech, wersja: {db_version}")
        cursor.close()
        return conn  # Zwróć obiekt połączenia
    except psycopg2.Error as e:
        print(f"Błąd połączenia z bazą danych Neon Tech: {e}")
        if conn:
            conn.close()
        return None

def stworz_tabele(conn):
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS oferty (
                    id SERIAL PRIMARY KEY,
                    tytul TEXT,
                    link TEXT UNIQUE,
                    zdjecie TEXT,
                    cena TEXT,
                    telefon TEXT
                )
            ''')
            conn.commit()
            print("Tabela 'oferty' została utworzona (lub już istnieje).")
        except psycopg2.Error as e:
            print(f"Błąd podczas tworzenia tabeli 'oferty': {e}")
            conn.rollback()  # Wycofaj transakcję w przypadku błędu
        cursor.close()
    else:
        print("Nie można utworzyć tabeli, brak połączenia z bazą danych.")

if __name__ == "__main__":
    conn = polacz()
    if conn:
        stworz_tabele(conn)
        conn.close()  # Zamknij połączenie po wykonaniu operacji

prefs = {"download.default_directory" : "/Users/maciej/PycharmProjects/behaveProject"}

@Given('launch chrome browser')
def step_impl(context):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option("prefs", prefs)
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
def step_impl(context):
    context.results_page.select_nieuszkodzony()
    context.dane_ofert = context.results_page.get_n_offers(n=10)

@Then('zapisuje dane')
def step_impl(context):
    plik_csv = "oferty_bmw_m3.csv"
    if context.dane_ofert:
        klucze = context.dane_ofert[0].keys()
        with open(plik_csv, 'w', newline='', encoding='utf-8') as plik_csv:
            dict_writer = csv.DictWriter(plik_csv, fieldnames=klucze)
            dict_writer.writeheader()
            dict_writer.writerows(context.dane_ofert)
        print(f"Dane zostały zapisane do pliku {plik_csv}")
    else:
        print("Nie pobrano żadnych danych, plik CSV nie został utworzony.")

@Then('close browser')
def step_impl(context):
   context.driver.quit()