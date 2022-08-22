import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

data=pd.read_csv("spacex_launch_dash.csv")
max_payload = data['Payload Mass (kg)'].max()
min_payload = data['Payload Mass (kg)'].min()
app = dash.Dash(__name__)
app.layout = html.Div(children=[html.H1("SpaceX Launch Records Dashboard",
                                style={"textAlign":"center","color":"#503D36",
                                "font-size":40}),
                                dcc.Dropdown(id='site-dropdown',
                                options=[{'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                ],value='ALL',placeholder="Select a location",
                                searchable=True
                                ),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                 min=0, max=10000, step=1000,
                                 value=[min_payload, max_payload])),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# add callback decorator 
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = data[data["Launch Site"]==entered_site]
    if entered_site == 'ALL':
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='Success by site')
        return fig
    else:
        filtered_df=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(filtered_df,values='class count',
        names='class',title="Total Success Launches for site " + entered_site)
        return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_site,payload):
    filtered_df=data[data["Payload Mass (kg)"].between(payload[0], payload[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",color="Booster Version Category",
        title='Success for the selected payload mass range for all sites')
        return fig
    else:
        filtered_df=filtered_df[filtered_df["Launch Site"]==entered_site]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",color="Booster Version Category",
        title=f"Success count for the selected payload mass range for {entered_site}")
        return fig

# Run the application                   
if __name__ == '__main__':
    app.run_server(port=3099)
                