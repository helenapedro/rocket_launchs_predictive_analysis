from data.loaddata import load_data

df = load_data('spacex_launch_dash.csv')

def get_payload_range():
    min_payload = df['Payload Mass (kg)'].min()
    max_payload = df['Payload Mass (kg)'].max()
    return [min_payload, max_payload]