Feature: showing off behave

  Scenario: run a simple test
    Given launch chrome browser
    When open otomoto
    When ochrona
    When wyszukuje marke i model
    When listuje auta
    Then zapisuje dane
    Then close browser