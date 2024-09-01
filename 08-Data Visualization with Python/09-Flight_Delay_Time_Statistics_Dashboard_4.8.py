from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding="ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

def compute_info(airline_data, entered_year):
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

app = Dash(__name__)
app.layout = html.Div(children=[ 
  
                                html.H1('Flight Delay Time Statistics', style={'textAlign': 'center', 
                                                                               'color':'#503D36',
                                                                               'fontSize':'30px'}),
                                
                                html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010', type='number', 
                                                                    style={'height':'35px', 'fontSize':'30'}),], 
                                         style={'font-size': 30}),
                                html.Br(),
                                html.Br(),
                          
                                html.Div([
                                        html.Div(dcc.Graph(id='carrier-plot')),
                                        html.Div(dcc.Graph(id='weather-plot'))
                                ], style={'display': 'flex'}),
    
                                html.Div([
                                        html.Div(dcc.Graph(id='nas-plot')),
                                        html.Div(dcc.Graph(id='security-plot'))
                                ], style={'display': 'flex'}),
                                
                                html.Div(dcc.Graph(id='late-plot'), style={'width':'65%'})
                       
                                ])

# add callback decorator
@app.callback( [
               Output(component_id='carrier-plot', component_property='figure'),
               Output(component_id='weather-plot', component_property='figure'),
               Output(component_id='nas-plot', component_property='figure'),
               Output(component_id='security-plot', component_property='figure'),
               Output(component_id='late-plot', component_property='figure')
               ],
               Input(component_id='input-year', component_property='value'))
               
# Add computation to callback function and return graph
def get_graph(entered_year):
    
    # Compute required information for creating graph from the data
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(airline_data, entered_year)
            
    # Create graph
    carrier_fig = px.line(data= avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average carrrier delay time (minutes) by airline')
    weather_fig = px.line(data= avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline', title='Average weather delay time (minutes) by airline')
    nas_fig = px.line(data= avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline', title='Average NAS delay time (minutes) by airline')
    sec_fig = px.line(data= avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline', title='Average security delay time (minutes) by airline')
    late_fig = px.line(data= avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline', title='Average late aircraft delay time (minutes) by airline')
            
    return[carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]


# Run the app
if __name__ == '__main__':
    app.run()