from dash import dcc
from data.datatable import create_data_table

def payloads_tab(payloads_df):
     return dcc.Tab(
          label='Payloads', 
          children=[
               create_data_table('payloads-table', payloads_df.columns, payloads_df.to_dict('records'))
          ]
     )