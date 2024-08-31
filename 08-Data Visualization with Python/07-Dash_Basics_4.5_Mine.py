from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
airline_data =  pd.read_csv('./airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})
data = airline_data.sample(n=500, random_state=42)
app = Dash(__name__)
colors = {
    'background': '#111111',
    'text': '#503D36',
}
fig = px.pie(data, values='Month', names='DistanceGroup', title='Distance group proportion by month')
#fig.show()
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Airline Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'fontSize': '40px'
        }
    ),

    html.Div(children='Proportion of distance group (250 mile distance interval group) by flights.', style={
        'textAlign': 'center',
        'color': '#F57241'
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig
    )
])
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
if __name__ == '__main__':
    app.run(debug=True)