import plotly.express as px
from data.loaddata import load_data

df = load_data('spacex_launch_dash.csv')

def get_scatter_chart(entered_site, payload_range):
    print('Params: {} {}'.format(entered_site, payload_range))
    if entered_site == 'ALL':
        filtered_df = df[(df['Payload Mass (kg)'] >= int(payload_range[0])) &
                                (df['Payload Mass (kg)'] <= int(payload_range[1]))
                               ]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='All sites - payload mass between {:8,d}kg and {:8,d}kg'.format(int(payload_range[0]),int(payload_range[1])))
    else:
        filtered_df = df[(df['Launch Site'] == entered_site) & 
                                (df['Payload Mass (kg)'] >= int(payload_range[0])) &
                                (df['Payload Mass (kg)'] <= int(payload_range[1]))
                               ]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Site {} - payload mass between {:8,d}kg and {:8,d}kg'.format(entered_site,int(payload_range[0]),int(payload_range[1])))
    return fig