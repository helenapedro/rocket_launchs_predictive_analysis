from dash import Dash, html, dcc, Input, Output, State
import dash
import dash_bootstrap_components as dbc
from src.sidebar import create_navibar
from pages.about import create_about_content
from pages.webscraping import layout as scraping_layout
from pages.eda import layout as eda_layout 
from pages.folium import layout as folium_layout

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css", 
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
    ]
)

server = app.server

app.config.suppress_callback_exceptions = True

# App Layout
app.layout = html.Div(
    [
        create_navibar(),
        dcc.Location(id="url"), 
        html.Div(id="page-content", className="content"),
        html.Div(
            [
                create_about_content(),
                dbc.Button(
                    "Close", 
                    id="close-sidebar", 
                    className="btn btn-danger mt-3",
                ),
            ],
            id="about-sidebar",
            className="sidebar bg-light border-left p-3",
            style={
                "position": "fixed",
                "top": 0,
                "left": "-320px",
                "bottom": 0,
                "width": "320px",
                "padding": "2rem 1rem",
                "overflow": "auto",
                "transition": "left 0.4s ease-in-out",
            }
        ),
    ],
    className="main-container",
)

# Callback to toggle the navbar
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Callback to toggle the sidebar visibility
@app.callback(
    Output("about-sidebar", "style"),
    [Input("about-link", "n_clicks"), Input("close-sidebar", "n_clicks")],
    State("about-sidebar", "style"),
)
def handle_sidebar(about_n, close_n, style):
    from dash import callback_context
    
    ctx = callback_context
    if not ctx.triggered:
        return style
    
    # Identify triggered input
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if triggered_id == "about-link":
        style["left"] = "0px"  # Show sidebar
    elif triggered_id == "close-sidebar":
        style["left"] = "-320px"  # Hide sidebar
    return style

# Unified callback for toggle buttons
@app.callback(
    Output("processed-data-content", "style"),
    [Input("toggle-processed-summary", "n_clicks")],
    [State("processed-data-content", "style")],
)
def toggle_summaries(toggle_processed_n, processed_style):
    # Initialize style if None (first load)
    processed_style = processed_style or {"display": "none"}

    # Toggle logic for the button
    if toggle_processed_n and toggle_processed_n % 2 == 1:
        processed_style["display"] = "block"  # Show content
    else:
        processed_style["display"] = "none"  # Hide content

    return processed_style

# Page Navigation
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/":
        return eda_layout
    elif pathname == "/scraping":
        return scraping_layout
    elif pathname == "/folium":
        return folium_layout
    elif pathname == "/about":
        return create_about_content()
    else:
        return html.H1("404: Page Not Found", className="error")

if __name__ == "__main__":
    app.run_server(debug=True)
