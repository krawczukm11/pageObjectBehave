Feature: showing off behave

  Scenario: run a simple test
    Given baza polaczona
    Given launch chrome browser
    When open otomoto
    When ochrona
    When wyszukuje marke i model
    When listuje auta
    #When zapisuje linki
    Then close browser