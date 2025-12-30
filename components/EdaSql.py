from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from utils.queries import (
    fetch_unique_launch_sites, 
    fetch_launch_count, 
    fetch_payload_mass_by_customer,
    fetch_avg_payload_mass_by_booster,
    fetch_mission_outcomes,
    fetch_failed_landings
)

def create_card(header_icon, header_text, body_content, header_bg_class="bg-primary"):
    """Reusable function to create a Bootstrap card."""
    return dbc.Card(
        [
            dbc.CardHeader(
                html.Div(
                    [
                        html.I(className=f"fas {header_icon} me-2"),
                        header_text
                    ],
                    className=f"d-flex align-items-center {header_bg_class} text-white"
                )
            ),
            dbc.CardBody(body_content)
        ],
        className="mb-4 shadow-lg hoverable"
    )

eda_cards = dbc.Col(
    [
        # EDA with SQL Queries Card
        dbc.Card(
            [
                dbc.CardHeader(
                    html.H1(
                        "EDA with SQL Queries",
                        className="text-center mb-4",
                        style={'color': '#4CAF50'}
                    )
                ),
                dbc.CardBody(
                    [
                        html.P(
                            "Explore SpaceX data interactively using SQL queries. "
                            "Fetch insights dynamically powered by MySQL.",
                            className="mb-4"
                        ),
                        html.Ul(
                            [
                                html.Li("View unique launch sites."),
                                html.Li("Fetch launch counts by site."),
                                html.Li("Analyze payload mass by customer."),
                                html.Li("Examine mission outcomes."),
                                html.Li("Identify failed landing outcomes on drone ships.")
                            ]
                        ),
                        dbc.CardFooter(
                            dbc.Button(
                                "Show/Hide Code Snippets",
                                id="toggle-code-btn",
                                color="secondary",
                                className="w-100"
                            )
                        ),
                        dbc.Collapse(
                            dbc.CardBody(dcc.Markdown()),
                            id="code-output"
                        )
                    ]
                )
            ],
            className="mb-4 shadow"
        ),

        # Cards for each query
        create_card(
            header_icon="fa-map-marker-alt",
            header_text="Unique Launch Sites",
            body_content=html.Div(id="launch-site-list", className="list-group")
        ),
        create_card(
            header_icon="fa-rocket",
            header_text="Launch Count",
            body_content=[
                dbc.Input(id="site-input", type="text", placeholder="Enter Launch Site", className="mb-2"),
                dbc.Button("Get Count", id="count-btn", color="primary", className="mb-2"),
                html.Div(id="launch-count-output", className="text-muted")
            ],
            header_bg_class="bg-success"
        ),
        create_card(
            header_icon="fa-clipboard-check",
            header_text="Mission Outcomes",
            body_content=dbc.Spinner(html.Div(id="mission-outcomes-output", className="text-muted")),
            header_bg_class="bg-warning"
        ),
        create_card(
            header_icon="fa-weight-hanging",
            header_text="Payload Mass by Customer",
            body_content=[
                dcc.Dropdown(
                    id="customer-dropdown",
                    options=[
                        {"label": "NASA (CRS)", "value": "NASA (CRS)"},
                        {"label": "SES", "value": "SES"}
                    ],
                    placeholder="Select a Customer",
                    className="mb-2"
                ),
                dbc.Spinner(html.Div(id="payload-mass-output", className="text-muted"))
            ],
            header_bg_class="bg-info"
        ),
        create_card(
            header_icon="fa-weight-hanging",
            header_text="Average Payload Mass",
            body_content=dbc.Spinner(html.Div(id="avg-payload-mass-output", className="text-muted")),
            header_bg_class="bg-secondary"
        ),
        create_card(
            header_icon="fa-times-circle",
            header_text="Failed Landing Outcomes",
            body_content=dbc.Spinner(html.Div(id="failed-landings-output", className="text-muted")),
            header_bg_class="bg-danger"
        )
    ],
    xs=12, sm=12, md=6, lg=4
)

@callback(
    [Output("code-output", "children"), Output("code-output", "style")],
    [Input("toggle-code-btn", "n_clicks")],
)
def toggle_code(n_clicks):
    if n_clicks:
        if n_clicks % 2 == 1:
            code_snippets = """
```python
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection function
def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    
# Fetch Unique Launch Sites
def fetch_unique_launch_sites():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT LAUNCH_SITE FROM SPACEXTBL")
    rows = cursor.fetchall()
    connection.close()
    return [row[0] for row in rows]

# Fetch Launch Count
def fetch_launch_count(launch_site):
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM SPACEXTBL WHERE LAUNCH_SITE = %s"
    cursor.execute(query, (launch_site,))
    result = cursor.fetchone()[0]
    connection.close()
    return result
```
            """
            return dcc.Markdown(code_snippets), {"display": "block"}
        else:
            return "", {"display": "none"}
    return "", {"display": "none"}

@callback(
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
    return "Enter a site and click Get Count"

@callback(
    Output("mission-outcomes-output", "children"),
    Input("mission-outcomes-output", "id")
)
def update_mission_outcomes(_):
    outcomes = fetch_mission_outcomes()
    return [html.P(f"{outcome[0]}: {outcome[1]}") for outcome in outcomes]

@callback(
    Output("payload-mass-output", "children"),
    Input("customer-dropdown", "value")
)
def update_payload_mass(customer):
    if customer:
        total_mass = fetch_payload_mass_by_customer(customer)
        return f"Total Payload Mass for {customer}: {total_mass} kg"
    return "Select a customer to see total payload mass"

@callback(
    Output("avg-payload-mass-output", "children"),
    Input("avg-payload-mass-output", "id")
)
def update_avg_payload_mass(_):
    avg_mass = fetch_avg_payload_mass_by_booster("F9 v1.1%")
    return f"Average Payload Mass for Booster Version F9 v1.1: {avg_mass} kg"

@callback(
    Output("failed-landings-output", "children"),
    Input("failed-landings-output", "id")
)
def update_failed_landings(_):
    landings = fetch_failed_landings()
    return [html.P(f"Landing Outcome: {landing[0]}, Booster Version: {landing[1]}, Launch Site: {landing[2]}") for landing in landings]

