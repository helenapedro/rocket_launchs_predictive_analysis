from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

# Import tabs
from tabs.rockets_tab import rockets_tab
from tabs.graphs_tab import payload_mass_distribution_tab
from tabs.launch_tab import launch_tab
from tabs.cores_tab import cores_tab
from tabs.payloads_tab import payloads_tab
from tabs.core_reuse_tab import cores_reuse_tab

from data.data_fetch import fetch_and_process_data

def eda_rest_api():
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H1(
                    "EDA with REST API", 
                    className="card-title text-center fw-bold",
                    style={'color': '#4CAF50'}
                ),
            ),

            html.Div(
                [
                    html.P(
                        "This dataset was gathered using a GET request from the SpaceX REST API. "
                        "Click the button to view the code snippet and explore how this data was fetched.",
                        className="text-center text-muted",
                    )
                ],
                className="hero-section",
            ),

            dbc.CardBody(
                [
                    dbc.Button(
                        "View/Hide Code Snippet",
                        id="toggle-api-button-summary",
                        className="btn btn-primary mb-3",
                    ),
                    dcc.Markdown(id="api-summary-content", style={"display": "none"}),
                    dcc.Store(id="api-snippet-visible", data=False),  # Store for visibility state
                ]
            ),

            # Tabs Section
            dbc.Row(
                dbc.Col(
                    dcc.Tabs(
                        [
                            rockets_tab(rockets_df),
                            launch_tab(launchpads_df),
                            payloads_tab(payloads_df),
                            cores_tab(cores_df),
                            payload_mass_distribution_tab(payloads_df),
                            cores_reuse_tab(cores_df),
                        ],
                        className='custom-tabs',
                        style={'border': '1px solid #dee2e6', 'borderRadius': '0.25rem'}
                    )
                )
            )
        ],
        className="mb-4 shadow-sm",
    )

rockets_df, launchpads_df, payloads_df, cores_df = fetch_and_process_data()

@callback(
    [Output("api-summary-content", "children"), Output("api-summary-content", "style"), Output("api-snippet-visible", "data")],
    Input("toggle-api-button-summary", "n_clicks"),
    State("api-snippet-visible", "data"),
    prevent_initial_call=True
)
def update_api_summary(n_clicks, is_visible):
    # Toggle visibility state
    new_visibility = not is_visible

    if new_visibility:
        code_snippet = """
```python
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = {
    'spacex': 'https://api.spacexdata.com/v4/',
}

# Generalized fetch function
def fetch_data(endpoint, base_url_type='spacex'):
    base_url = BASE_URL.get(base_url_type)
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

# Example fetch calls:
fetch_rockets_data = fetch_data('rockets')
fetch_launchpads_data = fetch_data('launchpads')
```
    """
        style = {"display": "block"}
    else:
        code_snippet = ""
        style = {"display": "none"}
    return code_snippet, style, new_visibility