from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import logging
import os
from datetime import datetime
from page_objects.otomoto_main_page import OtomotoMainPage
from page_objects.otomoto_result_page import OtomotoResultsPage

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("OtomotoSteps")

# Create output directory if it doesn't exist
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Default download directory
prefs = {"download.default_directory" : "/Users/maciej/PycharmProjects/behaveProject"}

@Given('launch chrome browser')
def step_impl(context):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option("prefs", prefs)
    context.driver = webdriver.Chrome(options=chrome_options)
    context.driver.maximize_window()
    context.main_page = OtomotoMainPage(context.driver)
    context.results_page = OtomotoResultsPage(context.driver)

@When('open otomoto')
def step_impl(context):
    context.driver.get("https://www.otomoto.pl")
    logger.info("Opened Otomoto website")

@When('ochrona') ##zamyka pop-up
def step_impl(context):
    try:
        context.main_page.accept_cookies()
        logger.info("Accepted cookies")
    except Exception as e:
        logger.error(f"Failed to accept cookies: {str(e)}")
        context.scenario.skip(reason=f"Failed to accept cookies: {str(e)}")

@When("wyszukuje marke i model")
def step_impl(context):
    try:
        context.main_page.open_marka_list()
        context.main_page.enter_marka("BMW")
        context.main_page.select_marka()
        context.main_page.open_model_list()
        context.main_page.enter_model("M3")
        context.main_page.select_model()
        context.main_page.click_pokaz_ogloszenia()
        logger.info("Successfully selected BMW M3 and navigated to results page")
    except Exception as e:
        logger.error(f"Failed during car selection: {str(e)}")
        context.scenario.skip(reason=f"Failed during car selection: {str(e)}")

@When("listuje auta")
def step_impl(context):
    try:
        context.results_page.select_nieuszkodzony()
        logger.info("Selected 'Nieuszkodzony' filter")
        context.dane_ofert = context.results_page.get_n_offers(n=10)
        logger.info(f"Successfully retrieved {len(context.dane_ofert)} offers")

        # Store extraction timestamp
        context.extraction_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    except Exception as e:
        logger.error(f"Failed to list cars: {str(e)}")
        context.scenario.skip(reason=f"Failed to list cars: {str(e)}")

@Then('zapisuje dane')
def step_impl(context):
    # Use timestamp in filename to avoid overwriting previous data
    base_filename = f"bmw_m3_{context.extraction_timestamp}"
    plik_csv = os.path.join(output_dir, f"{base_filename}.csv")

    if hasattr(context, 'dane_ofert') and context.dane_ofert:
        try:
            # Write data to CSV
            klucze = context.dane_ofert[0].keys()
            with open(plik_csv, 'w', newline='', encoding='utf-8') as plik_csv_file:
                dict_writer = csv.DictWriter(plik_csv_file, fieldnames=klucze)
                dict_writer.writeheader()
                dict_writer.writerows(context.dane_ofert)

            logger.info(f"Data saved to file {plik_csv}")
            print(f"Dane zostały zapisane do pliku {plik_csv}")

            # Also save stats about the extraction
            stats_file = os.path.join(output_dir, f"{base_filename}_stats.txt")
            with open(stats_file, 'w', encoding='utf-8') as stats_file:
                stats_file.write(f"Extraction timestamp: {context.extraction_timestamp}\n")
                stats_file.write(f"Total offers extracted: {len(context.dane_ofert)}\n")
                stats_file.write(f"Successfully saved to: {plik_csv}\n")
        except Exception as e:
            logger.error(f"Failed to save data: {str(e)}")
            print(f"Błąd podczas zapisywania danych: {str(e)}")
    else:
        error_msg = "No data was collected, CSV file was not created"
        logger.error(error_msg)
        print("Nie pobrano żadnych danych, plik CSV nie został utworzony.")

        # Create error report
        error_file = os.path.join(output_dir, f"{base_filename}_error.txt")
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write(f"Extraction timestamp: {context.extraction_timestamp}\n")
            f.write("Error: No data was collected\n")

            if hasattr(context, 'dane_ofert'):
                f.write("dane_ofert exists but is empty\n")
            else:
                f.write("dane_ofert attribute doesn't exist\n")

@Then('close browser')
def step_impl(context):
    if hasattr(context, 'driver'):
        context.driver.quit()
        logger.info("Browser closed")
    else:
        logger.warning("No driver instance found to close")