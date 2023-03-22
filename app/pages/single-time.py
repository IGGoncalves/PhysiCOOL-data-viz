from pathlib import Path
from typing import Dict

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
from physicool import processing
import plotly.express as px
import pandas as pd
from scipy import io as sio

palettes = px.colors.named_colorscales()

dash.register_page(__name__)

OUTPUT_PATH = Path("../output_norm_cond")
DATA = pd.read_csv("output_data.csv")
TIME_INTERVAL = int(DATA["time"].unique()[1])
print(TIME_INTERVAL)

SUBSTANCES = processing.Microenvironment(0, OUTPUT_PATH).substances

time_slider = dbc.Col(
    [
        html.Label(html.P("Select timestep (minutes)"), htmlFor="frame-slider"),
        html.Div(
            dcc.Slider(
                min=DATA["time"].min(),
                max=DATA["time"].max(),
                step=TIME_INTERVAL,
                id="frame-slider",
                value=DATA["time"].min(),
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
            ),
        ),
    ],
    className="p-3 bg-light border rounded-3",
    width={"size": 4, "offset": 4},
)

#################################################################
# CELL CONTAINER
#################################################################


def extract_data(
    frame: int, variables_map: Dict[str, int], output_path: Path
) -> pd.DataFrame:
    """Extracts the passed variables from the output files for the given time point."""
    time_str = str(frame).zfill(8)
    path_name = output_path / f"output{time_str}_cells_physicell.mat"
    cells = sio.loadmat(path_name)["cells"]
    # Create a DataFrame where each column is a cell variable
    data = pd.DataFrame({key: cells[value] for key, value in variables_map.items()})
    # Add the current time point to the DataFrame to identify it later
    data["time"] = frame
    return data


scatter_3d = dbc.Col([dcc.Graph(id="3d-scatter")])


@callback(Output("3d-scatter", "figure"), Input("frame-slider", "value"))
def update_bar_chart(slider_range):
    fig = px.scatter_3d(
        DATA[DATA["time"] == slider_range],
        x="position_x",
        y="position_y",
        z="position_z",
        size="total_volume",
        color="current_phase",
        hover_data=["current_phase"],
        opacity=0.7,
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.update(layout_showlegend=False)
    return fig


scatter_dropdown = dbc.Col(
    [
        html.Label("Custom data:", htmlFor="scatter-custom"),
        dcc.Dropdown(
            options=DATA.columns,
            value=DATA.columns[2],
            id="scatter-custom",
        ),
    ]
)

scatter_2d = dbc.Col([scatter_dropdown, html.Br(), dcc.Graph(id="2d-scatter")])


@callback(
    Output("2d-scatter", "figure"),
    Input("scatter-custom", "value"),
    Input("frame-slider", "value"),
)
def update_bar_chart(custom_data, frame):
    fig = px.scatter(
        DATA[DATA["time"] == frame],
        x="position_x",
        y="position_y",
        size="total_volume",
        color_continuous_scale="viridis",
        range_color=(DATA[custom_data].min(), DATA[custom_data].max()),
        color=custom_data,
        hover_data=["current_phase"],
        opacity=0.7,
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    return fig


scatter_div = dbc.Container([html.H2("Cell data"), dbc.Row([scatter_3d, scatter_2d])])

#################################################################
# ENVIRONMENT CONTAINER
#################################################################

# First substance plot
env_chart1 = dbc.Col(
    [
        dcc.Graph(id="graph"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Substance:", htmlFor="substance"),
                        dcc.Dropdown(
                            options=SUBSTANCES,
                            value=SUBSTANCES[0],
                            id="substance",
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label("Min value:", htmlFor="vmin"),
                        dbc.Input(
                            type="number", min=0, max=10, step=0.01, value=0, id="vmin"
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label("Max value:", htmlFor="vmax"),
                        dbc.Input(
                            type="number", min=0, max=10, step=0.01, value=1, id="vmax"
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label("Palette:", htmlFor="map"),
                        dcc.Dropdown(options=palettes, value="darkmint", id="map"),
                    ]
                ),
            ]
        ),
    ]
)


# Method to update the first substance plot
# It will consider as input the values from:
#   - the substance dropdown (substance);
#   - the time point slider (frame);
#   - the palette dropdown (palette);
@callback(
    Output("graph", "figure"),
    [
        Input("substance", "value"),
        Input("frame-slider", "value"),
        Input("map", "value"),
    ],
)
def filter_heatmap(substance: str, frame: int, palette: str):
    """
    Plots a heatmap with the substance concentration data.

    Inputs:
    substance: str
        The substance to be plotted (selected from the "substance" dropdown)
    """
    # Load the data from the
    me = processing.Microenvironment(int(frame/TIME_INTERVAL), OUTPUT_PATH)
    fig = px.imshow(
        me.data[substance][0],
        color_continuous_scale=palette,
        # title=f"Substance: {substance}",
    )
    fig.update_layout(coloraxis=dict(colorbar=dict(orientation="h", y=-0.5)))
    fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
    return fig


env_chart2 = dbc.Col(
    [
        dcc.Graph(id="graph_2"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Substance:", htmlFor="substance_2"),
                        dcc.Dropdown(
                            options=SUBSTANCES,
                            value=SUBSTANCES[-1],
                            id="substance_2",
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label("Min value:", htmlFor="vmin_2"),
                        dbc.Input(
                            type="number",
                            min=0,
                            max=10,
                            step=0.01,
                            value=0,
                            id="vmin_2",
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label("Max value:", htmlFor="vmax_2"),
                        dbc.Input(
                            type="number",
                            min=0,
                            max=10,
                            step=0.01,
                            value=1,
                            id="vmax_2",
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label("Palette:", htmlFor="map_2"),
                        dcc.Dropdown(options=palettes, value="sunset", id="map_2"),
                    ]
                ),
            ]
        ),
    ]
)


@callback(
    Output("graph_2", "figure"),
    [
        Input("substance_2", "value"),
        Input("frame-slider", "value"),
        Input("map_2", "value"),
        Input("vmin_2", "value"),
        Input("vmax_2", "value"),
    ],
)
def filter_heatmap(substance, frame, palette, vmin, vmax):
    me = processing.Microenvironment(int(frame/TIME_INTERVAL), OUTPUT_PATH)
    fig = px.imshow(
        me.data[substance][0],
        color_continuous_scale=palette,
        # zmin=vmin,
        # zmax=vmax,
        # labels=dict(x="X coordinates", y="Y coordinates", color="Concentration"),
    )
    fig.update_layout(coloraxis=dict(colorbar=dict(orientation="h", y=-0.5)))
    fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
    return fig


env_div = dbc.Container(
    [
        html.H2("Extracellular substances"),
        dbc.Row([env_chart1, env_chart2]),
    ]
)

#################################################################
# APPLICATION LAYOUT
# Simple header to b displayed at the top of the application
# Can also be used to navigate through the app (not implemented)
#################################################################

layout = dbc.Container(
    [
        dbc.Row([time_slider], class_name="px-0"),
        html.Br(style={"line-height": "50px"}),
        scatter_div,
        html.Br(),
        env_div,
        html.Br(style={"line-height": "100px"}),
    ],
    fluid=True,
    className="dbc",
)
