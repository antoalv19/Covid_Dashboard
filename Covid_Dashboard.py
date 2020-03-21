# Importo le librerie necessarie

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import dash_auth

# imposto account
# USERNAME_PASSWORD_PAIRS = [
#    ['endony', 'endony'], ["mamama", "endony"], ["covid19", "cocchino"]]
# lancio istanza dell'App

app = dash.Dash()
# auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server

# leggo DataFrame Regioni
url_regioni = r"https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"

regioni = pd.read_csv(url_regioni, dtype={'dimessi_guariti': int,
                                          'isolamento_domiciliare': int,
                                          'ricoverati_con_sintomi': int,
                                          'terapia_intensiva': int,
                                          'deceduti': int,
                                          "nuovi_attualmente_positivi": int,
                                          "totale_casi": int,
                                          "tamponi": int, })

regioni["data_time"] = pd.to_datetime(regioni["data"])
regioni["data_range"] = pd.to_datetime(regioni["data"])
regioni["data_time"] = regioni["data"].astype(str)
regioni["data"] = regioni["data_time"].str[:10]

options = [{"label": regione, "value": regione} for regione in regioni["denominazione_regione"].unique()]

colonne = ['dimessi_guariti', 'isolamento_domiciliare', 'ricoverati_con_sintomi', 'terapia_intensiva', 'deceduti']

legenda_dict = {
    "dimessi_guariti": "Dimessi",
    "nuovi_attualmente_positivi": "Nuovi Positivi",
    "isolamento_domiciliare": "Isolamento Domiciliare",
    "ricoverati_con_sintomi": "Ricoverati",
    "terapia_intensiva": "Terapia Intensiva",
    "deceduti": "Deceduti",
    "totale_casi": "Totale Casi",
}

colori_dict = {
    "dimessi_guariti": "#00FF00",
    "nuovi_attualmente_positivi": "#FFFF00",
    "isolamento_domiciliare": "#FFCC00",
    "ricoverati_con_sintomi": "#FF6600",
    "terapia_intensiva": "#FF0000",
    "deceduti": "#000000",
    "totale_casi": "#9900FF",
    "totale_attualmente_positivi": "#9900FF",
}
# Faccio Setup del Layout con Header, Input Box e grafico

app.layout = html.Div([
    # Imposto titolo della dashboard
    html.H1("Dashboard Andamento Covid 19", style={"textAlign": "center"}),
    # Divido la dashboard in Tabs
    dcc.Tabs(id="tabs", children=[
        # Imposto layout primo Tab
        dcc.Tab(label="Analisi Singola Regione", children=[
            # Div che contiene il selezionatore della regione
            html.Div([
                html.H3("Seleziona una Regione:", style={"paddingRight": "30px"}),
                dcc.Dropdown(
                    id="my_region",
                    options=options,
                    value="Lombardia",
                ),

            ], style={"display": "inline-block", "verticalAlign": "top", "width": "20%"}),
            # aggiungo un Div per contenere il date picker
            html.Div([
                html.H3("Seleziona un range di date:"),
                dcc.DatePickerRange(
                    id="my_date_picker",
                    min_date_allowed=regioni["data_range"].min(),
                    max_date_allowed=datetime.today(),
                    start_date=regioni["data_range"].min(),
                    end_date=datetime.today(),
                )
            ], style={"display": "inline-block"}),
            html.Div([
                html.Button(
                    id="submit-button",
                    n_clicks=0,
                    children="Aggiorna",
                    style={"fontSize": 24, "marginLeft": "30px"}
                ),
            ], style={"display": "inline-block"}
            ),
            dcc.Graph(id="my_graph"),
            dcc.Graph(id="my_bar_chart",
                      figure={
                          "data": [
                              {"x": [1, 2], "y": [3, 1]}
                          ]
                      }
                      ),
        ]),
        dcc.Tab(label="Confronto Tra Regioni", children=[
            # Div che contiene il selezionatore della regione
            html.Div([
                html.H3("Seleziona una Regione:", style={"paddingRight": "30px"}),
                dcc.Dropdown(
                    id="my_region_2",
                    options=options,
                    value=["Lombardia", "Campania"],
                    multi=True
                ),

            ], style={"display": "inline-block", "verticalAlign": "top", "width": "20%"}),
            # aggiungo un Div per contenere il date picker
            html.Div([
                html.H3("Seleziona un range di date:"),
                dcc.DatePickerRange(
                    id="my_date_picker_2",
                    min_date_allowed=regioni["data_range"].min(),
                    max_date_allowed=datetime.today(),
                    start_date=regioni["data_range"].min(),
                    end_date=datetime.today(),
                )
            ], style={"display": "inline-block"}),
            html.Div([
                html.Button(
                    id="submit-button_2",
                    n_clicks=0,
                    children="Aggiorna",
                    style={"fontSize": 24, "marginLeft": "30px"}
                ),
            ], style={"display": "inline-block"}
            ),
            dcc.Graph(id="my_graph_2",
                      figure={
                          "data": [
                              {"x": [1, 2], "y": [3, 1]}
                          ]
                      }
                      ),

        ])
    ])
])


# Aggiungo CallBack per aggiornare il titolo del grafico

@app.callback(
    Output("my_graph", "figure"),
    [Input("submit-button", "n_clicks")],
    [State("my_region", "value"),
     State("my_date_picker", "start_date"),
     State("my_date_picker", "end_date")]
)
def update_graph(n_clicks, region, start_date, end_date):
    # creo dataframe specifico con la regione selezionata:
    df_region = regioni[regioni["denominazione_regione"].eq(region)
                        & regioni["data_range"].ge(start_date)
                        & regioni["data_range"].le(end_date)]
    traces = []
    for col in colonne:
        traces.append({"x": df_region["data"],
                       "y": df_region[col],
                       "name": legenda_dict[col],
                       "mode": "lines+markers",
                       "marker": dict(color=colori_dict[col])
                       })

    fig = {
        "data": traces,
        "layout": {"title": "Andamento dei casi di Covid in: " + region,
                   "xaxis": dict(title="Data"),
                   "yaxis": dict(title="Numero Casi")}
    }
    return fig


@app.callback(
    Output("my_bar_chart", "figure"),
    [Input("submit-button", "n_clicks")],
    [State("my_region", "value"),
     State("my_date_picker", "start_date"),
     State("my_date_picker", "end_date")]
)
def update_bar_chart(n_clicks, region, start_date, end_date):
    # creo dataframe specifico con la regione selezionata:
    df_region = regioni[regioni["denominazione_regione"].eq(region)
                        & regioni["data_range"].ge(start_date)
                        & regioni["data_range"].le(end_date)]
    barre = []
    for col in colonne:
        barre.append(
            go.Bar(
                x=df_region["data"],
                y=df_region[col],
                name=legenda_dict[col],
                marker=dict(color=colori_dict[col]))
        )

    layout = go.Layout(
        title="Composizione dei casi di Covid in: " + region,
        barmode='stack',
        xaxis=dict(title="Data"),
        yaxis=dict(title="Numero Casi"),
    )

    bar_chart = {
        "data": barre,
        "layout": layout
    }
    return bar_chart


@app.callback(
    Output("my_graph_2", "figure"),
    [Input("submit-button_2", "n_clicks")],
    [State("my_region_2", "value"),
     State("my_date_picker_2", "start_date"),
     State("my_date_picker_2", "end_date")]
)
def update_graph_2(n_clicks, region_list, start_date, end_date):
    # creo dataframe specifico con la regione selezionata:
    df_region = regioni[regioni["denominazione_regione"].isin(region_list)
                        & regioni["data_range"].ge(start_date)
                        & regioni["data_range"].le(end_date)]
    data = []
    for regione in region_list:
        trace = go.Scatter(
            x=df_region["data"].unique(),
            y=df_region[df_region["denominazione_regione"].eq(regione)]["totale_attualmente_positivi"],
            mode="lines+markers",
            name=regione)
        data.append(trace)

    layout_regione = go.Layout(
        title="Andamento Casi Positivi per Regione",
        xaxis=dict(title="Data Rilevazione"),
        yaxis=dict(title="Numero Casi Positivi"),
        hovermode="closest"
    )

    graph_2 = {
        "data": data,
        "layout": layout_regione
    }
    return graph_2


# Setup server clause

if __name__ == "__main__":
    app.run_server()
