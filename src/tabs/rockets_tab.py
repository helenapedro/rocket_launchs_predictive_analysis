from dash import dcc
from data.datatable import create_data_table

def rockets_tab(rockets_df):
     return dcc.Tab(
          label='Rockets', 
          children=[
               create_data_table('rockets-table', rockets_df.columns, rockets_df.to_dict('records'))
          ]
     )