import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px

# List of years 
year_list = [i for i in range(2005, 2021, 1)]

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})


def compute_info_1(airline_data, entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)][['Year', 'Month', 
                                                      'Reporting_Airline', 
                                                      'CarrierDelay', 
                                                      'WeatherDelay', 
                                                      'NASDelay',
                                                      'SecurityDelay',
                                                      'LateAircraftDelay']]
    df.rename(columns={'CarrierDelay': 'CarrierDelayAvg', 
                   'WeatherDelay': 'WeatherDelayAvg', 
                   'NASDelay': 'NASDelayAvg', 
                   'SecurityDelay': 'SecurityDelayAvg', 
                   'LateAircraftDelay': 'LateAircraftDelayAvg'}, inplace=True)
    df.fillna(0, inplace=True)
    CarrierDelay_df = df.groupby(['Month','Reporting_Airline'])['CarrierDelayAvg'].mean().reset_index()
    WeatherDelay_df = df.groupby(['Month','Reporting_Airline'])['WeatherDelayAvg'].mean().reset_index()
    NASDelay_df = df.groupby(['Month','Reporting_Airline'])['NASDelayAvg'].mean().reset_index()
    SecurityDelay_df = df.groupby(['Month','Reporting_Airline'])['SecurityDelayAvg'].mean().reset_index()
    LateAircraftDelay_df = df.groupby(['Month','Reporting_Airline'])['LateAircraftDelayAvg'].mean().reset_index()
    return CarrierDelay_df, WeatherDelay_df, NASDelay_df, SecurityDelay_df, LateAircraftDelay_df

def compute_info_2(airline_data, entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)]
    
    # Cancellation Category Count
    bar_data = df.groupby(['Month','CancellationCode'])['Flights'].sum().reset_index()
    # Average flight time by reporting airline
    line_data = df.groupby(['Month','Reporting_Airline'])['AirTime'].mean().reset_index()
    # Diverted Airport Landings
    div_data = df[df['DivAirportLandings'] != 0.0]
    # Source state count
    map_data = df.groupby(['OriginState'])['Flights'].sum().reset_index()
    # Destination state count
    tree_data = df.groupby(['DestState', 'Reporting_Airline'])['Flights'].sum().reset_index()
    return bar_data, line_data, div_data, map_data, tree_data

# Layout Section of Dash
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.layout = html.Div(children=[
    html.H1('US Domestic Airline Flights Performance', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    
    html.Div([
        html.Div(html.H2('Report Type:', style={'margin-right': '2em'})),
        
        dcc.Dropdown(
            id='input-type',
            options=[
                {'label': 'Yearly Airline Performance Report', 'value': 'OPT1'},
                {'label': 'Yearly Airline Delay Report', 'value': 'OPT2'},
            ],
            value='OPT1',
            placeholder="Select a report type",
            style={
                'width': '80%',
                'padding': '3px',
                'font-size': '20px',
                'text-align-last': 'center',
                'display': 'flex'
            }
        ),
        html.Div(html.H2('Choose Year:', style={'margin-right': '2em'})),
        
        dcc.Dropdown(
            id='input-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder="Select a year",
            style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'},
        ),
        html.Div([ ], id='plot1'),
        html.Div([
            html.Div([ ], id='plot2'),
            html.Div([ ], id='plot3')
        ], style={'display': 'flex'}),
        html.Div([
            html.Div([ ], id='plot4'),
            html.Div([ ], id='plot5')
        ], style={'display': 'flex'}),
    ])
])

# Callback to update charts based on dropdown value
@app.callback([Output(component_id='plot1', component_property='children'),
               Output(component_id='plot2', component_property='children'),
               Output(component_id='plot3', component_property='children'),
               Output(component_id='plot4', component_property='children'),
               Output(component_id='plot5', component_property='children')
               ],
               [Input(component_id='input-type', component_property='value'),
                Input(component_id='input-year', component_property='value')],
               [State("plot1", 'children'), State("plot2", "children"),
                State("plot3", "children"), State("plot4", "children"),
                State("plot5", "children")
               ])
def create_fig(entered_year,chart):
    if(chart == 'OPT1'):
        # Compute required information for creating graph from the data
        bar_data, line_data, div_data, map_data, tree_data = compute_info_2(airline_data, entered_year)
        
        # Number of flights under different cancellation categories
        bar_fig = px.bar(bar_data, x='Month', y='Flights', color='CancellationCode', title='Monthly Flight Cancellation')
        
        # Average flight time by reporting airline
        line_fig = px.line(line_data, x='Month', y='AirTime', color='Reporting_Airline', title='Average monthly flight time (minutes) by airline')
        
        # Percentage of diverted airport landings per reporting airline
        pie_fig = px.pie(div_data, values='Flights', names='Reporting_Airline', title='% of flights by reporting airline')
        
        # Number of flights flying from each state using choropleth
        map_fig = px.choropleth(map_data,  # Input data
                locations='OriginState', 
                color='Flights',  
                hover_data=['OriginState', 'Flights'], 
                locationmode = 'USA-states', # Set to plot as US States
                color_continuous_scale='GnBu',
                range_color=[0, map_data['Flights'].max()]) 
        map_fig.update_layout(
                title_text = 'Number of flights from origin state', 
                geo_scope='usa') # Plot only the USA instead of globe
        
        # Number of flights flying to each state from each reporting airline
        tree_fig = px.treemap(tree_data, path=['DestState', 'Reporting_Airline'], 
                  values='Flights',
                  color='Flights',
                  color_continuous_scale='RdBu',
                  title='Flight count by airline to destination state'
            )
        
        
        # Return dcc.Graph component to the empty division
        return [dcc.Graph(figure=tree_fig), 
                dcc.Graph(figure=pie_fig),
                dcc.Graph(figure=map_fig),
                dcc.Graph(figure=bar_fig),
                dcc.Graph(figure=line_fig)
               ]
    else:            
        # Compute required information for creating graph from the data
        avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info_1(airline_data, entered_year)
        # Create graph
        carrier_fig = px.line(data= avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average carrrier delay time (minutes) by airline')
        weather_fig = px.line(data= avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline', title='Average weather delay time (minutes) by airline')
        nas_fig = px.line(data= avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline', title='Average NAS delay time (minutes) by airline')
        sec_fig = px.line(data= avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline', title='Average security delay time (minutes) by airline')
        late_fig = px.line(data= avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline', title='Average late aircraft delay time (minutes) by airline')
        return[dcc.Graph(figure=carrier_fig),
               dcc.Graph(figure=weather_fig),
               dcc.Graph(figure=nas_fig),
               dcc.Graph(figure=sec_fig),
               dcc.Graph(figure=late_fig)]

# Run the app
if __name__ == '__main__':
    app.run_server()