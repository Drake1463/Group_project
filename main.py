import json
import sqlite3
import requests


from requests.auth import HTTPBasicAuth

with open('secrets.txt', 'r') as file:
    api_key = file.read().strip()
#Accesses the form. the username is redscale and the forms name is Final
url = 'https://redscale.wufoo.com/api/v3/forms/Final/entries/json'

response = requests.get(url, auth=HTTPBasicAuth(api_key, 'pass'))

#prints a string to the user if the connection was succesful
if response.status_code == 200:
    print("Successfully authenticated!")
    print(response.json())
# prints a string to the user if the connection failed
else:
    print(f"Failed to authenticate. Status code: {response.status_code}")


if __name__ == '__main__':
    print('hello')