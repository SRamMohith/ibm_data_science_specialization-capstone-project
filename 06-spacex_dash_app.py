# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import wget

# Read the airline data into pandas dataframe
spacex_file = wget.download("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
spacex_df = pd.read_csv(spacex_file)
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
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                            options=[{'label':'All Site','value':'ALL'},{'label':'KSC LC-39A','value':'KSC LC-39A'},{'label':'CCAFS LC-40','value':'CCAFS LC-40'},{'label':'VAFB SLAC-4E','value':'VAFB SLC-4E'},{'label':'CCAFS SLC-40','value':'CCAFS SLC-40'}],
                                            value='ALL',
                                            placeholder='Select a Launch Site here',
                                            searchable='True'),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, max=10000, step=1000, value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart',component_property='figure'),
    Input(component_id='site-dropdown',component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site=='ALL':
        val = spacex_df.groupby('Launch Site')['class'].sum()
        fig = px.pie(spacex_df,values=val,names=spacex_df['Launch Site'].unique(),title='Pie Chart for All Sites')
    else:
        spacex_df_filter = spacex_df[spacex_df['Launch Site']==entered_site]
        val = spacex_df_filter['class'].value_counts(normalize=True)
        fig = px.pie(spacex_df_filter,values=val,names=spacex_df_filter['class'].unique(),title=f'Pie chart for {entered_site}')
    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),Input(component_id='payload-slider',component_property='value')]
)
def get_scatter_plot(entered_site,payload_range):
    min_pay, max_pay = payload_range
    spacex_df_payload = spacex_df[(spacex_df['Payload Mass (kg)']>=min_pay) & (spacex_df['Payload Mass (kg)']<=max_pay)]

    if entered_site=='ALL':
        fig = px.scatter(
            data_frame=spacex_df_payload,
            x='Payload Mass (kg)',y='class',color='Booster Version Category',
            title='Correlation between Success and Paylload for All Sites')
    else:
        fig = px.scatter(
            data_frame=spacex_df_payload[spacex_df_payload['Launch Site']==entered_site],
            x='Payload Mass (kg)',y='class',color='Booster Version Category',
            title=f'Correlation between Success and Payload for {entered_site}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()