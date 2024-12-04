import sqlite3

# Class to handle SQLite database operations
class Database:

    # Initialize the Database with the database file name
    def __init__(self, database_Reviews):
        self.database_Reviews = database_Reviews

    # Create a database table to store Wufoo form entries
    def create_table(self):
        connection = None
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect(self.database_Reviews)
            cursor = connection.cursor()

            # Execute the SQL statement to create the table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS WufooEntries (
                    EntryID INTEGER PRIMARY KEY,
                    BusinessName TEXT,
                    Rating INTEGER,
                    TimeFoodAvailable TEXT,
                    Feedback TEXT
                )
            ''')
            # Commit the changes to the database
            connection.commit()
            print(f"Table 'WufooEntries' created successfully in database '{self.database_Reviews}'.")
        except sqlite3.Error as e:
            # Handle exceptions during table creation
            print(f"Error creating table: {e}")
        finally:
            # Ensure the connection is closed
            if connection:
                connection.close()

    # Insert form entries into the database
    def insert_entries(self, entries):
        connection = None
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect(self.database_Reviews)
            cursor = connection.cursor()

            # Iterate over each entry and insert it into the database
            for entry in entries:
                cursor.execute('''
                    INSERT OR IGNORE INTO WufooEntries (EntryID, BusinessName, Rating, TimeFoodAvailable, Feedback)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    # Make sure to replace 'Field#' with the actual field name given from Wufoo
                    entry.get('EntryId'),
                    entry.get('Field1', 'N/A'),
                    entry.get('Field2', 'N/A'),
                    entry.get('Field3', 'N/A'),
                    entry.get('Field4', 0),
                    entry.get('Field5', 'N/A')
                ))
            # Commit the changes to the database
            connection.commit()
            print(f"Inserted {len(entries)} entries into the database.")
        except sqlite3.Error as e:
            # Handle exceptions during data insertion
            print(f"Error inserting entries: {e}")
        finally:
            # Ensure the connection is closed
            if connection:
                connection.close()