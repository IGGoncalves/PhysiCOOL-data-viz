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
frames = (
    int(processing.get_cell_file_num(output_path=OUTPUT_PATH, version="1.10.2")) - 1
)

SUBSTANCES = processing.Microenvironment(0, OUTPUT_PATH).substances

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


scatter_3d = dbc.Col([dcc.Graph(id="3d-scatter-time")])


@callback(Output("3d-scatter-time", "figure"), Input("frame-slider", "value"))
def update_bar_chart(slider_range):
    variables_map = {
        "position_x": 1,
        "position_y": 2,
        "position_z": 3,
        "current_phase": 7,
        "total_volume": 4,
    }
    df = extract_data(slider_range, variables_map, OUTPUT_PATH)
    df["live_status"] = df["current_phase"] == 14
    fig = px.scatter_3d(
        df,
        x="position_x",
        y="position_y",
        z="position_z",
        size="total_volume",
        color="live_status",
        hover_data=["current_phase"],
        opacity=0.7,
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    return fig


scatter_dropdown = dbc.Col(
    [
        html.Label("Custom data:", htmlFor="scatter-custom"),
        dcc.Dropdown(
            options=[
                "current_phase",
                "intra_oxy",
                "intra_glu",
                "intra_lac",
                "intra_energy",
            ],
            value="current_phase",
            id="scatter-custom",
        ),
    ]
)

scatter_2d = dbc.Col([scatter_dropdown, html.Br(), dcc.Graph(id="2d-scatter-time")])


@callback(Output("2d-scatter-time", "figure"), Input("scatter-custom", "value"))
def update_bar_chart(custom_data):
    variables_map = {
        "position_x": 1,
        "position_y": 2,
        "position_z": 3,
        "current_phase": 7,
        "total_volume": 4,
        "intra_oxy": 27,
        "intra_glu": 28,
        "intra_lac": 29,
        "intra_energy": 30,
    }
    df = pd.concat(
        [
            extract_data(frame, variables_map, output_path=OUTPUT_PATH)
            for frame in range(frames)
        ],
        ignore_index=True,
    )
    fig = px.scatter(
        df,
        x="position_x",
        y="position_y",
        animation_frame="time",
        size="total_volume",
        color_continuous_scale="viridis",
        range_color=(df[custom_data].min(), df[custom_data].max()),
        color=custom_data,
        hover_data=["current_phase"],
        opacity=0.7,
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    return fig


scatter_div = dbc.Container([html.H2("Cell data"), dbc.Row([scatter_3d, scatter_2d])])

#################################################################
# APPLICATION LAYOUT
# Simple header to b displayed at the top of the application
# Can also be used to navigate through the app (not implemented)
#################################################################

layout = dbc.Container(
    [
        scatter_div,
        html.Br(style={"line-height": "100px"}),
    ],
    fluid=True,
    className="dbc",
)
