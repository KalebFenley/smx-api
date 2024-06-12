import os
import requests
from dotenv import load_dotenv

# load from .env file
load_dotenv

api_url = os.getenv('SMX_API_URL')
username = os.getenv('SMX_USERNAME')
password = os.getenv('SMX_PASSWORD')

headers = {
    'Content-Type': 'application/json'
}

def query_alarms():
    """
    Queries the SMX API for a list of standing alarms.

    This function retrieves a list of standing alarms from the SMX API. 
    **Before using this function, please ensure the following environment variables are set, or built in .env file:**

    * `SMX_API_URL`: The base URL of the SMX API (e.g., "https://{smx_ip}:18443/rest/v1/").
    * `SMX_USERNAME`: The username for authentication with the SMX API.
    * `SMX_PASSWORD`: The password for authentication with the SMX API.

    **Security Note:** It's highly recommended to store sensitive information like credentials in environment variables 
    instead of directly in your code. This improves security and makes code management easier.

    Returns:
        dict: A dictionary containing the response data from the SMX API, including a list of standing alarms on success.

    Raises:
        requests.exceptions.HTTPError: If the SMX API responds with an error status code.
        requests.exceptions.RequestException: If any other request-related exception occurs.
    """

    endpoint = "fault/alarm"
    params = {
        "offset":0,
        "limit":0,
    }
    r = requests.get(f'{api_url}{endpoint}', params=params, auth=(username, password), headers=headers, verify=False)
    try:
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.HTTPError as err:
        print(f'HTTP error occurred: {err}')
    except requests.exceptions.RequestException as err:
        print(f'Request exception occurred: {err}')
    return(data)

alarms = query_alarms()

"""
Basic example of parsing alarms.
Ideally you would have more logic in place to alert/discard based on alarm type/severity...ect
"""
for alarm in alarms:
    if alarm['severity'] == "MAJOR":
        # Here you would call a function to alert.
        for i in alarm:
            print(f"{i:30} {alarm[i]}")
