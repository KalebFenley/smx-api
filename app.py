import os
import requests
from dotenv import load_dotenv

'''
Before using this please ensure the following environment variables are set, or built in .env file:

SMX_API_URL: The base URL of the SMX API (e.g., "https://{smx_ip}:18443/rest/v1/").
SMX_USERNAME: The username for authentication with the SMX API.
SMX_PASSWORD: The password for authentication with the SMX API.
'''


# load from .env file
load_dotenv

api_url = os.getenv('SMX_API_URL')
username = os.getenv('SMX_USERNAME')
password = os.getenv('SMX_PASSWORD')

headers = {
    'Content-Type': 'application/json'
}

def query_devices():
    endpoint = "config/device"
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
        return(False)
    except requests.exceptions.RequestException as err:
        print(f'Request exception occurred: {err}')
        return(False)
    return(data)

def query_alarms():
    """
    This function retrieves a list of standing alarms from the SMX API.
    
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

# Pull all standing alarms from SMX
alarm_list = query_alarms()
"""
Basic example of parsing alarms.
Ideally you would have more logic in place to alert/discard based on alarm type/severity...ect
"""
for alarm in alarm_list:
    if alarm['severity'] == "MAJOR":
        # Here you would call a function to alert.
        for i in alarm:
            print(f"{i:30} {alarm[i]}")

# Pull Device Information from SMX
device_list = query_devices()
# Build a dict contianing hostname:ipaddress for every Calix OLT
hostname_ip_dict = {}
for device in device_list:
    hostname_ip_dict[f"{device['hostname']}"] = device["address"]