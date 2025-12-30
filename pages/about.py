from dash import html
import dash_bootstrap_components as dbc

def create_about_content():
    return dbc.Container(
        [
            # Title Section
            dbc.Card(
                dbc.CardHeader(
                    html.H1("Predictive Analytics for Rocket Launch Costs and Reusability", className="text-center text-primary my-4"),
                    className="bg-light shadow"
                ),
                className="mb-4"
            ),
            
            # Summary Section
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Project Overview",
                                    className="card-title text-secondary mb-3"
                                ),
                                html.P(
                                    """
                                    The project delves into the feasibility of SpaceY entering the rocket 
                                    launch market to rival SpaceX, with a focus on reducing launch costs 
                                    via reusable rocket stages.
                                    """,
                                    className="card-text"
                                ),
                                html.P(
                                    """
                                    This analysis examines critical data, including payload capacities, 
                                    success rates, and cost-effectiveness, to provide actionable insights 
                                    for SpaceY's strategic planning.
                                    """,
                                    className="card-text"
                                ),
                                dbc.Button(
                                    "Learn More",
                                    color="primary",
                                    className="mt-3",
                                    href="/"
                                ),
                            ],
                            id="summary-content-sidebar",
                            className="text-center"
                        ),
                    ],
                    className="shadow p-4"
                ),
                className="mb-4"
            ),
        ],
        fluid=True,
        className="page-content mt-5"
    )
