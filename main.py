from wufoo_API_client import WufooAPIClient
from database import Database


# Main function to obtain data and store it in the database.
def main():
    try:
        # API key is stored in the secret.txt file.
        with open('secret.txt', 'r') as file:
            api_key = file.read().strip()

    except FileNotFoundError:
        print("Error: secret.txt was not found. Better go find it. :)")
        return

    wufoo_client = WufooAPIClient(api_key)
    entries = wufoo_client.obtain_data()

    # Check if entries are retrieved and proceed.
    if entries:
        # Name of the database file is BSU_Reviews.db
        database_name = 'BSU_Reviews.db'
        db = Database(database_name)
        # Table is created
        db.create_table()
        # Insert the obtained entries
        db.insert_entries(entries)
    else:
        print("No entries retrieved from the Wufoo form. Sad :(")

# Execute the main function
if __name__ == '__main__':
    main()
