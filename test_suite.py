import unittest
import sqlite3
from database import Database
from wufoo_API_client import WufooAPIClient
from main import fetch_data_from_db, create_main_window
import PySimpleGUI as sg


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
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='DiningHall_Rating';")
        self.assertIsNotNone(cursor.fetchone(), "Table was not created successfully.")
        connection.close()

    def test_insert_entries(self):
        # Insert test entries
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
            }
        ]
        self.db.insert_entries(entries)

        # Fetch data directly from the database
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM DiningHall_Rating")
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 1, "Data insertion failed.")
        self.assertEqual(rows[0][1], 'Dining Hall A', "Inserted data does not match expected values.")
        connection.close()


class TestWufooAPIClient(unittest.TestCase):
    def setUp(self):
        # Set up the Wufoo client with an invalid API key
        self.client = WufooAPIClient("invalid_api_key")

    def test_obtain_data(self):
        # Test API data retrieval with an invalid key
        entries = self.client.obtain_data()
        self.assertEqual(len(entries), 0, "API client should not retrieve data with an invalid API key.")


class TestGUI(unittest.TestCase):
    def setUp(self):
        # Use an in-memory database with some preloaded data
        self.db_name = ":memory:"
        self.db = Database(self.db_name)
        self.db.create_table()
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

    def test_fetch_data_from_db(self):
        # Test fetching data directly from the database
        headers, rows = fetch_data_from_db(self.db_name)
        self.assertEqual(len(headers), 8, "Headers count does not match expected.")
        self.assertEqual(len(rows), 2, "Row count does not match expected.")
        self.assertEqual(rows[0][1], 'Dining Hall A', "First row data mismatch.")

    def test_gui_display(self):
        # Test if the main window initializes correctly
        window = create_main_window(self.db_name)
        table = window['-TABLE-']
        self.assertEqual(len(table.Values), 2, "GUI table does not display correct number of rows.")
        self.assertEqual(table.Values[0][1], 'Dining Hall A', "First row in GUI table does not match expected data.")
        window.close()

    def test_gui_sorting(self):
        # Test sorting functionality via GUI
        window = create_main_window(self.db_name)
        sort_column = 'DiningHall'
        query = f"SELECT * FROM DiningHall_Rating ORDER BY {sort_column}"
        headers, sorted_data = fetch_data_from_db(self.db_name, query)
        window['-TABLE-'].update(values=[list(row) for row in sorted_data])

        # Validate sorting
        table = window['-TABLE-']
        self.assertEqual(table.Values[0][1], 'Dining Hall A', "Sorting did not arrange data correctly.")
        window.close()


if __name__ == "__main__":
    unittest.main()