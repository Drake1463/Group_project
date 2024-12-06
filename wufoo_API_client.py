import requests
from requests.auth import HTTPBasicAuth

# This class handles the API interactions with Wufoo.
class WufooAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key

    # Obtains data from the Wufoo form.
    def obtain_data(self):
        url = 'https://redscale.wufoo.com/api/v3/forms/Final/entries/json'
        response = requests.get(url, auth=HTTPBasicAuth(self.api_key, 'pass'))

        # Check if the request was successful, return entries, else error.
        if response.status_code == 200:
            print("Successfully authenticated!")
            return response.json().get('Entries', [])
        else:
            # response.status_code is used to print error code for debugging.
            print(f"Failed to authenticate. Status code: {response.status_code}")
            return []
