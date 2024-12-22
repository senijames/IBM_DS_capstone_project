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
                                  dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'CCAFS LC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    ],
                                    value='ALL',
                                    placeholder="place holder here",
                                    searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    100: '100',
                                                    10000: '10,000'},
                                                value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                html.Div(dcc.Graph(id='alternative')),
                                ]),

                                
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filter_success = spacex_df[spacex_df['class'] == 1].groupby('Launch Site').count().reset_index()
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site].groupby('class').count().reset_index()
    if entered_site == 'ALL':
        fig = px.pie(filter_success, values='class', 
        names='Launch Site', 
        title=entered_site)
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(filtered_df, values='Launch Site',
        names='class',
        title=entered_site)
        return fig       
    



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id="success-payload-scatter-chart", component_property="figure"),
              Input(component_id="site-dropdown", component_property="value"), 
              Input(component_id="payload-slider", component_property="value"))
def get_scatter_plot(slider, ranger):    
    low, high = ranger
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    if slider == 'ALL':
        fig = px.scatter( spacex_df[mask], 
        x="Payload Mass (kg)", y="class", 
        color="Booster Version Category"), 
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == slider]
        mask_two = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
        # return the outcomes piechart for a selected site
        fig = px.scatter(
        filtered_df[mask_two], x="Payload Mass (kg)", y="class", 
        color="Booster Version Category"),
        return fig   

# Run the app
if __name__ == '__main__':
    app.run_server()
