from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from src.dashboard.scatter import get_scatter_chart
from src.dashboard.pie import get_pie_chart
from src.dashboard.payload import get_payload_range
from src.dashboard.dropdown import dropdown_menu

def create_home_page():
    return dbc.Container([
        dbc.Row([
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.H1(
                            "Launch Records Dashboard", 
                            className="text-center mb-4",
                            style={'color': '#4CAF50'}
                        ),
                    ),
                    # Hero Section
                    html.Div(
                        [
                            html.P(
                                "Explore the performance metrics and payload data of various launch sites. "
                                "Use the filters to customize the view and gain actionable insights.",
                                className='text-center text-muted'
                            ),
                        ],
                        className="hero-section"
                    ),

                    # Dropdown and Slider Row
                    dbc.Row(
                        [
                            dbc.Col([
                                html.Label("Select State:", className='form-label'),
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=dropdown_menu(),
                                    value='ALL',
                                    placeholder="Select State",
                                    searchable=True,
                                    className='form-control',
                                ),
                            ], xs=12, sm=12, md=6, lg=6, xl=6),
                            dbc.Col([
                                html.Label("Payload Range (Kg):", className='form-label'),
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0', 1000: '1000'},
                                    value=get_payload_range(),
                                    className='mb-4 shadow hoverable',
                                ),
                            ], xs=12, sm=12, md=6, lg=6, xl=6),
                        ], className='mb-4 shadow hoverable'
                    ),

                    # Graphs Row
                    dbc.Row([
                        dbc.Col([
                            dbc.Card(
                                dbc.CardBody([
                                    html.H5("Success Rate by Launch Site", className="card-title text-center"),
                                    dcc.Graph(id='success-pie-chart'),
                                ])
                            ),
                        ],  xs=12, sm=12, md=6, lg=6, xl=6),
                        dbc.Col([
                            dbc.Card(
                                dbc.CardBody([
                                    html.H5("Payload vs. Success Rate", className="card-title text-center"),
                                    dcc.Graph(id='success-payload-scatter-chart'),
                                ])
                            ),
                        ],  xs=12, sm=12, md=6, lg=6, xl=6),
                    ]),
                ],
                className="mb-4 shadow"
            ),
        ]),
    ], 
    fluid=True, 
    className="mt-5"
)

# Callbacks
@callback(Output(component_id='success-pie-chart', component_property='figure'),
          Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart_callback(entered_site):    
    fig = get_pie_chart(entered_site)     
    return fig

@callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
          Input(component_id='site-dropdown', component_property='value'), 
          Input(component_id="payload-slider", component_property="value"))
def get_scatter_chart_callback(entered_site, payload_range):
    fig = get_scatter_chart(entered_site, payload_range)
    return fig
