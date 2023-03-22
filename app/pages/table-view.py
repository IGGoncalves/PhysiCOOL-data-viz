from pathlib import Path

import dash
from dash import dash_table
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__)

OUTPUT_PATH = Path("../output_norm_cond")
DATA = pd.read_csv("output_data.csv")
TIME_INTERVAL = int(DATA["time"].unique()[1])

#################################################################
# APPLICATION LAYOUT
# Simple header to b displayed at the top of the application
# Can also be used to navigate through the app (not implemented)
#################################################################

layout = dbc.Container(
    [
        dash_table.DataTable(DATA.to_dict('records'), [{"name": i, "id": i} for i in DATA.columns])
    ],
    fluid=True,
    className="dbc",
)
