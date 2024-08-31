from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


airline_data = pd.read_csv('./airline_data.csv', 
                            encoding="ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})


app = Dash(__name__)


app.layout = html.Div(children=[html.H1(children='Airline Dashboard',
                                        style={'textAlign': 'center',
                                               'color': '#503D36',
                                               'fontSize': '40px'}),
                                html.Div(['Input:', dcc.Input(id='input-year', value='2000', type='number', 
                                                              style={'height':'50px', 'font-size': 35})], 
                                         style={'fontSize': '40px'}),
                                html.Br(),
                                html.Br(),
                                html.Div(
                                    dcc.Graph(id='line-plot')),
                               ], style={'backgroundColor':'#111111'})

@app.callback(
    Output(component_id='line-plot', component_property='figure'),
    Input(component_id='input-year', component_property='value'))
def create_figure(year):
    df = airline_data[airline_data['Year'] == int(year)][['Month', 'ArrDelay']]
    df.rename(columns={'ArrDelay': 'ArrDelayAvg'}, inplace=True)
    mean_delays = df.groupby('Month').mean().reset_index()
    fig = px.line(mean_delays, x='Month', y='ArrDelayAvg', title='Sales Over Years')
    return fig
                               
if __name__ == '__main__':
    app.run()