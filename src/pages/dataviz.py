import os
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.queries import (
    fetch_unique_launch_sites,      
    fetch_launch_count, 
    fetch_payload_mass_by_customer,
    fetch_avg_payload_mass_by_booster,
    fetch_mission_outcomes,
    fetch_failed_landings
)

# Construct the absolute path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '../data/dataset_part_2.csv')

# Load the dataset
df = pd.read_csv(data_path)

def create_section(title, graph_id, description, conclusions):
    return dbc.Row([
        dbc.Col([
            html.H2(title),
            dcc.Graph(id=graph_id),
            html.Div([
                html.P(description),
                html.Ul([html.Li(conclusion) for conclusion in conclusions])
            ])
        ], xs=12, sm=12, md=12, lg=6)
    ], className="justify-content-center")

# Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Exploratory Data Analysis and Feature Engineering", className="text-center text-primary mb-4"), width=12)
    ]),

    create_section(
        "Relationship between Payload and Flight Number",
        'payload-flight-graph',
        "As the flight number increases, the first stage is more likely to land successfully. The payload mass is also important; it seems the more massive the payload, the less likely the first stage will return.",
        []
    ),

    create_section(
        "Relationship between Launch Site and Flight Number",
        'launchsite-flight-graph',
        "From the plot above it can be concluded that:",
        [
            "CCAFS SLC 40 is the most common launch site.",
            "The larger the flight amount at a launch site, the greater the success rate at a launch site.",
            "Launches have a 66.6% success rate."
        ]
    ),

    create_section(
        "Relationship between Payload and Launch Site",
        'payload-launchsite-graph',
        "From the plot above it can be concluded that:",
        [
            "VAFB-SLC does not launch any heavy payloads.",
            "The higher success rate was for the rockets.",
            "The greater the payload mass was for a launch site CCAFS SLC 40.",
            "Most launches with payload mass under 10,000 kg are from any launch site, but heavier ones happen mainly at CCAFS SLC 40 and KSC LC 39A."
        ]
    ),

    create_section(
        "Success Rate by Orbit Type",
        'orbit-success-graph',
        "From the plot above it can be concluded that:",
        [
            "GEO, HEO, SSO, VLEO, and ES-L1 had the most success rate by mean."
        ]
    ),

    create_section(
        "Relationship between Flight Number and Orbit Type",
        'flight-orbit-graph',
        "From the plot above it can be concluded that:",
        [
            "LEO orbit success apparently is correlated to the number of flights.",
            "There is no relationship for GTO orbit."
        ]
    ),

    create_section(
        "Relationship between Payload and Orbit Type",
        'payload-orbit-graph',
        "From the plot above it can be concluded that:",
        [
            "There are successfully heavy payloads for the Polar, LEO, and ISS.",
            "Heavy payloads have a negative influence on GTO orbits and positive on GTO and Polar LEO (ISS) orbits."
        ]
    ),

    create_section(
        "Launch Success Yearly Trend",
        'yearly-trend-graph',
        "From the line chart above it can be seen that:",
        [
            "There is a significant improvement since 2014 and it was increasing until 2020."
        ]
    ),

    # EDA With SQL
    dbc.Row([
        dbc.Col(html.H1("EDA with SQL", className="text-center text-primary mb-4"), 
                width=12
        )
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.Div([
                         html.I(className="fas fa-info-circle me-2"),
                         "Summary",
                    ], className="bg-secondary text-white"),
                ),    
                dbc.CardBody([
                        html.P("This section allows you to explore SpaceX launch data through interactive SQL queries."),
                        html.Ul([
                            html.Li("View unique launch sites."),
                            html.Li("Fetch the launch count for a specific site."),
                            html.Li("Analyze payload mass by customer."),
                            html.Li("Examine mission outcomes."),
                            html.Li("Identify failed landing outcomes on drone ships."),
                        ]),
                        html.P("The backend is powered by MySQL, and SQL queries are executed dynamically to provide the latest insights.")
                ]),
            ], className="mb-4 shadow-lg")
        ], xs=12, sm=12, md=12, lg=8),
    ], className="justify-content-center"),

    # Query Sections
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.I(className="fas fa-map-marker-alt me-2"),
                        "Unique Launch Sites"
                    ], className="d-flex align-items-center bg-primary text-white")
                ),
                dbc.CardBody([
                    html.Div(id="launch-site-list", className="list-group")
                ])
            ], className="mb-4 shadow-lg hoverable")
        ], xs=12, sm=12, md=6, lg=4),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.I(className="fas fa-rocket me-2"),
                        "Launch Count"
                    ], className="d-flex align-items-center bg-success text-white")
                ),
                dbc.CardBody([
                    dbc.Input(id="site-input", type="text", placeholder="Enter Launch Site", className="mb-2"),
                    dbc.Button("Get Count", id="count-btn", color="primary", className="mb-2"),
                    html.Div(id="launch-count-output", className="text-muted")
                ])
            ], className="mb-4 shadow-lg hoverable")
        ], xs=12, sm=12, md=6, lg=4),    
    ], className="justify-content-center"),
    
], fluid=True)

# Callbacks
@callback(
    Output('payload-flight-graph', 'figure'),
    Output('launchsite-flight-graph', 'figure'),
    Output('payload-launchsite-graph', 'figure'),
    Output('orbit-success-graph', 'figure'),
    Output('flight-orbit-graph', 'figure'),
    Output('payload-orbit-graph', 'figure'),
    Output('yearly-trend-graph', 'figure'),
    Input('payload-flight-graph', 'id')
)
def update_graphs(_):
    # Relationship between Payload and Flight Number
    fig1 = px.scatter(df, x="FlightNumber", y="PayloadMass", color="Class", title="Relationship between Payload and Flight Number")

    # Relationship between Launch Site and Flight Number
    fig2 = px.scatter(df, x="FlightNumber", y="LaunchSite", color="Class", title="Relationship between Launch Site and Flight Number")

    # Relationship between Payload and Launch Site
    fig3 = px.scatter(df, x="PayloadMass", y="LaunchSite", color="Class", title="Relationship between Payload and Launch Site")

    # Success Rate by Orbit Type
    orbit_success = df.groupby('Orbit')['Class'].mean().reset_index()
    fig4 = px.bar(orbit_success, x='Orbit', y='Class', title='Success Rate by Orbit Type')

    # Relationship between Flight Number and Orbit Type
    fig5 = px.scatter(df, x="FlightNumber", y="Orbit", color="Class", title="Relationship between Flight Number and Orbit Type")

    # Relationship between Payload and Orbit Type
    fig6 = px.scatter(df, x="PayloadMass", y="Orbit", color="Class", title="Relationship between Payload and Orbit Type")

    # Launch Success Yearly Trend
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    yearly_trend = df.groupby('Year')['Class'].mean().reset_index()
    fig7 = px.line(yearly_trend, x='Year', y='Class', title='Launch Success Yearly Trend')

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7


""" @callback(
    Output("launch-site-list", "children"),
    Input("launch-site-list", "id")
)
def update_launch_sites(_):
    sites = fetch_unique_launch_sites()
    return [html.Li(site, className="list-group-item") for site in sites]

@callback(
    Output("launch-count-output", "children"),
    Input("count-btn", "n_clicks"),
    State("site-input", "value")
)
def update_launch_count(n_clicks, site):
    if n_clicks and site:
        count = fetch_launch_count(site)
        return f"Launch count for {site}: {count}"
    return "Enter a site and click Get Count" """