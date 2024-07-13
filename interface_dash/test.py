import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(style={'padding': 50}, children=[
    html.H1('Dash Plot Animation Example'),

    # Add a button
    html.Button('Click Me', id='button', n_clicks=0),

    # Add a checkbox
    dcc.Checklist(
        id='checklist',
        options=[
            {'label': 'Option 1', 'value': '1'},
            {'label': 'Option 2', 'value': '2'}
        ],
        value=['1']
    ),

    # Add an interval component for animation
    dcc.Interval(
        id='interval-component',
        interval=50,  # in milliseconds
        n_intervals=0  # number of times the interval has triggered
    ),

    # Add a plot
    dcc.Graph(id='graph')
])

# Define callback to update graph based on button clicks, checklist selection, and interval triggers


@app.callback(
    Output('graph', 'figure'),
    [Input('button', 'n_clicks'), Input('checklist', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_graph(n_clicks, checklist_values, n_intervals):
    x_data = np.linspace(0, 10, 100)  # X-axis data
    y_data = np.sin(x_data + 0.1 * n_intervals)  # Animated Y-axis data

    trace = go.Scatter(x=x_data, y=y_data,
                       mode='lines+markers', name='Animated Line Plot')

    layout = go.Layout(
        title='Procedural Animation Plot',
        xaxis={'title': 'X Axis'},
        yaxis={'title': 'Y Axis'}
    )

    figure = go.Figure(data=[trace], layout=layout)
    return figure


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
