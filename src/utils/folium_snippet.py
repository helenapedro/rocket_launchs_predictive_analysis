from dash import dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

def snippet():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.Button(
                        "View/Hide Code Snippet",
                        id="toggle-folium-button-summary",
                        className="btn btn-primary mb-3",
                    ),
                    dcc.Markdown(id="folium-summary-content", style={"display": "none"}),
                    dcc.Store(id="folium-snippet-visible", data=False), 
                ]
            ),
        ],
        className="mb-4 shadow-sm",
    )

@callback(
     [
        Output("folium-summary-content", "children"), 
        Output("folium-summary-content", "style"), 
        Output("folium-snippet-visible", "data")
     ],
     Input("toggle-folium-button-summary", "n_clicks"),
     State("folium-snippet-visible", "data"),
     prevent_initial_call=True
)
def update_folium_summary(n_clicks, is_visible):
    # Toggle visibility state
    new_visibility = not is_visible

    if new_visibility:
        code_snippet = """
```python
import folium
from folium.plugins import MarkerCluster, HeatMap
from folium.features import DivIcon
from dash import html

def update_map_and_stats(selected_site, selected_status, start_date, end_date, map_type_toggle):
     # Existing code
     ...
            
    # Map generation
    site_info = launch_sites_df[launch_sites_df['Launch Site'] == selected_site].iloc[0]
    site_coordinates = [site_info['Lat'], site_info['Long']]
    site_map = folium.Map(location=site_coordinates, zoom_start=10)

     if 'heatmap' in map_type_toggle:
        # Add heatmap
        heat_data = [[row['Lat'], row['Long']] for _, row in filtered_df.iterrows()]
        HeatMap(heat_data).add_to(site_map)
     else:
           # Add markers
          marker_cluster = MarkerCluster().add_to(site_map)
          for _, record in filtered_df.iterrows():
               coordinate = [record['Lat'], record['Long']]
               marker_color = 'green' if record['class'] == 1 else 'red'

               folium.Marker(
                    coordinate,
                    icon=folium.Icon(color=marker_color),
                    popup=f"Launch Outcome: {'Success' if record['class'] == 1 else 'Failure'}<br>Launch Time: {record['Date']}",
                    tooltip=f"Launch {record['Launch Site']} - {'Success' if record['class'] == 1 else 'Failure'}"
               ).add_to(marker_cluster)

     # Existing code
     ...

    # Render map as HTML
    map_html = site_map._repr_html_()

    return map_html, stats_content
```
    """
        style = {"display": "block"}
    else:
        code_snippet = ""
        style = {"display": "none"}
    return code_snippet, style, new_visibility