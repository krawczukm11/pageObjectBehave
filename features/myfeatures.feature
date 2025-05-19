Feature: Otomoto search functionality

  Scenario: Search for BMW M3
    Given launch chrome browser
    When open otomoto
    When ochrona
    When wyszukuje marke i model
    When listuje auta
    Then zapisuje dane
    Then close browser

  Scenario Outline: Search for different car brands and models
    Given launch chrome browser
    When open otomoto
    When ochrona
    When wyszukuje marke "<marka>" i model "<model>"
    When listuje auta
    Then zapisuje dane do "<plik_csv>"
    Then close browser

    Examples:
      | marka    | model | plik_csv                |
      | BMW      | M3    | oferty_bmw_m3.csv       |
      | Audi     | A4    | oferty_audi_a4.csv      |
      | Mercedes | CLA   | oferty_mercedes_cla.csv |