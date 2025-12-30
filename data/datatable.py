from dash import dash_table

# Create reusable DataTable component
def create_data_table(id, columns, data):
    return dash_table.DataTable(
        id=id,
        columns=[{"name": col, "id": col} for col in columns],
        data=data,
        style_table=style_table,
        style_cell=style_cell,
        style_header=style_header,
    )

# Prepare style dictionaries for DataTable consistency
style_table = {'overflowX': 'scroll'}
style_cell = {
    'textAlign': 'left',
    'minWidth': '150px',
    'width': 'auto',
    'maxWidth': '300px',
    'whiteSpace': 'normal',
    'padding': '10px',
}
style_header = {
    'textAlign': 'center',
    'backgroundColor': '#f1f1f1',
    'fontWeight': 'bold',
    'minWidth': '150px',
    'width': 'auto',
    'maxWidth': '300px',
    'padding': '10px',
}
