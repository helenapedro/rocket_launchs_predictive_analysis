from dash import html, dash_table, dcc, Output, Input, State, callback
import dash_bootstrap_components as dbc
from data.data_fetch import fetch_initial_data

# Fetch and process the data
dataframe = fetch_initial_data()

def fetch_initial_data_layout():
    if dataframe.empty:
        return html.Div("No data available to display", style={"textAlign": "center", "padding": "20px"})

    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    [
                        dbc.Button(
                            "View Code Snippet",
                            id="toggle-button-initial",
                            className="btn btn-primary mb-3"
                        ),
                        dbc.Collapse(
                            dcc.Markdown(id="code-snippet-div"),
                            id="collapse-snippet",
                            is_open=False,
                        ),
                    ]
                )
            ),
            dbc.Row(
                dbc.Col(
                    dash_table.DataTable(
                        id='spacex-data-table',
                        columns=[{"name": col, "id": col} for col in dataframe.columns],
                        data=dataframe.to_dict('records'),
                        page_size=5,
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'textAlign': 'left',
                            'padding': '10px',
                            'whiteSpace': 'normal',
                        },
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        },
                        style_data={
                            'backgroundColor': 'rgb(250, 250, 250)',
                        },
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
                        ],
                    ),
                    className="mb-4"
                )
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Data Enrichment Observations", className="card-title"),
                                html.P(
                                    """
                                    From the initial data, many columns only contain ID numbers without context. 
                                    To enrich this dataset, we used the SpaceX API to retrieve detailed information 
                                    about rockets, payloads, launchpads, and cores.
                                    """,
                                    className='text-muted'
                                ),
                            ]
                        ),
                        className="mb-4"
                    )
                )
            ),
            dbc.Row(
                dbc.Col(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItem([
                                html.I(className="bi bi-rocket-fill me-2 text-primary"),
                                html.Span("Rocket: "),
                                "Retrieve the booster name."
                            ]),
                            dbc.ListGroupItem([
                                html.I(className="bi bi-box2-fill me-2 text-success"),
                                html.Span("Payload: "),
                                "Obtain the mass of the payload and the orbit it will enter."
                            ]),
                            dbc.ListGroupItem([
                                html.I(className="bi bi-geo-alt-fill me-2 text-danger"),
                                html.Span("Launchpad: "),
                                "Identify the name of the launch site, as well as its longitude and latitude."
                            ]),
                            dbc.ListGroupItem([
                                html.I(className="bi bi-cpu-fill me-2 text-warning"),
                                html.Span("Cores: "),
                                """
                                Gather detailed information including the landing outcome, landing type, 
                                number of flights for that core, usage of grid fins, whether the core is reused, 
                                presence of legs, the landing pad used, the block version, reuse count, 
                                and the serial number of the core.
                                """
                            ])
                        ]
                    )
                )
            ),
        ],
        fluid=True
    )

# Define the callback with dynamic button text
@callback(
    [Output("code-snippet-div", "children"), Output("collapse-snippet", "is_open"), Output("toggle-button-initial", "children")],
    Input("toggle-button-initial", "n_clicks"),
    State("collapse-snippet", "is_open"),
    prevent_initial_call=True
)
def update_initial_data(n_clicks, is_open):
    if n_clicks:
        code_snippet = """
```python
import pandas as pd
from utils.data import fetch_data_from_api

def fetch_table():
    data = fetch_data_from_api()
    if data:
        df = pd.DataFrame(data)

        df = df.map(
            lambda x: str(x) if not isinstance(x, (str, int, float, bool, type(None))) else x
        )

        pd.set_option('display.max_columns', None)
        return df
    else:
        return pd.DataFrame()
```
    """
        new_button_text = "Hide Code Snippet" if not is_open else "View Code Snippet"
        return code_snippet, not is_open, new_button_text
    return "", is_open, "View Code Snippet"