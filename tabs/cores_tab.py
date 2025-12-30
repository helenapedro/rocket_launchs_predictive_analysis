from dash import dcc
from data.datatable import create_data_table

def cores_tab(cores_df):
     return dcc.Tab(
          label='Cores', 
          children=[
               create_data_table('cores-table', cores_df.columns, cores_df.to_dict('records'))
          ]
     )