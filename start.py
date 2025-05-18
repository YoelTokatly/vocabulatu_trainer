
import json
import sqlite3
import os
import pandas as  pd

def initial_db(FILE_PATH,DB_PATH):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        


            
        # Read the JSON file
        with open(FILE_PATH, 'r') as file:
            vocabulary_data = json.load(file)
        
        # Connect to SQLite database (creates it if it doesn't exist)
   
        
        # Create tables if they don't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS units (
            unit_id TEXT PRIMARY KEY,
            unit_name TEXT NOT NULL
        )
        ''')

        
    
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_id TEXT NOT NULL,
            word TEXT NOT NULL,
            meaning TEXT NOT NULL,
            FOREIGN KEY (unit_id) REFERENCES units(unit_id)
        )
        ''')
        
        #check if empty
        query = f"SELECT count(*) as rows  FROM vocabulary " 
        result = pd.read_sql(query,conn)['rows'][0]
        if result == 0: 
            
            # Insert data into the database
            for unit_name, words in vocabulary_data.items():
                # Insert unit
                cursor.execute("INSERT OR REPLACE INTO units (unit_id, unit_name) VALUES (?, ?)",
                            (unit_name, unit_name))
                
                # Insert words
                for word_data in words:
                    cursor.execute(
                        "INSERT INTO vocabulary (unit_id, word, meaning) VALUES (?, ?, ?)",
                        (unit_name, word_data["word"], word_data["meaning"])
                    )

        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False