import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

single_time_card = dbc.Col(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H1(
                        [html.I(className="fa-regular fa-clock me-2"), "Single time"],
                        className="text-nowrap",
                    ),
                    html.Hr(),
                    html.P(
                        "Some quick example text to build on the card title and "
                        "make up the bulk of the card's content.",
                        className="card-text",
                    ),
                    dbc.Button("Go to page", color="primary", href="/single-time"),
                ]
            ),
        ],
    )
)

time_series_card = dbc.Col(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H1(
                        [
                            html.I(className="fa-solid fa-chart-line me-2"),
                            "Time series",
                        ],
                        className="text-nowrap",
                    ),
                    html.Hr(),
                    html.P(
                        "Some quick example text to build on the card title and "
                        "make up the bulk of the card's content.",
                        className="card-text",
                    ),
                    dbc.Button("Go to page", color="primary", href="/data-series"),
                ]
            ),
        ],
    )
)

animation_card = dbc.Col(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H1(
                        [
                            html.I(className="fa-regular fa-circle-play me-2"),
                            "Animations",
                        ],
                        className="text-nowrap",
                    ),
                    html.Hr(),
                    html.P(
                        "Some quick example text to build on the card title and "
                        "make up the bulk of the card's content.",
                        className="card-text",
                    ),
                    dbc.Button("Go to page", color="primary", href="/animations"),
                ]
            ),
        ],
    )
)

table_view_card = dbc.Col(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H1(
                        [html.I(className="fa-solid fa-table me-2"), "Table view"],
                        className="text-nowrap",
                    ),
                    html.Hr(),
                    html.P(
                        "Some quick example text to build on the card title and "
                        "make up the bulk of the card's content.",
                        className="card-text",
                    ),
                    dbc.Button("Go to page", color="primary", href="/table-view"),
                ]
            ),
        ],
    )
)

layout = dbc.Container(
    children=[
        dbc.Col(
            html.Div(
                [
                    html.H1(
                        children="Welcome to the PhysiCell Data Visualizer",
                        className="text-center align-middle",
                    ),
                    html.H2(
                        "Please, select one of the data visualization options",
                        className="text-center",
                    ),
                    html.Hr(style={"line-height": "5"}),
                    dbc.Row([single_time_card, time_series_card]),
                    html.Br(),
                    dbc.Row([animation_card, table_view_card]),
                ],
                className="h-100 p-5 bg-light border rounded-3",
            ),
            width={"size": 10, "offset": 1},
        ),
    ]
)
