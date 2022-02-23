import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import plotly.graph_objects as go
from dash import State

# Malleable Variables
processed_df_loc = '../sample_transcriptions/122021_processed.csv'

# Creating the App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Setting up dataframes
df_index = 0
input_df = pd.read_csv(processed_df_loc)
running_df = pd.DataFrame()
instantaneous_df = input_df.iloc[df_index]


instance_ui = html.Div([
    #dash_table.DataTable(input_df.to_dict('records'), [{"name": i, "id": i} for i in input_df.columns]),
    
    # Initial Data
    html.H3('Initial Data'),
    html.P(instantaneous_df['Transcriptions']), # Breakpoint--will change depending on data source
    html.P('Extracted Callsign: ' + str(instantaneous_df['callsign'])), # Breakpoint--will change depending on data source
    html.P('Extracted Altitude Change: ' + str(instantaneous_df['altitude'])), # Breakpoint--will change depending on data source
    html.P('Extracted Heading Change: ' + str(instantaneous_df['heading'])), # Breakpoint--will change depending on data source
    html.P('Extracted Speed Change: ' + str(instantaneous_df['speed'])), # Breakpoint--will change depending on data source
    
    # Editable Data
    html.H3('Change Values: '),
    html.Div([
        "Callsign: ",
        dcc.Input(id='callsign-input', value=instantaneous_df['callsign'], type='text')
    ]),
    html.Br(),
    html.Div(html.P(id='callsign-output')),
    html.Div([
        "Altitude: ",
        dcc.Input(id='altitude-input', value=instantaneous_df['altitude'], type='text')
    ]),
    html.Br(),
    html.Div(html.P(id='altitude-output')),
    html.Div([
        "Heading: ",
        dcc.Input(id='heading-input', value=instantaneous_df['heading'], type='text')
    ]),
    html.Br(),
    html.Div(html.P(id='heading-output')),
    html.Div([
        "Speed: ",
        dcc.Input(id='speed-input', value=instantaneous_df['speed'], type='text')
    ]),
    html.Br(),
    html.Div(html.P(id='speed-output')),
],)

app.layout = html.Div([
    html.H1("Human Validation for ATC Project"),
    html.Br(),
    html.Button('Next', id='next-val'),
    #html.Button('Back', id='next-val'),


    #html.Button('Submit', id='button'),
    html.Div(id='output-container-button',
             children='Enter a value and press submit')
])



"""@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )
"""


@app.callback(
    Output('output-container-button', 'children'),
    Input('next-val', 'n_clicks'),
    #State('input-on-submit', 'value')
)
def page_forward(n_clicks):
    global df_index 
    df_index += 1
    print(df_index)
    instantaneous_df = input_df.iloc[df_index]
    
    link = 'https://drive.google.com/drive/search?q=' + instantaneous_df['id']

    return html.Div([
        html.H3('Initial Data'),
        dash.dcc.Link('Audio Link', link),
        html.P(instantaneous_df['Transcriptions']), # Breakpoint--will change depending on data source
        html.P('Extracted Callsign: ' + str(instantaneous_df['callsign'])), # Breakpoint--will change depending on data source
        html.P('Extracted Altitude Change: ' + str(instantaneous_df['altitude'])), # Breakpoint--will change depending on data source
        html.P('Extracted Heading Change: ' + str(instantaneous_df['heading'])), # Breakpoint--will change depending on data source
        html.P('Extracted Speed Change: ' + str(instantaneous_df['speed'])), # Breakpoint--will change depending on data source
        
        # Editable Data
        html.H3('Change Values: '),
        html.Div([
            "Callsign: ",
            dcc.Input(id='callsign-input', value=instantaneous_df['callsign'], type='text')
        ]),
        html.Br(),
        html.Div(html.P(id='callsign-output')),
        html.Div([
            "Altitude: ",
            dcc.Input(id='altitude-input', value=instantaneous_df['altitude'], type='text')
        ]),
        html.Br(),
        html.Div(html.P(id='altitude-output')),
        html.Div([
            "Heading: ",
            dcc.Input(id='heading-input', value=instantaneous_df['heading'], type='text')
        ]),
        html.Br(),
        html.Div(html.P(id='heading-output')),
        html.Div([
            "Speed: ",
            dcc.Input(id='speed-input', value=instantaneous_df['speed'], type='text')
        ]),
        html.Br(),
        html.Div(html.P(id='speed-output')),
    ])
"""
@app.callback(
    #Output('container-button-basic', 'children'),
    Input('back-val'),
)
def page_back(input_value):
    df_index -= 1
    instantaneous_df = input_df.iloc[df_index]"""

@app.callback(
    Output(component_id='callsign-output', component_property='children'),
    Input(component_id='callsign-input', component_property='value')
)
def update_callsign_div(input_value):
    instantaneous_df['callsign'] = input_value

    return f'Output: {input_value}'

@app.callback(
    Output(component_id='altitude-output', component_property='children'),
    Input(component_id='altitude-input', component_property='value')
)
def update_altitude_div(input_value):
    instantaneous_df['altitude'] = input_value

    return f'Output: {input_value}'

@app.callback(
    Output(component_id='heading-output', component_property='children'),
    Input(component_id='heading-input', component_property='value')
)
def update_heading_div(input_value):
    instantaneous_df['heading'] = input_value

    return f'Output: {input_value}'

@app.callback(
    Output(component_id='speed-output', component_property='children'),
    Input(component_id='speed-input', component_property='value')
)
def update_speed_div(input_value):
    instantaneous_df['speed'] = input_value

    return f'Output: {input_value}'

if __name__ == '__main__':
    app.run_server(debug=True)

"""
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Select Dataset", header=True),
                dbc.DropdownMenuItem("nuScenes", id="nuscenes-select"),
                dbc.DropdownMenuItem("astyx", id="astyx-select"),
            ],
            nav=True,
            in_navbar=True,
            label="Current Dataset: nuScenes",
            right=True,
            id="datasets"
        ),
    ],
    brand="Project Configs",
    brand_href="#",
    fluid=True,
    color="primary",
    dark=True,
)

dbscan_select = html.Div([
    html.P("eps"),
    dcc.Slider(min=1, max=10, value=3, step=1,
        marks={
            1: {'label': '1 eps'},
            5: {'label': '5 eps'},
            10: {'label': '10 eps'}
        },
        id="dbscan-eps-select"
    ),
    html.Br(),
    html.P("min-pts"),
    dcc.Slider(min=1, max=10, value=3, step=1,
        marks={
            1: {'label': '1 pts'},
            5: {'label': '5 pts'},
            10: {'label': '10 pts'}
        },
        id="dbscan-min-select"
    )], id="dbscan-select", style=dict(display="none"))

optics_select = html.Div([
    html.P("min_pts"),
    dcc.Slider(min=1, max=10, value=3, step=1,
        marks={
            1: {'label': '1 eps'},
            5: {'label': '5 eps'},
            10: {'label': '10 eps'}
        },
        id="optics-min-select"
    )], id="optics-select", style=dict(display="none"))

gbdbscan_select = html.Div([
    html.P("g"),
    dcc.Slider(min=1, max=5, value=1, step=1,
        marks={
            1: {'label': '1'},
            3: {'label': '3'},
            5: {'label': '5'}
        },
        id="gbdbscan-g-select"
    ),
    html.Br(),
    html.P("f"),
    dcc.Slider(min=1, max=10, value=2, step=1,
        marks={
            1: {'label': '1'},
            5: {'label': '5'},
            10: {'label': '10'}
        },
        id="gbdbscan-f-select"
    ),
    html.Br(),
    html.P("k"),
    dcc.Slider(min=0.1, max=1, value=0.3, step=0.1,
        marks={
            0.1: {'label': '0.1'},
            0.5: {'label': '0.5'},
            1: {'label': '1'}
        },
        id="gbdbscan-k-select"
    ),
    html.Br(),
    html.P("num_r"),
    dcc.Slider(min=1, max=100, value=75, step=1,
        marks={
            1: {'label': '1'},
            50: {'label': '50'},
            100: {'label': '100'}
        },
        id="gbdbscan-num_r-select"
    ),
    html.Br(),
    html.P("num_t"),
    dcc.Slider(min=1, max=30, value=18, step=1,
        marks={
            1: {'label': '1'},
            15: {'label': '15'},
            30: {'label': '30'}
        },
        id="gbdbscan-num_t-select"
    )], id="gbdbscan-select", style=dict(display="none"))

hdbscan_select = html.Div([
    html.P("min_cluster_size"),
    dcc.Slider(min=1, max=10, value=5, step=1,
        marks={
            1: {'label': '1'},
            5: {'label': '5'},
            10: {'label': '10'}
        },
        id="hdbscan-min-cluster-size-select"
    )], id="hdbscan-select", style=dict(display="none"))

sidebar = html.Div(
    [
        html.H2("Clustering Options", className="display-5"),
        html.Hr(),
        html.P(
            "Select algorithm to display.", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("DBSCAN", href="/dbscan", active="exact"),
                dbc.NavLink("OPTICS", href="/optics", active="exact"),
                dbc.NavLink("GBDBSCAN", href="/gbdbscan", active="exact"),
                dbc.NavLink("HDBSCAN", href="/hdbscan", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Div([
            html.Hr(),
            html.P("Select algorithm parameters", className="lead"),
            dbscan_select,
            optics_select,
            gbdbscan_select,
            hdbscan_select
        ], id="param-section", style=dict(display="none")),
    ],
)

content = html.Div(id="content")

row = html.Div(
    [
        dbc.Row(html.Hr(), style=dict(width="100%")),
        dbc.Row(
            [
                dbc.Col(sidebar, width="3"),
                dbc.Col(content, width="8")
            ],
            justify="around",
            style=dict(width="100%")
        ),
        html.Br()
    ],
)

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div([
        navbar,
        row,
    ]),
])


# @app.callback(
#     Output("datasets", "label"),
#     [Input("nuscenes-select", "n_clicks"), Input("astyx-select", "n_clicks")],
# )
# def update_data(nuscenes, astyx):
#     id_lookup = {"nuscenes-select": "nuScenes", "astyx-select": "astyx"}

#     ctx = dash.callback_context

#     if (nuscenes is None and astyx is None) or not ctx.triggered:
#         return "Current Dataset: nuScenes"

#     button_id = ctx.triggered[0]["prop_id"].split(".")[0]
#     return "Current Dataset: " + id_lookup[button_id]

@app.callback(
    Output("datasets", "label"),
    Output("param-section", "style"),
    Output("content", "children"),
    Output("dbscan-select", "style"),
    Output("optics-select", "style"),
    Output("gbdbscan-select", "style"),
    Output("hdbscan-select", "style"),
    Input("url", "pathname"),
    Input("nuscenes-select", "n_clicks"),
    Input("astyx-select", "n_clicks"),
    Input("dbscan-eps-select", "value"),
    Input("dbscan-min-select", "value"),
    Input("optics-min-select", "value"),
    Input("gbdbscan-g-select", "value"),
    Input("gbdbscan-f-select", "value"),
    Input("gbdbscan-k-select", "value"),
    Input("gbdbscan-num_r-select", "value"),
    Input("gbdbscan-num_t-select", "value"),
    Input("hdbscan-min-cluster-size-select", "value"))
def render_content(pathname, nuscenes, astyx, dbscan_eps, dbscan_min_samples, optics_min_samples, gbdbscan_g, gbdbscan_f, gbdbscan_k, gbdbscan_num_r, gbdbscan_num_t, hdbscan_min_cluster_size):
    id_lookup = {"nuscenes-select": "nuScenes", "astyx-select": "astyx"}
    ctx = dash.callback_context
    if (nuscenes is None and astyx is None) or not ctx.triggered:
        dataset_label = "Current Dataset: nuScenes"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id in id_lookup.keys():
            dataset_label = "Current Dataset: " + id_lookup[button_id]
        else:
            dataset_label = "Current Dataset: nuScenes"
    if pathname == "/dbscan":
        plots.algo = "dbscan"
        dbscan_scatter, dbscan_overlay, dbscan_metrics = plots._cluster(dataset=dataset_label[17:], dbscan_eps=dbscan_eps, dbscan_min_samples=dbscan_min_samples)
        content = html.Div([
            dcc.Graph(figure=dbscan_scatter),
            dcc.Graph(figure=dbscan_overlay),
            html.Hr(),
            html.P("v_measure_score: " + str(dbscan_metrics["v_measure_score"])),
            html.P("homogeneity_score: " + str(dbscan_metrics["homogeneity_score"])),
            html.P("completeness_score: " + str(dbscan_metrics["completeness_score"])),
            html.Br()
        ])
        return dataset_label, dict(display="block"), content, dict(display="block"), dict(display="none"), dict(display="none"), dict(display="none")
    elif pathname == "/optics":
        plots.algo = "optics"
        optics_scatter, optics_overlay, optics_metrics = plots._cluster(dataset=dataset_label[17:], optics_min_samples=optics_min_samples)
        content = html.Div([
            dcc.Graph(figure=optics_scatter),
            dcc.Graph(figure=optics_overlay),
            html.Hr(),
            html.P("v_measure_score: " + str(optics_metrics["v_measure_score"])),
            html.P("homogeneity_score: " + str(optics_metrics["homogeneity_score"])),
            html.P("completeness_score: " + str(optics_metrics["completeness_score"])),
            html.Br()
        ])
        return dataset_label, dict(display="block"), content, dict(display="none"), dict(display="block"), dict(display="none"), dict(display="none")
    elif pathname == "/gbdbscan":
        plots.algo = "gbdbscan"
        gbdbscan_scatter, gbdbscan_overlay, gbdbscan_metrics = plots._cluster(dataset=dataset_label[17:], gbdbscan_g=gbdbscan_g, gbdbscan_f=gbdbscan_f, gbdbscan_k=gbdbscan_k, gbdbscan_num_r=gbdbscan_num_r, gbdbscan_num_t=gbdbscan_num_t)
        content = html.Div([
            dcc.Graph(figure=gbdbscan_scatter),
            dcc.Graph(figure=gbdbscan_overlay),
            html.Hr(),
            html.P("v_measure_score: " + str(gbdbscan_metrics["v_measure_score"])),
            html.P("homogeneity_score: " + str(gbdbscan_metrics["homogeneity_score"])),
            html.P("completeness_score: " + str(gbdbscan_metrics["completeness_score"])),
            html.Br()
        ])
        return dataset_label, dict(display="block"), content, dict(display="none"), dict(display="none"), dict(display="block"), dict(display="none")
    elif pathname == "/hdbscan":
        plots.algo = "hdbscan"
        hdbscan_scatter, hdbscan_overlay, hdbscan_metrics = plots._cluster(dataset=dataset_label[17:], hdbscan_min_cluster_size=hdbscan_min_cluster_size)
        content = html.Div([
            dcc.Graph(figure=hdbscan_scatter),
            dcc.Graph(figure=hdbscan_overlay),
            html.Hr(),
            html.P("v_measure_score: " + str(hdbscan_metrics["v_measure_score"])),
            html.P("homogeneity_score: " + str(hdbscan_metrics["homogeneity_score"])),
            html.P("completeness_score: " + str(hdbscan_metrics["completeness_score"])),
            html.Br()
        ])
        return dataset_label, dict(display="block"), content, dict(display="none"), dict(display="none"), dict(display="none"), dict(display="block")
    else:
        return dataset_label, dict(display="none"), html.Div(), dict(display="none"), dict(display="none"), dict(display="none"), dict(display="none")

"""
