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
