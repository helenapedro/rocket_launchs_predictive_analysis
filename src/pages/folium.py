from dash import dcc, html, Output, Input, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import os

import folium
from folium.plugins import MarkerCluster, HeatMap
from folium.features import DivIcon

from math import sin, cos, sqrt, atan2, radians

# Construct the absolute path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '../data/spacex_launch_geo.csv')

# Load data
spacex_df = pd.read_csv(data_path)
launch_sites_df = spacex_df[['Launch Site', 'Lat', 'Long']].drop_duplicates()

# Date filter: Convert to datetime
spacex_df['Date'] = pd.to_datetime(spacex_df['Date'])

# Distance calculation function using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two latitude-longitude points in kilometers."""
    R = 6373.0  # Approximate radius of Earth in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


layout = dbc.Container(
    [
          # Hero Section
          dbc.Row(
               dbc.Col(
                    dbc.Card(
                         [    dbc.CardHeader([
                                   html.H1(
                                        "SpaceX Launch Sites Interactive Map",
                                        className="text-center",
                                        style={'color': '#4CAF50'}
                                   ),
                              ]),

                              # Hero Section
                              html.Div(
                                   [
                                        html.P(
                                             "Explore SpaceX launch sites, analyze past launches, and visualize successes and failures on an interactive map. "
                                             "Use filters to customize your view and gain insights into SpaceX's incredible achievements.",
                                             className="text-center text-muted",
                                             style={"font-size": "18px"}
                                        )
                                   ],
                                   className="hero-section"
                              ),

                              dbc.CardBody([

                                   dbc.Button(
                                   "View/Hide Code Snippet",
                                   id="toggle-folium-button-summary",
                                   className="btn btn-primary mb-3",
                                   ),
                                   dcc.Markdown(id="folium-summary-content", style={"display": "none"}),
                                   dcc.Store(id="folium-snippet-visible", data=False)
                              ])

                         ], className="mb-4 shadow"
                    )
               )
          ),

          # Filters and Statistics
          dbc.Row([
                    dbc.Col([
                         dbc.Card([
                              dbc.CardBody([
                                   html.Label("Select a launch site:", id="launch-site-label"),
                                   dcc.Dropdown(
                                        id='launch-site-dropdown',
                                        options=[{'label': site, 'value': site} for site in launch_sites_df['Launch Site']],
                                        value=launch_sites_df['Launch Site'].iloc[0],
                                        placeholder="Select a Launch Site",
                                        className="mb-2"
                                   ),
                                   dbc.Tooltip("Select a SpaceX launch site to filter launches.", target="launch-site-label"),
                                   dcc.Checklist(
                                        id='launch-success-filter',
                                        options=[
                                             {'label': 'Success', 'value': 1},
                                             {'label': 'Failure', 'value': 0}
                                        ],
                                        value=[1, 0],
                                        inline=True,
                                        style={'margin-bottom': '20px'}
                                   ),
                                   dcc.DatePickerRange(
                                        id='date-range-picker',
                                        start_date=spacex_df['Date'].min().date(),
                                        end_date=spacex_df['Date'].max().date(),
                                        display_format='YYYY-MM-DD',
                                        style={'width': '100%'}
                                   ),

                                   dcc.Checklist(
                                        id='map-type-toggle',
                                        options=[{'label': 'Show Heatmap', 'value': 'heatmap'}],
                                        value=[]
                                   )

                              ])
                         ], className="mb-4 shadow-lg hoverable")
                    ], 
                    xs=12, sm=12, md=6, lg=6, xl=6
               ),

               dbc.Col(
                   [
                         dbc.Card([
                              dbc.CardBody([
                              html.Div(id='launch-stats', className="stats-container"),
                              ])
                         ], className="mb-4 shadow-sm")
                    ], 
                    xs=12, sm=12, md=6, lg=6, xl=6
               )
          ]),

          # Map Section
          dbc.Row([
               dbc.Col(
                   [
                         dbc.Card([
                              dbc.CardBody([
                                   html.Iframe(
                                        id='launch-map',
                                        width='100%',
                                        height='800',
                                        style={'border': 'none'}
                                   )
                              ])
                         ], className="mb-4 shadow-lg hoverable")
                    ],
               )
          ])
    ],
    fluid=True,
    className="mt-5"
)

@callback(
    [
        Output('launch-map', 'srcDoc'),
        Output('launch-stats', 'children')
    ],
    [
        Input('launch-site-dropdown', 'value'),
        Input('launch-success-filter', 'value'),
        Input('date-range-picker', 'start_date'),
        Input('date-range-picker', 'end_date'),
        Input('map-type-toggle', 'value') 
    ]
)
def update_map_and_stats(selected_site, selected_status, start_date, end_date, map_type_toggle):
    # Ensure the selected site is valid
    if selected_site not in launch_sites_df['Launch Site'].values:
        error_message = html.Div(
            "No valid site selected. Please select a valid launch site.",
            style={'color': 'red'}
        )
        return "", error_message

    # Validate date range
    if pd.to_datetime(start_date) > pd.to_datetime(end_date):
        error_message = html.Div(
            "Invalid date range. The start date must be earlier than the end date.",
            style={'color': 'red'}
        )
        return "", error_message

    # Filter data based on inputs
    filtered_df = spacex_df[
        (spacex_df['Launch Site'] == selected_site) &
        (spacex_df['class'].isin(selected_status)) &
        (spacex_df['Date'] >= start_date) &
        (spacex_df['Date'] <= end_date)
    ]

    if filtered_df.empty:
        error_message = html.Div(
            f"No launches found for {selected_site} with the selected filters.",
            style={'color': 'red'}
        )
        return "", error_message

    # Map generation
    site_info = launch_sites_df[launch_sites_df['Launch Site'] == selected_site].iloc[0]
    site_coordinates = [site_info['Lat'], site_info['Long']]
    site_map = folium.Map(location=site_coordinates, zoom_start=10)

    if 'heatmap' in map_type_toggle:
        # Add heatmap
        heat_data = [[row['Lat'], row['Long']] for _, row in filtered_df.iterrows()]
        HeatMap(heat_data).add_to(site_map)
    else:
        # Add markers
        marker_cluster = MarkerCluster().add_to(site_map)
        for _, record in filtered_df.iterrows():
            coordinate = [record['Lat'], record['Long']]
            marker_color = 'green' if record['class'] == 1 else 'red'

            folium.Marker(
                coordinate,
                icon=folium.Icon(color=marker_color),
                popup=f"Launch Outcome: {'Success' if record['class'] == 1 else 'Failure'}<br>Launch Time: {record['Date']}",
                tooltip=f"Launch {record['Launch Site']} - {'Success' if record['class'] == 1 else 'Failure'}"
            ).add_to(marker_cluster)

    # Add main launch site marker
    folium.Marker(
        site_coordinates,
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 12px; color: #d35400;"><b>{selected_site}</b></div>'
        ),
        popup=f"Launch Site: {selected_site}"
    ).add_to(site_map)

    # Calculate statistics
    total_launches = len(filtered_df)
    successful_launches = filtered_df['class'].sum()
    success_rate = (successful_launches / total_launches * 100) if total_launches > 0 else 0

    stats_content = html.Div([
        html.H4(f"Launch Statistics for {selected_site}:"),
        html.P(f"Total Launches: {total_launches}"),
        html.P(f"Successful Launches: {successful_launches}"),
        html.P(f"Success Rate: {success_rate:.2f}%")
    ])

    # Render map as HTML
    map_html = site_map._repr_html_()

    return map_html, stats_content

@callback(
     [
        Output("folium-summary-content", "children"), 
        Output("folium-summary-content", "style"), 
        Output("folium-snippet-visible", "data")
     ],
     Input("toggle-folium-button-summary", "n_clicks"),
     State("folium-snippet-visible", "data"),
     prevent_initial_call=True
)
def update_folium_summary(n_clicks, is_visible):
    # Toggle visibility state
    new_visibility = not is_visible

    if new_visibility:
        code_snippet = """
```python
import folium
from folium.plugins import MarkerCluster, HeatMap
from folium.features import DivIcon
from dash import html

def update_map_and_stats(selected_site, selected_status, start_date, end_date, map_type_toggle):
     # Existing code
     ...
            
    # Map generation
    site_info = launch_sites_df[launch_sites_df['Launch Site'] == selected_site].iloc[0]
    site_coordinates = [site_info['Lat'], site_info['Long']]
    site_map = folium.Map(location=site_coordinates, zoom_start=10)

     if 'heatmap' in map_type_toggle:
        # Add heatmap
        heat_data = [[row['Lat'], row['Long']] for _, row in filtered_df.iterrows()]
        HeatMap(heat_data).add_to(site_map)
     else:
           # Add markers
          marker_cluster = MarkerCluster().add_to(site_map)
          for _, record in filtered_df.iterrows():
               coordinate = [record['Lat'], record['Long']]
               marker_color = 'green' if record['class'] == 1 else 'red'

               folium.Marker(
                    coordinate,
                    icon=folium.Icon(color=marker_color),
                    popup=f"Launch Outcome: {'Success' if record['class'] == 1 else 'Failure'}<br>Launch Time: {record['Date']}",
                    tooltip=f"Launch {record['Launch Site']} - {'Success' if record['class'] == 1 else 'Failure'}"
               ).add_to(marker_cluster)

     # Existing code
     ...

    # Render map as HTML
    map_html = site_map._repr_html_()

    return map_html, stats_content
```
    """
        style = {"display": "block"}
    else:
        code_snippet = ""
        style = {"display": "none"}
    return code_snippet, style, new_visibility