import sqlite3
import csv

# Define the path to your CSV file
CSV_FILE_PATH = 'C:/Users/CHRISTIAN/OneDrive/Documents/Projects/Pokemon Guessing Game/database/Pokedex_Database_VF.csv'
DB_FILE_PATH = 'C:/Users/CHRISTIAN/OneDrive/Documents/Projects/Pokemon Guessing Game/database/pokemon.db'


def create_database():
    # Connect to (or create) the SQLite database
    conn = sqlite3.connect(DB_FILE_PATH)
    cur = conn.cursor()

    # Create the Pokemon table based on the CSV structure
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Pokemon (
            No INTEGER PRIMARY KEY,       -- Pokedex number
            Name TEXT NOT NULL,            -- Pokémon name
            Generation INTEGER NOT NULL,   -- Pokémon generation
            Type1 TEXT NOT NULL,           -- Primary type
            Type2 TEXT,                    -- Secondary type (can be NULL)
            Category TEXT NOT NULL         -- Category (Ordinary, Legendary, etc.)
        )
    ''')

    conn.commit()
    conn.close()

def insert_pokemon_data_from_csv():
    # Connect to the database
    conn = sqlite3.connect(DB_FILE_PATH)
    cur = conn.cursor()

    # Open the CSV file and read its content
    with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row

        # Insert each row from the CSV into the database
        for row in reader:
            pokedex_number, name, generation, type1, type2, category = row
            type2 = type2 if type2 != '' else None  # Replace empty string with None

            # Check if the Pokémon is already in the database
            cur.execute('SELECT No FROM Pokemon WHERE No = ?', (pokedex_number,))
            if cur.fetchone() is None:
                # Insert only if the Pokémon does not already exist
                cur.execute('''
                    INSERT INTO Pokemon (No, Name, Generation, Type1, Type2, Category)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (pokedex_number, name, generation, type1, type2, category))

    # Commit and close the connection
    conn.commit()
    conn.close()


def verify_data_insertion():
    # Connect to the database
    conn = sqlite3.connect(DB_FILE_PATH)
    cur = conn.cursor()

    # Fetch the first 10 Pokémon entries to verify
    cur.execute('SELECT * FROM Pokemon LIMIT 10')
    rows = cur.fetchall()

    # Print the result
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    create_database()              # Step 1: Create the table
    insert_pokemon_data_from_csv()  # Step 2: Insert data from CSV
    verify_data_insertion()         # Step 3: Verify data
    print("Database created, data inserted from CSV, and verified successfully!")
