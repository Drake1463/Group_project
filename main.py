from wufoo_API_client import WufooAPIClient
from database import Database

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
        db_manager = Database(database_Reviews)

        # Create the database table
        db_manager.create_table()

        # Insert the fetched entries into the database
        db_manager.insert_entries(entries)
    else:
        # Print a message if no entries were retrieved
        print("No entries retrieved from the Wufoo form.")

# Run the main function
if __name__ == '__main__':
    main()