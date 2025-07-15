Feature: showing off behave

  Scenario: run a simple test
    Given baza polaczona
    Given launch chrome browser
    When open otomoto
    When ochrona
    When wyszukuje marke i model
    When listuje i zapisuje 10 aut
    Then close browser