from dash import dcc, html

def payload_mass_distribution_tab(payloads_df):
     return dcc.Tab(
          label='Payload Mass Distribution', 
          children=[
               html.Div(dcc.Graph(
                    id='payload-mass-distribution',
                    figure={
                         'data': [
                         {
                              'x': payloads_df['name'], 
                              'y': payloads_df['mass_kg'], 
                              'type': 'bar', 
                              'name': 'Mass (kg)'
                         }
                         ],
                         'layout': {
                         'title': {'text': 'Payload Mass Distribution', 'x': 0.5},
                         'xaxis': {'title': 'Payload Name', 'automargin': True},
                         'yaxis': {'title': 'Mass (kg)', 'automargin': True},
                         'template': 'plotly_dark',
                         }
                    }
               )
          ),]
     )