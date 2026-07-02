# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
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
                                               
        dcc.Dropdown(id='site-dropdown',
                options=[
                    {'label':'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                ],
                value='ALL',
                placeholder="Select a Launch Site Here",
                searchable=True                  
                ),




                html.Br(),  
               
                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                # If a specific launch site was selected, show the Success vs. Failed counts for the site
           
                html.Div(dcc.Graph(id='success-pie-chart')),
                html.Br(),




                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
               
                    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, marks={0: '0', 100: '100'}, value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
               
                html.Br(),
                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
               
                ]),






# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
        Output(component_id='success-pie-chart', component_property='figure'),
        Input(component_id='site-dropdown', component_property='value')
)




def pie_chart(entered_site):
   
    if entered_site =='ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total succesful launches in all sites')
        return fig
    else:
        new_df = spacex_df[spacex_df['Launch Site']== entered_site]
        success_failured = new_df.groupby(['Launch Site', 'class']).size().reset_index(name='class total')




        fig = px.pie(success_failured,values='class total', names='class',title='Total Launch Site Success')
        return fig
















# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id="payload-slider", component_property="value")
    ]
)




def scatter_chart(entered_site, payload_range):
    minimum, maximum = payload_range
    payload_mass_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= minimum) & (spacex_df['Payload Mass (kg)'] <= maximum)]




    if entered_site == 'ALL':
        fig = px.scatter(payload_mass_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title='Correlation Between Payload and Success for All Sites')
        return fig
    else:
        new_filtered_df = payload_mass_df[payload_mass_df['Launch Site'] == entered_site]
        fig = px.scatter(new_filtered_df, x='Payload Mass (kg)', y= 'class', color='Booster Version Category', title='Selected Launch Site Payload mass compared to class')
        return fig




if __name__ == '__main__':
    app.run(port=8066)
