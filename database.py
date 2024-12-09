import sqlite3

from Tools.scripts.mailerdaemon import emparse_list


# This class handles SQLite database operations.
class Database:
    def __init__(self, database_name):
        self.database_name = database_name

    # Creates a table for form entries on Wufoo.
    def create_table(self):
        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()

            # Only creates table if there is not one there already
            # and creates the columns for the table.
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS DiningHall_Rating (
                    EntryID INTEGER PRIMARY KEY,
                    DiningHall TEXT,
                    Mealtime TEXT,
                    Beverage TEXT,
                    Cuisine TEXT,
                    FoodTemp TEXT,
                    Dessert TEXT,
                    Dinning TEXT,
                    Feedback TEXT
                )
            ''')
            connection.commit()
            print(f"Table 'DiningHall_Rating' created successfully in database '{self.database_name}'.")

            # # Clears the table of any data
            # cursor.execute(f"DELETE FROM DiningHall_Rating")
            # connection.commit()

        # Used "Error as e" to know what type of error.
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        # Finally close the connection when all data is processed.
        finally:
            connection.close()

    # Inserts form entries into the DiningHall_Rating table.
    def insert_entries(self, entries):
        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()

            # Iterate through each entry in entries and insert it into the correct field.
            for entry in entries:
                dining_hall = entry.get('Field9')  # DiningHall
                mealtime = entry.get('Field10')  # Mealtime
                beverage = entry.get('Field16')  # Beverage
                cuisine = entry.get('Field15')  # Cuisine
                foodtemp = entry.get('Field14')  # FoodTemp
                dessert = entry.get('Field13')  # Dessert
                dinning = entry.get('Field12')  # Dinning
                feedback = entry.get('Field19')  # Feedback

                # The pulled data will be added into the database table.
                cursor.execute('''
                        INSERT INTO DiningHall_Rating (
                        DiningHall, Mealtime, Beverage, 
                        Cuisine, FoodTemp, Dessert, Dinning, Feedback)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (dining_hall, mealtime, beverage, cuisine,
                     foodtemp, dessert, dinning, feedback))

            # Commit changes to the database after all entries are added.
            connection.commit()
            print(f"Inserted {len(entries)} forms into the database.")

        # Error handling
        except sqlite3.Error as e:
            print(f"Error inserting entries: {e}")
        finally:
            connection.close()
