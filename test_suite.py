import unittest
import sqlite3
from database import Database
from wufoo_API_client import WufooAPIClient
from app import fetch_data_from_db, create_main_window

class TestGUI(unittest.TestCase):
    def setUp(self):
        # Use an in-memory database for testing
        self.db_name = ":memory:"
        self.db = Database(self.db_name)
        self.db.create_table()  # Ensure table is created

        # Insert some data into the table
        entries = [
            {
                'Field9': 'Dining Hall A',
                'Field10': 'Lunch',
                'Field16': 'Water',
                'Field15': 'Italian',
                'Field14': 'Hot',
                'Field13': 'Cake',
                'Field12': 'Clean',
                'Field19': 'Great experience!'
            },
            {
                'Field9': 'Dining Hall B',
                'Field10': 'Dinner',
                'Field16': 'Juice',
                'Field15': 'Mexican',
                'Field14': 'Warm',
                'Field13': 'Pie',
                'Field12': 'Spacious',
                'Field19': 'Loved the ambiance!'
            }
        ]
        self.db.insert_entries(entries)

        # Fetch data to confirm it is inserted
        headers, rows = fetch_data_from_db(self.db_name)
        print(f"Headers after insertion: {headers}")  # Debugging line
        print(f"Rows after insertion: {rows}")  # Debugging line

    def fetch_data_from_db(self, query="SELECT * FROM DiningHall_Rating"):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        headers = [description[0] for description in cursor.description]

        print(f"Headers: {headers}")  # Debug print
        print(f"Rows: {rows}")  # Debug print

        connection.close()

        return headers, rows




class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Use an in-memory database for testing
        self.db_name = ":memory:"
        self.db = Database(self.db_name)
        self.db.create_table()

    def test_create_table(self):
        # Check if the table was created
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info('DiningHall_Rating');")
        if not cursor.fetchall():
            print("Table 'DiningHall_Rating' does not exist.")
        connection.close()

    def test_insert_entries(self):
        # Now, execute the SELECT query to fetch the data
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='DiningHall_Rating';")
        table = cursor.fetchone()
        print(f"Table check result: {table}")  # Debugging line

        # Now fetch the data from the table
        cursor.execute("PRAGMA table_info('DiningHall_Rating');")
        rows = cursor.fetchall()
        print(f"Inserted rows: {rows}")  # Debugging line

        connection.close()


class TestWufooAPIClient(unittest.TestCase):
    def setUp(self):
        # Set up the Wufoo client with an invalid API key
        self.client = WufooAPIClient("invalid_api_key")

    def test_obtain_data(self):
        # Test API data retrieval with an invalid key
        entries = self.client.obtain_data()
        self.assertEqual(len(entries), 0, "API client should not retrieve data with an invalid API key.")

if __name__ == "__main__":
    unittest.main()
