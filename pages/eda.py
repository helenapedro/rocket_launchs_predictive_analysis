import os
from dash import html
import dash_bootstrap_components as dbc

from pages.home import create_home_page
from pages.data_exploration import create_exploration_page
from components.EdaSql import eda_cards
from components.EdaGraphsSection import eda_graphs

layout = dbc.Container(
    [
        create_home_page(),

        # Visualization Section
        dbc.Row(
            [
                dbc.Col([
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H1(
                                    "EDA with Data Visualization", 
                                    className="text-center mb-4",
                                    style={'color': '#4CAF50'}
                                ),
                            ),

                            eda_graphs,    
                        ],
                        className="mb-4 shadow"
                    ),
                ]
            ),

            eda_cards
        ]),

        create_exploration_page(),

        # Footer
        html.Footer(
            "@2021, Helena Pedro",
            className='text-center text-muted mt-5',
        ),

    ], 
    fluid=True,
    className="mt-5"
)