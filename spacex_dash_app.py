# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',  
                                    options=[{'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                        {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                        {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'}],
                                    value='ALL',
                                    placeholder='Select a Lunch Site here',
                                    searchable=True),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                 marks={0: '0', 2000: '2000', 4000: '4000', 6000:'6000', 8000: '8000', 10000: '10000'},
                                 value=[min_payload, max_payload]
                                 ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        filtered_df = filtered_df[filtered_df['class'] == 1].reset_index()
        filtered_df = filtered_df.groupby('Launch Site')['class'].sum().reset_index(name='counts')
        fig = px.pie(filtered_df, values='counts', 
        names='Launch Site', 
        title='Successfull landings for each Launch Site')
        return fig
    else:
        filtered_df=filtered_df[filtered_df['Launch Site']==entered_site]
        filtered_df=filtered_df.groupby('class')['class'].value_counts().reset_index(name='counts')
        filtered_df.columns=['class', 'counts']
        filtered_df['class'] = filtered_df['class'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(filtered_df, values='counts', 
        names='class', 
        color='class',
        color_discrete_map={'Success': 'green', 'Failure': 'red'},
        title='Successfull landings for site {}'.format(entered_site))
        return fig
                                        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'),
            Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, entered_payload):
    filtered_df = spacex_df
    if entered_site=='ALL':
        fig2 = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color="Booster Version Category", 
        title="Success rate for all launch sites")
        return fig2
    else:
        filtered_df=filtered_df[filtered_df['Launch Site']==entered_site]
        fig2 = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color="Booster Version Category",
        title="Succes rate for site {}".format(entered_site))
        return fig2 

# Run the app
if __name__ == '__main__':
    app.run_server()
