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

if __name__ == "__main__":
    conn = polacz()
    if conn:
        stworz_tabele(conn)
        conn.close()  # Zamknij połączenie po wykonaniu operacji