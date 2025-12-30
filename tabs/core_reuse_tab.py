from dash import dcc, html

def cores_reuse_tab(cores_df):
     return dcc.Tab(
          label='Core Reuse Count', 
          children=[
               html.Div(dcc.Graph(
                    id='core-reuse-count',
                    figure={
                         'data': [
                         {
                              'x': cores_df['Core Serial Number'], 
                              'y': cores_df['Times Reused'], 
                              'type': 'bar', 'name': 'Times Reused'
                         }
                         ],
                         'layout': {
                         'title': 'Core Reuse Count',
                         'xaxis': {'title': 'Core Serial Number'},
                         'yaxis': {'title': 'Times Reused'},
                         }
                    }
               )
          )]
     )