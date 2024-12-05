import json
import sqlite3
import requests
from requests.auth import HTTPBasicAuth

# Class to handle API interactions with Wufoo
class WufooAPIClient:

    # Initialize the WufooAPIClient with API key
    def __init__(self, api_key):
        self.api_key = api_key


    # Fetch data from the Wufoo form
    def fetch_data(self):
  
        # Construct the API endpoint URL
        url = 'https://redscale.wufoo.com/api/v3/forms/Final/entries/json'
        
        # Make the GET request to the API
        response = requests.get(url, auth=HTTPBasicAuth(self.api_key, 'pass'))
        # Check if the request was successful
        if response.status_code == 200:
            print("Successfully authenticated!")
            # Return the list of entries
            return response.json().get('Entries', [])
        else:
            # Print an error message if authentication fails
            print(f"Failed to authenticate. Status code: {response.status_code}")
            return []

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
                    INSERT OR IGNORE INTO WufooEntries (EntryID, BusinessName, Rating, Feedback)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    # Make sure to replace 'Field#' with the actual field name given from Wufoo
                    # entry.get('EntryId'),
                    entry.get('Crimson Dining ', 'N/A'),
                    entry.get('Maxwell Cafe', 'N/A'),
                    entry.get('East Campus Commons', 'N/A'),
                    entry.get('Flynn Dinning Commmons', 'N/A'),
                    entry.get('The Bear', 'N/A')
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

# Main's function is to fetch data and storing it in database_Reviews
def main():
    # Load the API key from the file named secret.txt
    try:
        with open('secret.txt', 'r') as file:
            api_key = file.read().strip()
    except FileNotFoundError:
        # Handle the case where the secret file is missing
        print("Error: secret.txt was not found. You might wanna find it.  :)")
        return

    # Initialize the Wufoo API client
    wufoo_client = WufooAPIClient(api_key)

    # Fetch data from the Wufoo form
    entries = wufoo_client.fetch_data()

    # Check if there are entries to process
    if entries:
        # Define the name of the SQLite database
        database_Reviews = 'WufooData.db'

        # Initialize the database manager
        db = Database(database_Reviews)

        # Create the database table
        db.create_table()

        # Insert the fetched entries into the database
        db.insert_entries(entries)
    else:
        # Print a message if no entries were retrieved
        print("No entries retrieved from the Wufoo form.")

# Run the main function
if __name__ == '__main__':
    main()
