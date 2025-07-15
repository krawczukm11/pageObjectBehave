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

# Stałe konfiguracyjne
MAX_OFFERS_LIMIT = 10
MAX_SCROLL_ATTEMPTS = 10
SCROLL_PAUSE_TIME = 2
OFFERS_BATCH_SIZE = 5

# Preferencje Chrome
CHROME_PREFS = {"download.default_directory": "/Users/maciej/PycharmProjects/behaveProject"}



def zapisz_oferty_do_bazy_batch(oferty):
    """
    Zapisuje wiele ofert do bazy danych w jednej transakcji (optymalne)
    Args:
        oferty: Lista słowników z danymi ofert
    Returns:
        int: Liczba pomyślnie zapisanych ofert
    """
    if not oferty:
        return 0

    conn = polacz()
    if not conn:
        return 0

    zapisane_oferty = 0
    cursor = conn.cursor()

    try:
        for oferta in oferty:
            # Pobierz dane z oferty - obsługa różnych formatów
            tytul = oferta.get('tytul') or oferta.get('title', '')
            link = oferta.get('link', '')
            cena = oferta.get('cena') or oferta.get('price', '')
            telefon = oferta.get('telefon') or oferta.get('phone', '')

            # Wstaw dane do bazy (UNIQUE constraint na link zapobiegnie duplikatom)
            cursor.execute('''
                INSERT INTO oferty (tytul, link, cena, telefon) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (link) DO NOTHING
                RETURNING id
            ''', (tytul, link, cena, telefon))

            # Sprawdź czy rekord został wstawiony
            if cursor.fetchone():
                zapisane_oferty += 1

        conn.commit()
        print(f"💾 Pomyślnie zapisano {zapisane_oferty}/{len(oferty)} ofert do bazy")

    except psycopg2.Error as e:
        print(f"❌ Błąd podczas zapisywania ofert do bazy: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

    return zapisane_oferty


def zapisz_do_csv(oferty, nazwa_pliku):
    """
    Zapisuje oferty do pliku CSV
    Args:
        oferty: Lista słowników z danymi ofert
        nazwa_pliku: Nazwa pliku CSV
    Returns:
        bool: True jeśli zapis się powiódł
    """
    if not oferty:
        print("❌ Brak danych do zapisania do CSV")
        return False

    try:
        klucze = oferty[0].keys()
        with open(nazwa_pliku, 'w', newline='', encoding='utf-8') as plik:
            dict_writer = csv.DictWriter(plik, fieldnames=klucze)
            dict_writer.writeheader()
            dict_writer.writerows(oferty)

        print(f"📄 Dane zostały zapisane do pliku {nazwa_pliku}")
        return True

    except Exception as e:
        print(f"❌ Błąd podczas zapisywania do CSV: {e}")
        return False

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
    """
    Pobiera 10 ofert i zapisuje do CSV oraz bazy danych
    """
    try:
        # Ustaw filtr na nieuszkodzone
        context.results_page.select_nieuszkodzony()
        print("🔧 Ustawiono filtr: nieuszkodzone")

        # Scroll żeby załadować więcej ofert
        context.driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Pobierz oferty
        print(f"🔄 Pobieranie {MAX_OFFERS_LIMIT} ofert...")
        context.dane_ofert = context.results_page.get_n_offers(n=MAX_OFFERS_LIMIT)

        if context.dane_ofert:
            print(f"📦 Pobrano {len(context.dane_ofert)} ofert")

            # Zapisz do CSV
            plik_csv = "oferty_bmw_m3.csv"
            csv_success = zapisz_do_csv(context.dane_ofert, plik_csv)

            # Zapisz do bazy danych (batch insert - bardziej efektywne)
            context.liczba_zapisanych = zapisz_oferty_do_bazy_batch(context.dane_ofert)

            # Wyświetl podsumowanie każdej oferty
            for i, oferta in enumerate(context.dane_ofert, 1):
                tytul = oferta.get('tytul', oferta.get('title', 'Brak tytułu'))
                print(f"✅ Oferta {i}/{len(context.dane_ofert)}: {tytul[:50]}...")

            # Zapisz statystyki do context
            context.scroll_stats = {
                'scrolls': 1,
                'total_offers': len(context.dane_ofert),
                'saved_to_db': context.liczba_zapisanych,
                'csv_file': plik_csv if csv_success else None,
                'csv_success': csv_success,
                'limit_reached': len(context.dane_ofert) >= MAX_OFFERS_LIMIT
            }

            print(f"📊 PODSUMOWANIE:")
            print(f"   • Pobrano ofert: {len(context.dane_ofert)}")
            print(f"   • Zapisano do bazy: {context.liczba_zapisanych}")
            print(f"   • Zapisano do CSV: {'✅' if csv_success else '❌'}")

        else:
            print("❌ Nie pobrano żadnych ofert")
            context.scroll_stats = {
                'scrolls': 1,
                'total_offers': 0,
                'saved_to_db': 0,
                'csv_file': None,
                'csv_success': False,
                'limit_reached': False
            }

    except Exception as e:
        print(f"❌ Błąd podczas pobierania i zapisywania ofert: {e}")
        context.scroll_stats = {
            'scrolls': 1,
            'total_offers': 0,
            'saved_to_db': 0,
            'csv_file': None,
            'csv_success': False,
            'limit_reached': False,
            'error': str(e)
        }


@Then('close browser')
def step_close_browser(context):
    """Zamyka przeglądarkę"""
    if hasattr(context, 'driver'):
        context.driver.quit()
        print("🔚 Przeglądarka została zamknięta")



