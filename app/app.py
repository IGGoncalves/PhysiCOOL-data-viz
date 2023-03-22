from pathlib import Path

from dash import Dash, html, dcc, callback, Output, Input
import dash
import dash_bootstrap_components as dbc

import data

OUTPUT_PATH = "../output"
DATA = data.extract_data(output_path=OUTPUT_PATH)
DATA.to_csv("output_data.csv", index=False)

# stylesheet with the .dbc class from dash-bootstrap-templates library
DBC_CSS = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Bootstrap Sandstone theme
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SIMPLEX, DBC_CSS, dbc.icons.FONT_AWESOME],
    use_pages=True,
)


#################################################################
# NAVBAR (APP HEADER)
# Simple header to be displayed at the top of the application.
# Can also be used to navigate through the app.
#################################################################
navbar = dbc.NavbarSimple(
    children=[
        dcc.Store(id="time-data"),
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More", header=True),
                dbc.DropdownMenuItem("Single time", href="/single-time"),
                dbc.DropdownMenuItem("Time series", href="/data-series"),
                dbc.DropdownMenuItem("Animations", href="/animations"),
                dbc.DropdownMenuItem("Table view", href="/table-view"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="PhysiCell Data Visualizer",
    brand_href="/",
    fixed="top",
    color="dark",
    dark=True,
)

app.layout = html.Div(
    [dbc.Row(navbar), dbc.Row([dash.page_container], style={"padding-top": "100px"})]
)

if __name__ == "__main__":
    app.run_server(debug=True)
