from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash import dash_table

from webscrapping.fetch_and_process_data import fetch_falcon_9_launch_data

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            html.H1(
                                "Falcon 9 and Falcon Heavy Launch Records", 
                                className='text-center mb-4', 
                                style={'color': '#4CAF50'}
                            ),
                        ),

                        # Hero Section
                        html.Div(
                            [
                                html.P(
                                    "The web scraping process involved accessing Wikipedia's 'List of Falcon 9 and Falcon Heavy launches' page "
                                    "to extract historical launch data. Using BeautifulSoup, the HTML table was parsed, cleaned, and formatted "
                                    "into a Pandas DataFrame for further analysis.",
                                    className='text-center text-muted'
                                ),
                            ],
                            className="hero-section"
                        ),

                        dbc.CardBody(
                            [
                                dbc.Row(
                                    dbc.Col(
                                        [
                                            dbc.Button(
                                                "View/Hide Code Snippet",
                                                id="toggle-webscraping-summary",
                                                className="btn btn-primary mb-3",
                                            ),
                                            dcc.Markdown(id="webscrapin-content", style={"display": "none"}),
                                            dcc.Store(id="webscraping-visible", data=False),
                                        ]
                                    ),    
                                ),

                                dbc.Row(
                                    dbc.Col(
                                        html.Button(
                                            "Download Scrape Launch Data", 
                                            id="scrape-button", 
                                            n_clicks=0, 
                                            className="btn btn-success my-3"
                                        ),
                                        className="d-flex justify-content-center"
                                    )
                                ),
                                
                                dbc.Row(
                                    dbc.Col(
                                        id="table-container", 
                                        className="mt-4"
                                    )
                                ),  
                                # Empty initially, filled after data fetch
                                dcc.Download(id="download-dataframe-csv")
                            ]
                        )
                    ]
                )
            )
        )
    ],
    fluid=True,
    className="mt-5"
)


# Dash Callback to update table and handle CSV download
@callback(
    [Output("table-container", "children"),
     Output("download-dataframe-csv", "data")],
    [Input("scrape-button", "n_clicks")]
)
def update_table(n_clicks):
    # Fetch and process the launch data
    df = fetch_falcon_9_launch_data()

    # Convert DataFrame to Dash table
    table = dash_table.DataTable(
        id="launch-table",
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'center'},
    )

    # Generate CSV download only when button is clicked
    if n_clicks > 0:
        return table, dcc.send_data_frame(df.to_csv, "falcon9_launches.csv")

    # Return only the table without download
    return table, None

# Callback to toggle the visibility of the code snippet description
@callback(
    Output("webscraping-data-description", "style"),
    Input("toggle-webscraping-description", "n_clicks"),
    prevent_initial_call=True
)
def toggle_code_snippet_visibility(n_clicks):
    # Toggle visibility based on the click count (even -> hide, odd -> show)
    if n_clicks % 2 == 0:
        return {"display": "none"}
    else:
        return {
            "display": "block",
            "backgroundColor": "#f4f4f4",
            "padding": "10px",
            "borderRadius": "5px",
            "whiteSpace": "pre-wrap",
            "overflowX": "scroll",
        }
    
@callback(
     [
        Output("webscrapin-content", "children"), 
        Output("webscrapin-content", "style"), 
        Output("webscraping-visible", "data")
     ],
     Input("toggle-webscraping-summary", "n_clicks"),
     State("webscraping-visible", "data"),
     prevent_initial_call=True
)
def update_scraping_summary(n_clicks, is_visible):
    # Toggle visibility state
    new_visibility = not is_visible

    if new_visibility:
        code_snippet = """
```python
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Main scraping function
def fetch_falcon_9_launch_data():
     # Wikipedia URL with Falcon 9 and Falcon Heavy launch data
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
        style = {"display": "block"}
    else:
        code_snippet = ""
        style = {"display": "none"}
    return code_snippet, style, new_visibility
