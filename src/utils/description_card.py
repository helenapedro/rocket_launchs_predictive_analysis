from dash import html
import dash_bootstrap_components as dbc
from dash.dcc import Markdown

def create_description_card(button_id, button_text, description_text, code_snippet, card_id):
    # Ensure code_snippet is either a string or a Dash component
    if not isinstance(code_snippet, (str, Markdown)):
        code_snippet = str(code_snippet)  # Convert to string if not already

    return dbc.Col(
        [
            html.Button(
                button_text, 
                id=button_id, 
                n_clicks=0,
                className="btn btn-primary mb-3"
            ),
            dbc.Col(
                [
                    html.H3(description_text, className="text-start"),
                    html.Pre(
                        code_snippet,
                        id=card_id,
                        style={
                            "display": "none",  # Initially hidden
                            "backgroundColor": "#f4f4f4",
                            "padding": "10px",
                            "borderRadius": "5px",
                            "whiteSpace": "pre-wrap",
                            "overflowX": "scroll",
                        },
                        className="pre-scrollable",
                    ),
                ],
                style={"marginBottom": "20px"},
                className="card p-3",
            ),
        ],
        className="container mt-5",
    )
