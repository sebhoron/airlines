# Import required modules.
import pandas as pd

import dash
import dash_html_components as html
import dash_table as dt
import dash_core_components as dcc
import plotly.express as px

from dash.dependencies import Input, Output


app = dash.Dash() # Initialise dash app.

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Read in data.
url = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv'
AirlineSafetyData = pd.read_csv(url)
TopAirlines19 = AirlineSafetyData.sort_values('incidents_85_99', ascending=False).head(5)
TopAirlines20 = AirlineSafetyData.sort_values('incidents_00_14', ascending=False).head(5)

# Set layout.
app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Airline Accidents', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),
        html.Div(children='First look at the data', style={'textAlign':'left',
                                            'marginBottom':10}),
        # Add a table.
        dt.DataTable(
        id='tbl', data=AirlineSafetyData.head(10).to_dict('records'),
        columns=[{"name": i, "id": i} for i in AirlineSafetyData.head(10).columns],
        ),
        html.Div(children='Plotting by airlines', style={'textAlign':'left',
                                            'marginTop':20,'marginBottom':10}),
        # Create a dropdown.
        dcc.Dropdown(id = 'dropdown_scatter', 
        options = [
            {'label':'Fatalities', 'value':'Fatalities'},
            {'label':'Fatal accidents', 'value':'Fatal accidents'},
            {'label':'Incidents', 'value':'Incidents'}
            ],
        value = 'Fatalities'), # Default value.
        dcc.Graph(id = 'scatter_plot'), # Create graph.
        html.Div(children='Airlines with most accidents', style={'textAlign':'left',
                                            'marginTop':20,'marginBottom':10}),
        dcc.Dropdown(id = 'dropdown_bar',
        options = [
            {'label':'1985-99', 'value':'1985-99'},
            {'label':'2000-14', 'value':'2000-14'}
        ],
        value = '2000-14'),
        dcc.Graph(id = 'bar_plot')
    ])
    
# Create callback that will connect the dropdown and the scatter plot.
@app.callback(Output(component_id='scatter_plot', component_property= 'figure'),
              [Input(component_id='dropdown_scatter', component_property= 'value')])
def graph_update(dropdown_value):
    print(dropdown_value)
    
    # Adjust the plot depending on the chosen option.
    if dropdown_value == 'Fatalities': 
        fig = px.scatter(AirlineSafetyData, x='fatalities_85_99', y ='fatalities_00_14', 
                        color='avail_seat_km_per_week', text="airline", opacity=0.75, 
                        trendline='ols', trendline_color_override='red')
    elif dropdown_value == 'Incidents':
        fig = px.scatter(AirlineSafetyData, x='incidents_85_99', y='incidents_00_14', 
                        color='avail_seat_km_per_week', text="airline", opacity=0.75,
                        trendline='ols', trendline_color_override='red')
    elif dropdown_value == 'Fatal accidents':
        fig = px.scatter(AirlineSafetyData, x='fatal_accidents_85_99', y='fatal_accidents_00_14', 
                        color='avail_seat_km_per_week', text="airline", opacity=0.75,
                        trendline='ols', trendline_color_override='red')
    fig.update_layout(title = '{}'.format(dropdown_value) + ' by Airline ',
                      xaxis_title = '1985-99',
                      yaxis_title = '2000-14'
                      )
    return fig
# Create callback that will connect the dropdown and the bar plot.
@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='dropdown_bar', component_property= 'value')])
def graph_update(dropdown_value):
    print(dropdown_value)

    if dropdown_value == '2000-14': 
        fig = px.bar(TopAirlines20, x='airline', y ='fatalities_00_14', color='airline')
    elif dropdown_value == '1985-99':
        fig = px.bar(TopAirlines19, x='airline', y='incidents_85_99', color='airline')
    
    fig.update_layout(title = '5 Airlines with the highest number of incidents in years ' + '{}'.format(dropdown_value),
                      xaxis_title = '',
                      yaxis_title = 'Number of incidents'
                      )
    return fig
# Run web server.
if __name__ == '__main__': 
    app.run_server()