import plotly.express as px
from src.data.loaddata import load_data

df = load_data('spacex_launch_dash.csv')

def get_pie_chart(entered_site):    
    if entered_site == 'ALL':
        fig = px.pie(df, 
                     values='class', 
                     names='Launch Site', 
                     title='Total Success Launches By Site')        
    else:
        filtered_df = df[df['Launch Site'] == entered_site]
        filtered_df = filtered_df.groupby('class').count().reset_index()        
        fig = px.pie(filtered_df, 
                     values='Unnamed: 0', 
                     names='class', 
                     title='Total Launches for site {}'.format(entered_site))        
    return fig