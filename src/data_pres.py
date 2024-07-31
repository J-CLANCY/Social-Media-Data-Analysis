#!/usr/bin/env python3
"""
This script presents using Plotly/Dash the analysis of the data downloaded from Meta i.e. Facebook/Instagram.

This script has a companion script "data_proc.py" which processes the raw data for presentation.

"""

__author__ = "Joseph Clancy"
__version__ = "0.1.0"
__license__ = "MIT"

import pathlib
import json
import dash
import yaml

import plotly.io as pio
import plotly.express as px

from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State


def setup():
    """Pull in config.yaml from config folder"""

    with open("../config/config.yaml", "r") as file:
        conf = yaml.safe_load(file)

        # Set the token for mapbox API
        px.set_mapbox_access_token(conf["token"])

    return conf

# Initialisation crap
# ======================================================================================================================
proj_dir = pathlib.Path.cwd()
raw_data_dir = pathlib.Path(f"D:/Social_Media_Data")
config = setup()
pio.templates.default = "seaborn"

# Import processed data
with open("../output/results.json", "r") as data_file:
    results = json.load(data_file)

platforms_list = list(results.keys())

# Dash app instantiation/configuration
# ======================================================================================================================
app = dash.Dash(__name__, external_stylesheets=config["external_stylesheets"], suppress_callback_exceptions=True)
app.title = "My Social Media Chats Analysis"

# HTML layout definition
app.layout = html.Div([
    # Header/Title definition
    html.Div(
        children=[
            html.H1(
                children="My Social Media Chats Analysis", className="header-title"
            ),
            html.P(children="Joseph Clancy", className="header-author"),
        ],
        className="header",
    ),

    # Drop down menu definitions
    html.Div([
        # Platform Selector Dropdown
        html.Div(
            children=[
                html.Div(children="Platform", className="menu-title"),
                dcc.Dropdown(
                    id="platform_dropdown",
                    persistence=True,
                    options=[{"value": x, "label": x}
                             for x in platforms_list],
                    value=platforms_list[0],
                    className="dropdown",
                ),
            ], className="drop"
        ),
        # Chat Selector Dropdown
        html.Div(
            id="chats_div",
            children=[
                html.Div(children="Chats", className="menu-title"),
                dcc.Dropdown(
                    id="chats_dropdown",
                    persistence=True,
                    options=[{"value": x, "label": x} for x in list(results[platforms_list[0]].keys())],
                    value=list(results[platforms_list[0]].keys())[0],
                    className="dropdown",
                ),
            ],
            className="drop"
        ),
    ], className="menu"),

    # Wrapper for the main body of the page containing graphs
    html.Div(id='main_page', children=[], className="wrapper"),

], style={'backgroundColor': '#EDEDED'})


# Assistance Functions
# ======================================================================================================================
def make_stats_table(stats_dict):

    stats_div = [html.Div(
        children=[
            html.Div(children=f"Counts Table", className="header-title"),
            dash_table.DataTable(
                id='stats_table',
                columns=[{"name": i, "id": i, "type": "numeric"} for i in
                         list(stats_dict["counts"].keys())],
                data=[stats_dict["counts"]],
                style_cell=dict(textAlign='center'),
                style_header=dict(backgroundColor="lightGrey", fontWeight="bold"),
                style_as_list_view=True,
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'Metric'},
                        'textAlign': 'left'
                    }
                ]
            )
        ]
    )]

    return stats_div


# Callback Functions
# ======================================================================================================================
@app.callback(
    Output("chats_dropdown", "options"),
    Input("platform_dropdown", "value"),
)
def change_subview_list(platform_choice):
    return [{"value": x, "label": x} for x in list(results[platform_choice].keys())]


@app.callback(
    Output("main_page", "children"),
    Input("platform_dropdown", "value"),
    Input("chats_dropdown", "value"),
)
def load_main_page(platform_choice, chats_choice):
    page_elements = []

    analyses = results[platform_choice][chats_choice]

    # Make Statistics Table
    page_elements.extend(make_stats_table(analyses["Statistics"]))

    return page_elements


def main():
    """ Main entry point of the script"""
    app.run_server(debug=True)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
