import requests
import logging

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Base URLs
BASE_URLS = {
    'spacex': 'https://api.spacexdata.com/v4/',
    'static': 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/',
}

# Generalized fetch function
def fetch_data(endpoint, base_url_type='spacex'):
    base_url = BASE_URLS.get(base_url_type)
    if not base_url:
        logging.error(f"Invalid base URL type: {base_url_type}")
        return None
    
    url = f"{base_url}{endpoint}"
    try:
        logging.info(f"Fetching data from {url}")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return None

# Fetching specific datasets
def fetch_initial_spacex_data():
    return fetch_data('API_call_spacex_api.json', base_url_type='static')

def fetch_rockets_data():
    return fetch_data('rockets', base_url_type='spacex')

def fetch_launchpads_data():
    return fetch_data('launchpads', base_url_type='spacex')

def fetch_payloads_data():
    return fetch_data('payloads', base_url_type='spacex')

def fetch_cores_data():
    return fetch_data('cores', base_url_type='spacex')

