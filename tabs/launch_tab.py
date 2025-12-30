from dash import dcc
from data.datatable import create_data_table

def launch_tab(launchpads_df):
     return dcc.Tab(
          label='Launchpads', 
          children=[
               create_data_table('launchpads-table', launchpads_df.columns, launchpads_df.to_dict('records'))
          ]
     )