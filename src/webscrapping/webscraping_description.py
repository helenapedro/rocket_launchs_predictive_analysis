from utils.description_card import create_description_card
from utils.webscraping_snippet import snippet

def create_webscraping_description():
    button_id = "toggle-webscraping-description"
    button_text = "Show/Hide Code Snippet"
    description_text = """
          The web scraping process involved accessing Wikipedia's 'List of Falcon 9 and Falcon Heavy launches' page 
          to extract historical launch data. Using BeautifulSoup, the HTML table was parsed, cleaned, and formatted 
          into a Pandas DataFrame for further analysis.
     """
    code_snippet = """
```python
     from bs4 import BeautifulSoup
     import pandas as pd
     import requests

     # Main scraping function
     def fetch_falcon_9_launch_data():
          url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
          response = requests.get(url)
          soup = BeautifulSoup(response.text, 'html.parser')

          # Locate and parse the target table
          html_tables = soup.find_all('table', class_='wikitable plainrowheaders collapsible')
          launch_table = html_tables[2]  # Use the 3rd table containing launch data

          # Extract column names
          column_names = [extract_column_from_header(th) for th in launch_table.find_all('th')]

          # Initialize the data dictionary
          launch_data = {name: [] for name in column_names}

          # Scrape rows
          for row in launch_table.find_all('tr'):
               if row.th and row.th.string and row.th.string.strip().isdigit():
                    cells = row.find_all('td')

                    # Extract key data points
                    date, time = parse_date_time(cells[0])
                    launch_data['Date'].append(date)
                    launch_data['Time'].append(time)
                    launch_data['Payload'].append(cells[3].a.string if cells[3].a else 'N/A')
                    launch_data['Orbit'].append(cells[5].a.string if cells[5].a else 'N/A')
                    launch_data['Launch outcome'].append(cells[7].string.strip() if cells[7].string else 'N/A')

          # Convert to DataFrame
          return pd.DataFrame(launch_data)

     # Helper function: Extract column names
     def extract_column_from_header(header):
          for tag in ['br', 'a', 'sup']:
               if getattr(header, tag):
                    getattr(header, tag).extract()
          return ' '.join(header.stripped_strings)

     # Helper function: Parse date and time
     def parse_date_time(cell):
          date_time = list(cell.stripped_strings)
          return date_time[0].strip(','), date_time[1] if len(date_time) > 1 else 'N/A'
```
     """

    card_id = "webscraping-data-description"
    
    # Pass all required arguments to the function
    description_card = create_description_card(
        button_id, 
        button_text, 
        description_text, 
        code_snippet, 
        card_id
    )
    
    return description_card