import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)

# Read the automobiles data into pandas dataframe
auto_data = pd.read_csv('automobileEDA.csv', encoding="ISO-8859-1")

# Layout Section of Dash
app.layout = html.Div(children=[
    html.H1('Car Automobile Components', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    
    html.Div([
        html.Div(html.H2('Drive Wheels Type:', style={'margin-right': '2em'})),
        
        dcc.Dropdown(
            id='demo-dropdown',
            options=[
                {'label': 'Rear Wheel Drive', 'value': 'rwd'},
                {'label': 'Front Wheel Drive', 'value': 'fwd'},
                {'label': 'Four Wheel Drive', 'value': '4wd'},
            ],
            value='rwd'
        ),
        
        html.Div([
            html.Div(dcc.Graph(id='plot1')),
            html.Div(dcc.Graph(id='plot2'))
        ], style={'display': 'flex'}),
    ])
])

# Callback to update charts based on dropdown value
@app.callback(
    [Output(component_id='plot1', component_property='figure'),
     Output(component_id='plot2', component_property='figure')],
    Input(component_id='demo-dropdown', component_property='value')
)
def display_selected_drive_charts(value):
    # Filter the DataFrame based on the selected drive wheels
    filtered_df = auto_data[auto_data['drive-wheels'] == value]
    
    # Handle NaN values in the 'price' column
    filtered_df = filtered_df[filtered_df['price'].notna()]
    
    # Group by 'drive-wheels' and 'body-style', calculating the mean price
    grouped_df = filtered_df.groupby(['drive-wheels', 'body-style'], as_index=False)['price'].mean().reset_index()
    
    # Create figures
    fig1 = px.pie(grouped_df, values='price', names='body-style', title="Pie Chart")
    fig2 = px.bar(grouped_df, x='body-style', y='price', title='Bar Chart')
    
    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)
