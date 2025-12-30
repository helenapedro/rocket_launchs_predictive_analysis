from dash import html
import dash_bootstrap_components as dbc

def create_webscraping_summary():
    return dbc.Container(
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("Web Scraping Summary", className="text-center")),
                        dbc.CardBody(
                            [
                                html.H4("Process", className="card-title mt-4"),
                                html.P(
                                    "The web scraping process involved accessing Wikipedia's 'List of Falcon 9 and Falcon Heavy launches' page to extract historical launch data. "
                                    "Using BeautifulSoup, the HTML table was parsed, cleaned, and formatted into a Pandas DataFrame for further analysis.",
                                    className="card-text",
                                ),
                                html.H4("Outcome", className="card-title mt-4"),
                                html.P(
                                    "Successfully gathered Falcon 9 launch records into a structured format, enabling exploratory data analysis and visualization. ",
                                    className="card-text",
                                ),
                            ]
                        ),
                    ],
                    className="mb-4 shadow-lg",
                ),
                width=10,
                className="mx-auto",
            )
        ),
        className="mt-5",
    )
