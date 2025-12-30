from datetime import date
from dash import html
from dash import dash_table
import pandas as pd
import requests

def fetch_initial_data_from_api(endpoint):
    base_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/'
    url = f"{base_url}{endpoint}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def fetch_rocket_launch_data():
    return fetch_initial_data_from_api('API_call_spacex_api.json')

def fetch_and_clean_data(raw_data):
    if not raw_data:
        return pd.DataFrame()

    data = pd.json_normalize(raw_data)
    data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

    # Remove rows with multiple cores or payloads those are falcon rockets with 2 extra rocket boosters
    data = data[data['cores'].map(len) == 1]
    data = data[data['payloads'].map(len) == 1]

    # Extract single core and payload values
    data['cores'] = data['cores'].map(lambda x: x[0])
    data['payloads'] = data['payloads'].map(lambda x: x[0])

    # Convert cores and payloads columns to strings
    data['cores'] = data['cores'].apply(str)
    data['payloads'] = data['payloads'].apply(str)

    # Convert date_utc to datetime and restrict by date
    data['date'] = pd.to_datetime(data['date_utc']).dt.date
    data = data[data['date'] <= date(2020, 11, 13)]

    """ rocket_id_to_booster_name = {rocket['id']: rocket['name'] for rocket in data['rocket']}
     # Add booster names to launchpads DataFrame
    launchpad_booster_names = [
        rocket_id_to_booster_name.get(launchpad['rockets'][0], 'Unknown Booster') if launchpad['rockets'] else 'No Rockets'
        for launchpad in data['launchpad']
    ]

    data['launchpad']['booster_name'] = launchpad_booster_names
 """
    # Construct a cleaned DataFrame
    cleaned_data = pd.DataFrame({
        'FlightNumber': data['flight_number'],
        'Date': data['date'],
        'Rocket': data['rocket'],
        'launchpad': data['launchpad'],
        'Core': data['cores'],
        'Payload': data['payloads'],
    })

    return cleaned_data

def fetch_and_clean_launch_data():
    raw_data = fetch_rocket_launch_data()
    return fetch_and_clean_data(raw_data)

# Define the lists
""" BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []
 """
# Example functions to populate lists
""" def getBoosterVersion(data):
    global BoosterVersion
    BoosterVersion = [item['rocket'].get('rocket_name', 'Unknown') for item in data]

def getLaunchSite(data):
    global LaunchSite
    LaunchSite = [item['launch_site']['site_name_long'] for item in data]

def getPayloadData(data):
    global PayloadMass, Orbit
    for item in data:
        payload_mass = item['rocket']['second_stage']['payloads'][0].get('payload_mass_kg', 0)
        orbit = item['rocket']['second_stage']['payloads'][0].get('orbit', 'Unknown')
        PayloadMass.append(payload_mass)
        Orbit.append(orbit)

def getCoreData(data):
    global Outcome, Flights, GridFins, Reused, Legs, LandingPad, Block, ReusedCount, Serial, Longitude, Latitude
    for item in data:
        core = item['rocket']['first_stage']['cores'][0]
        Outcome.append(core.get('landing_success', 'Unknown'))
        Flights.append(core.get('flight', 0))
        GridFins.append(core.get('gridfins', False))
        Reused.append(core.get('reused', False))
        Legs.append(core.get('legs', False))
        LandingPad.append(core.get('landing_vehicle', 'Unknown'))
        Block.append(core.get('block', 0))
        ReusedCount.append(core.get('reuse_count', 0))
        Serial.append(core.get('core_serial', 'Unknown'))
        Longitude.append(item['launch_site']['site_location'].get('longitude', 0))
        Latitude.append(item['launch_site']['site_location'].get('latitude', 0))

# Assuming 'data' is your dataset
data_2 = fetch_rocket_launch_data()

# Call the functions to populate the lists
getBoosterVersion(data_2)
getLaunchSite(data_2)
getPayloadData(data_2)
getCoreData(data_2)

# Construct the dataset
launch_dict = {
    'FlightNumber': [item['flight_number'] for item in data_2],
    'Date': [item['date_utc'] for item in data_2],
    'BoosterVersion': BoosterVersion,
    'PayloadMass': PayloadMass,
    'Orbit': Orbit,
    'LaunchSite': LaunchSite,
    'Outcome': Outcome,
    'Flights': Flights,
    'GridFins': GridFins,
    'Reused': Reused,
    'Legs': Legs,
    'LandingPad': LandingPad,
    'Block': Block,
    'ReusedCount': ReusedCount,
    'Serial': Serial,
    'Longitude': Longitude,
    'Latitude': Latitude
}

# Create DataFrame
data_df = pd.DataFrame(launch_dict)

# Filter the DataFrame to keep only Falcon 9 launches
data_falcon9 = data_df[data_df['BoosterVersion'] != 'Falcon 1']

# Reset the FlightNumber column
data_falcon9.loc[:, 'FlightNumber'] = list(range(1, data_falcon9.shape[0] + 1))
 """
def create_clean_data(data):
    return html.Div(
        [
            html.H1('Data Wrangling', style={'textAlign': 'center', 'padding': '20px'}), 

            # Add a DataTable for the cleaned data
            html.Div(
                dash_table.DataTable(
                    id='launch-data-table',
                    columns=[{"name": col, "id": col} for col in data.columns],
                    data=data.to_dict('records'),
                    style_table={'overflowX': 'scroll'},
                    style_cell={'textAlign': 'left', 'padding': '10px'},
                    style_header={'backgroundColor': '#f1f1f1', 'fontWeight': 'bold'},
                ),
                style={'margin': '20px'},
            ),
        ],
        className="container",
    )

# Fetch and process data
launch_data = fetch_and_clean_launch_data()

# Create the exploration page layout
layout = create_clean_data(launch_data)