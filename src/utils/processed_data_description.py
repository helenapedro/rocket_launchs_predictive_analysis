from utils.description_card import create_description_card

def create_processed_data_description():
    description_text = (
        "Click the button to view the code snippet."
    )
    code_snippet = """
     import pandas as pd
     from utils.data import fetch_rockets_data, fetch_initial_spacex_data
    
     def fetch_and_process_data():
          rockets_data = fetch_rockets_data()
          initial_data = fetch_initial_spacex_data()

          # Convert data to DataFrame
          rockets_df = pd.DataFrame(rockets_data)[['name', 'height', 'mass']]
     
          # Map rocket IDs to booster names
          rocket_id_to_booster_name = {r['id']: r['name'] for r in rockets_data}

          return rockets_df, initial_data
     """
    return create_description_card("toggle-processed-summary", "Show/Hide Code Snippet", description_text, code_snippet, "processed-data-content")
