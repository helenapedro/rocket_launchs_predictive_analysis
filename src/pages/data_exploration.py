import os
import sys
import dash_bootstrap_components as dbc

# Add the parent directory to the system path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import custom modules
from data.clean_data import fetch_and_clean_launch_data
from data.data_fetch import fetch_initial_data
from data.row_data import fetch_initial_data_layout
from utils.api_description import eda_rest_api

# Fetch and clean launch data
launch_data = fetch_and_clean_launch_data()

def create_exploration_page():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    eda_rest_api(),
                )
            ),
        ],
        fluid=True,
        className="mt-5 px-4"
    )

# Fetch and process data
initial_data = fetch_initial_data()
initial_data_layout = fetch_initial_data_layout()

# Create the exploration page layout
layout = create_exploration_page()
