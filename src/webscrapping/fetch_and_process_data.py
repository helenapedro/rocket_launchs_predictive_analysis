from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
import requests

# Scraping function to fetch and process the Falcon 9 launches data
def fetch_falcon_9_launch_data():
    static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
    response = requests.get(static_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    html_tables = soup.find_all('table', class_='wikitable plainrowheaders collapsible')

    # Extract column names from the header of the third table
    column_names = []
    first_launch_table = html_tables[2]
    tc = first_launch_table.find_all('th')
    for th in tc:
        name = extract_column_from_header(th)
        if name and name != 'Date and time':  # Exclude the 'Date and time' column
            column_names.append(name)

    # Create dictionary to hold the scraped data, initializing with empty lists
    launch_dict = {name: [] for name in column_names}
    launch_dict['Launch site'] = []
    launch_dict['Payload'] = []
    launch_dict['Payload mass'] = []
    launch_dict['Orbit'] = []
    launch_dict['Customer'] = []
    launch_dict['Launch outcome'] = []
    launch_dict['Version Booster'] = []
    launch_dict['Booster landing'] = []
    launch_dict['Date'] = []
    launch_dict['Time'] = []

    # Scrape the data row by row
    for table in html_tables:
        for rows in table.find_all("tr"):
            if rows.th:
                flight_number = rows.th.string.strip() if rows.th.string else None
                if flight_number and flight_number.isdigit():
                    row = rows.find_all('td')

                    # Get Date and Time separately
                    datatimelist = date_time(row[0])
                    date = datatimelist[0].strip(',')
                    launch_dict['Date'].append(date)
                    time = datatimelist[1]
                    launch_dict['Time'].append(time)

                    # Booster version
                    bv = booster_version(row[1])
                    launch_dict['Version Booster'].append(bv or row[1].a.string)

                    # Other columns (Launch site, Payload, etc.)
                    launch_dict['Launch site'].append(row[2].a.string)
                    launch_dict['Payload'].append(row[3].a.string)
                    launch_dict['Payload mass'].append(get_mass(row[4]))
                    launch_dict['Orbit'].append(row[5].a.string)
                    launch_dict['Customer'].append(row[6].a.string if row[6].a else '')
                    
                    # Handling NoneType for Launch Outcome
                    launch_outcome = row[7].string.strip() if row[7].string else 'N/A'
                    launch_dict['Launch outcome'].append(launch_outcome)

                    launch_dict['Booster landing'].append(landing_status(row[8]))

    # Ensure all columns are the same length
    max_length = max(len(lst) for lst in launch_dict.values() if lst is not None)  # Find the maximum length, excluding None
    for key, value in launch_dict.items():
        # Append None (or any placeholder) to lists that are shorter
        while len(value) < max_length:
            value.append(None)

    # Convert the dictionary into a DataFrame
    df = pd.DataFrame(launch_dict)

    # Return only the relevant columns
    df = df[['Date', 'Time', 'Launch site', 'Payload', 'Payload mass', 'Orbit', 'Customer', 'Launch outcome', 'Version Booster', 'Booster landing']]

    return df

# Scraping Functions
def date_time(table_cells):
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    out = ''.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i % 2 == 0][0:-1])
    return out

def landing_status(table_cells):
    return [i for i in table_cells.strings][0]

def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass = mass[0:mass.find("kg") + 2]
    else:
        new_mass = 0
    return new_mass

def extract_column_from_header(row):
    if row.br:
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()

    column_name = ' '.join(row.contents)

    if not (column_name.strip().isdigit()):
        column_name = column_name.strip()
        return column_name
