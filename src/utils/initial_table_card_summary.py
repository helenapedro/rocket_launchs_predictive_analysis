from dash import html
import dash_bootstrap_components as dbc
from utils.processed_data_description import create_processed_data_description

def initial_table_card_summary():
     return dbc.Card(
          [
               dbc.CardBody(
                    [
                         create_processed_data_description(),

                    ]
               ),
          ]
     )