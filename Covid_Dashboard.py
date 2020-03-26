# Importo le librerie necessarie

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import dash_table
import numpy as np
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Scheme, Sign, Symbol
import pycountry_convert as pc
import pycountry
import plotly.express as px
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

colonne_andamento = ['dimessi_guariti', "nuovi_attualmente_positivi", 'isolamento_domiciliare',
                     'ricoverati_con_sintomi', 'terapia_intensiva', 'deceduti', "totale_casi", "tamponi"]

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

index_dict = {'dimessi_guariti': "Dimessi e Guariti",
              'isolamento_domiciliare': "Isolamento Domiciliare",
              'ricoverati_con_sintomi': "Ricoverati",
              'terapia_intensiva': "Terapia Intensiva",
              'deceduti': "Deceduti",
              "nuovi_attualmente_positivi": "Nuovi Positivi",
              "totale_casi": "Totale Casi",
              "tamponi": "Tamponi",
              }

denom_geo = {'Campania': "Sud e Isole",
             'Molise': "Sud e Isole",
             'Puglia': "Sud e Isole",
             'P.A. Trento': "Nord",
             'Calabria': "Sud e Isole",
             'Emilia Romagna': "Nord",
             'Piemonte': "Nord",
             'Liguria': "Nord",
             'Friuli Venezia Giulia': "Nord",
             'Veneto': "Nord",
             'Lazio': "Centro",
             'Basilicata': "Sud e Isole",
             "Valle d'Aosta": "Nord",
             'P.A. Bolzano': "Nord",
             'Toscana': "Centro",
             'Abruzzo': "Sud e Isole",
             'Sardegna': "Sud e Isole",
             'Sicilia': "Sud e Isole",
             'Lombardia': "Nord",
             'Marche': "Centro",
             'Umbria': "Centro"}

# Leggo Df Province
prov_url = r"https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv"
provincia = pd.read_csv(prov_url, dtype=(dict(sigla_provincia=str)))
provincia = provincia[provincia["denominazione_provincia"].ne("In fase di definizione/aggiornamento")
                      & provincia["data"].ne("data")].copy()
provincia["data_range"] = pd.to_datetime(provincia["data"], errors="coerce")
provincia["data"] = provincia["data"].str[:10]

# Preparo Grafico totale data

totale_data = pd.pivot_table(data=regioni, index="data", aggfunc=np.sum)
totale_data.reset_index(inplace=True)
trace_1 = go.Scatter(
    x=totale_data["data"].unique(),
    y=totale_data["deceduti"],
    name="Deceduti",
    marker=dict(color="#000000"),
    mode="lines+markers",
)

trace_2 = go.Scatter(
    x=totale_data["data"].unique(),
    y=totale_data["terapia_intensiva"],
    name="Terapia Intensiva",
    marker=dict(color="#FF0000"),
    mode="lines+markers",
)

trace_3 = go.Scatter(
    x=totale_data["data"].unique(),
    y=totale_data["ricoverati_con_sintomi"],
    name="Ricoverati",
    marker=dict(color="#FF6600"),
    mode="lines+markers",
)

trace_4 = go.Scatter(
    x=totale_data["data"].unique(),
    y=totale_data["isolamento_domiciliare"],
    name="Isolamento Domiciliare",
    marker=dict(color="#FFCC00"),
    mode="lines+markers",
)

trace_5 = go.Scatter(
    x=totale_data["data"].unique(),
    y=totale_data["dimessi_guariti"],
    name="Guariti",
    marker=dict(color="#00FF00"),
    mode="lines+markers",
)

trace_6 = go.Scatter(
    x=totale_data["data"].unique(),
    y=totale_data["nuovi_attualmente_positivi"],
    name="Nuovi Casi",
    marker=dict(color="#FFFF00"),
    mode="lines+markers",
)

trace_7 = go.Scatter(
    x=totale_data["data"].unique(),
    y=totale_data["totale_attualmente_positivi"],
    name="Totale Attualmente Positivi",
    marker=dict(color="#9900FF"),
    mode="lines+markers",
)

data_tot = [trace_1, trace_2, trace_3, trace_4, trace_5, trace_6, trace_7]

tot_layout = go.Layout(
    title='Andamento Casi Totali per Data',
    xaxis=dict(title="Data Rilevazione"),
    yaxis=dict(title="Numero Casi")
)
# Preparo tabella scostamento totale
totale_data.set_index("data", inplace=True)
totale_var = totale_data[colonne_andamento]
totale_var.fillna(0).sort_index(ascending=False).head().style.background_gradient(cmap='coolwarm')
oggi_ieri = totale_var.iloc[-2:]
differenza = oggi_ieri.diff()[1:2].transpose()
latest = oggi_ieri.transpose()
merge_var = pd.merge(left=latest, right=differenza, how="left", left_on=latest.index, right_on=differenza.index)
merge_var.set_index("key_0", inplace=True)
merge_var.rename(index=index_dict, inplace=True)
merge_var.columns = [merge_var.columns[0], merge_var.columns[1][:10], "Var. Assoluta"]
merge_var.index.name = ""
ieri = merge_var.columns[0]
merge_var["Var. Percentuale"] = merge_var["Var. Assoluta"].div(merge_var[ieri])
merge_var.reset_index(inplace=True)

# preparo tabella e grafico nuovi positivi
nuovi_positivi = pd.pivot_table(regioni, index=["data"], aggfunc={"nuovi_attualmente_positivi": np.sum})
data_new = [go.Bar(
    x=nuovi_positivi.index,
    y=nuovi_positivi["nuovi_attualmente_positivi"],
    text=nuovi_positivi["nuovi_attualmente_positivi"],
    hoverinfo="text",
    textposition="outside",
    marker={'color': nuovi_positivi["nuovi_attualmente_positivi"],
            'colorscale': 'Sunset'}
)]

layout_new = go.Layout(
    title="Nuovi Casi Positivi per Data",
    xaxis=dict(title="Data Rilevazione"),
    yaxis=dict(title="Numero Casi"),

)

# Preparo Grafico e tabella andamento area geografica
regioni["denom_geo"] = regioni["denominazione_regione"].map(denom_geo)
tot_area_geo = regioni[regioni["data"].eq(str(regioni["data_range"].max())[:10])] \
    .sort_values(["totale_casi"], ascending=False).reset_index(drop=False)
tot_area_geo_piv = pd.pivot_table(data=tot_area_geo, index="denom_geo", aggfunc=np.sum).sort_values(by="totale_casi",
                                                                                                    ascending=False)
data_geo_bar = [go.Bar(
    x=tot_area_geo_piv.index.unique(),
    y=tot_area_geo_piv[col],
    name=legenda_dict[col],
    marker=dict(color=colori_dict[col]),
    text=tot_area_geo_piv[col],
    textposition="auto",
    hoverinfo="text"
) for col in colonne]

layout_geo_bar = go.Layout(
    title='Composizione Casi Totali per Area Geografica',
    barmode='stack',
    xaxis=dict(title="Area Geografica"),
    yaxis=dict(title="Numero Casi"),
)

# line graph
regioni_area_geo = pd.pivot_table(data=regioni, index=["data", "denom_geo"], aggfunc=np.sum).reset_index()

data_geo_chart = [go.Scatter(
    x=regioni_area_geo["data"].unique(),
    y=regioni_area_geo[regioni_area_geo["denom_geo"].eq(area)]["nuovi_attualmente_positivi"],
    mode="lines+markers",
    name=area) for area in regioni["denom_geo"].unique()]

layout_geo_chart = go.Layout(
    title="Andamento Nuovi Casi Positivi per Area Geografica",
    xaxis=dict(title="Data Rilevazione"),
    yaxis=dict(title="Numero Casi Positivi"),
)

# leggo df andamento globale
state_data = pd.read_csv(r"https://covid.ourworldindata.org/data/ecdc/full_data.csv")
state_data = state_data[state_data["total_cases"].ge(500)]
# imposto opzioni per drop down
country_options = [{"label": country, "value": country} for country in state_data["location"].unique()]

# costruisco colonna "days_since"
nuovo_df = pd.DataFrame()
for location in state_data["location"].unique():
    df_temp = state_data[state_data["location"].eq(location)].copy()
    df_temp["days_since"] = np.arange(len(df_temp))
    nuovo_df = pd.concat([nuovo_df, df_temp])

""""# preparo dati e realizzo scatter geo

df_geo = pd.read_csv(r"https://covid.ourworldindata.org/data/ecdc/full_data.csv")

country_list = []
i = 0

while i < len(list(pycountry.countries)):
    country_list.append(list(pycountry.countries)[i].__getattr__("name"))
    i += 1

df_geo = df_geo[df_geo["location"].isin(country_list)].copy()
country_dict = dict([(country,pc.country_name_to_country_alpha3(country ,cn_name_format="default")) for country in df_geo["location"].unique()])
df_geo["alpha"] = df_geo["location"].map(country_dict)
df_geo["datetime"] = pd.to_datetime(df_geo["date"])
df_geo = df_geo[df_geo["datetime"].ge("01-01-2020")]
df_geo["week"] = df_geo['datetime'].dt.strftime('%U').astype(int)
df_geo.sort_values(by="week", ascending=True, inplace=True)
fig_geo_map = px.scatter_geo(df_geo,
                         locations="alpha",
                         color="location",
                         hover_name="location",
                         size="total_cases",
                         animation_frame="week",
                         projection="natural earth")"""

# Faccio Setup del Layout con Header, Input Box e grafico

app.layout = html.Div([
    # Imposto titolo della dashboard
    html.H1("Dashboard Andamento Covid 19", style={"textAlign": "center"}),
    # Divido la dashboard in Tabs
    dcc.Tabs(id="tabs", children=[
        # Imposto layout primo tab
        dcc.Tab(label="Riassunto Andamento Nazionale", children=[
            html.Div([
                # Imposto titolo della tabella
                html.H2("Tabella di Sintesi aggiornata al {}".format(str(regioni["data_range"].max())[:10]),
                        style={"textAlign": "center"}),
                dash_table.DataTable(
                    style_cell={'textAlign': 'right'},
                    style_data={
                        'whiteSpace': 'normal',
                    },
                    style_cell_conditional=[
                        {
                            'if': {'column_id': merge_var.columns[0]},
                            'textAlign': 'right',
                            "fontWeight": "bold",

                        },
                        {
                            'if': {'column_id': 'Var. Assoluta'},
                            'textAlign': 'center'
                        },
                        {
                            'if': {'column_id': 'Var. Percentuale'},
                            'textAlign': 'center'
                        },
                        {
                            'if': {'column_id': merge_var.columns[1]},
                            'textAlign': 'center'
                        },
                        {
                            'if': {'column_id': merge_var.columns[2]},
                            'textAlign': 'center'
                        }
                    ],
                    id="table",
                    columns=[{
                        'id': merge_var.columns[0],
                        'name': merge_var.columns[0],
                        'type': 'text'
                    }, {
                        'id': merge_var.columns[1],
                        'name': merge_var.columns[1],
                        'type': 'numeric',
                        'format': Format(group=',')
                    }, {
                        'id': merge_var.columns[2],
                        'name': merge_var.columns[2],
                        'type': 'numeric',
                        'format': Format(group=',')
                    }, {
                        'id': merge_var.columns[3],
                        'name': merge_var.columns[3],
                        'type': 'numeric',
                        'format': Format(group=',')
                    }, {
                        'id': merge_var.columns[4],
                        'name': merge_var.columns[4],
                        'type': 'numeric',
                        'format': FormatTemplate.percentage(2).sign(Sign.positive),
                    },

                    ],
                    data=merge_var.to_dict("records")
                ),
                dcc.Graph(id="my_case_new",
                          figure={
                              "data": data_new,
                              "layout": layout_new,
                          }
                          ),
                dcc.Graph(id="my_graph_total",
                          figure={
                              "data": data_tot,
                              "layout": tot_layout,
                          }
                          ),
            ])
        ]),
        # Imposto layout Tab Province
        dcc.Tab(label="Analisi Singola Regione / Province", children=[
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
            dcc.Graph(id="my_bar_chart"),
            dcc.Graph(id="my_province_chart"),
            dcc.Graph(id="my_graph"),
        ]),
        # Imposto layout tab regioni
        dcc.Tab(label="Confronto Tra Regioni", children=[
            # Div che contiene il selezionatore della regione
            html.Div([
                html.H3("Seleziona una Regione:", style={"paddingRight": "30px"}),
                dcc.Dropdown(
                    id="my_region_2",
                    options=options,
                    value=["Lombardia", "Campania", "Emilia Romagna", "Veneto", "Piemonte"],
                    multi=True
                ),

            ], style={"display": "inline-block", "verticalAlign": "top", "width": "40%"}),
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
            dcc.Graph(id="my_graph_2", ),
            dcc.Graph(id="my_graph_3", ),
            dcc.Graph(id="my_graph_4", ),
            dcc.Graph(id="my_graph_5", ),
            dcc.Graph(id="my_graph_6", ),
            dcc.Graph(id="my_graph_7", ),
            dcc.Graph(id="my_graph_8", ),

        ]),
        dcc.Tab(label="Confronto per Area Geografica", children=[
            dcc.Graph(id="geo_chart",
                      figure={
                          "data": data_geo_chart,
                          "layout": layout_geo_chart,
                      }
                      ),
            dcc.Graph(id="geo_bar",
                      figure={
                          "data": data_geo_bar,
                          "layout": layout_geo_bar,
                      }),
        ]),
        # Imposto layout tab internazionale
        dcc.Tab(label="Andamento Globale", children=[
            # Div che contiene il selezionatore della regione
            html.Div([
                html.H3("Seleziona una Nazione:", style={"paddingRight": "30px"}),
                dcc.Dropdown(
                    id="my_state",
                    options=country_options,
                    value=["China", "Italy", "United States", "Spain", "France"],
                    multi=True
                ),

            ], style={"display": "inline-block", "verticalAlign": "top", "width": "40%"}),
            # aggiungo i grafici

            dcc.Graph(id="my_state_1"),
#            html.H2("Evoluzione Totale casi attivi dal 01-01-2020",
#                    style={"textAlign": "center"}),
#            dcc.Graph(id="my_map", figure=fig_geo_map),
            dcc.Graph(id="my_state_2"),
            dcc.Graph(id="my_state_3"),
            dcc.Graph(id="my_state_4"),
        ]),
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
    Output("my_province_chart", "figure"),
    [Input("submit-button", "n_clicks")],
    [State("my_region", "value"),
     State("my_date_picker", "start_date"),
     State("my_date_picker", "end_date")]
)
def update_province(n_clicks, region, start_date, end_date):
    # creo dataframe specifico con la regione selezionata:
    df_prov = provincia[provincia["denominazione_regione"].eq(region)
                        & provincia["data_range"].ge(start_date)
                        & provincia["data_range"].le(end_date)]
    prov_piv = pd.pivot_table(df_prov, index=["data", "denominazione_provincia"],
                              aggfunc={"totale_casi": np.sum}).sort_values(
        by=["totale_casi", "denominazione_provincia"],
        ascending=False)
    prov_piv.reset_index(inplace=True)

    prov_graph = [go.Bar(
        x=prov_piv["data"].unique(),
        y=prov_piv[prov_piv["denominazione_provincia"].eq(prov)]["totale_casi"],
        name=prov,
    ) for prov in prov_piv["denominazione_provincia"].unique()]

    prov_layout = go.Layout(
        title="Andamento Totale Casi Positivi per Provincia in: " + region,
        xaxis=dict(title="Data Rilevazione"),
        yaxis=dict(title="Numero Totale Casi"),
        barmode="stack"
    )

    fig = {
        "data": prov_graph,
        "layout": prov_layout
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
        yaxis=dict(title="Numero Casi Attualmente Positivi"),
    )

    graph_2 = {
        "data": data,
        "layout": layout_regione
    }
    return graph_2


@app.callback(
    Output("my_graph_3", "figure"),
    [Input("submit-button_2", "n_clicks")],
    [State("my_region_2", "value"),
     State("my_date_picker_2", "start_date"),
     State("my_date_picker_2", "end_date")]
)
def update_graph_3(n_clicks, region_list, start_date, end_date):
    # creo dataframe specifico con la regione selezionata:
    df_region = regioni[regioni["denominazione_regione"].isin(region_list)
                        & regioni["data_range"].ge(start_date)
                        & regioni["data_range"].le(end_date)]
    data = []
    for regione in region_list:
        trace = go.Scatter(
            x=df_region["data"].unique(),
            y=df_region[df_region["denominazione_regione"].eq(regione)]["deceduti"],
            mode="lines+markers",
            name=regione)
        data.append(trace)

    layout_regione = go.Layout(
        title="Andamento Decessi per Regione",
        xaxis=dict(title="Data Rilevazione"),
        yaxis=dict(title="Numero Decessi"),
    )

    graph_3 = {
        "data": data,
        "layout": layout_regione
    }
    return graph_3


@app.callback(
    Output("my_graph_4", "figure"),
    [Input("submit-button_2", "n_clicks")],
    [State("my_region_2", "value"),
     State("my_date_picker_2", "start_date"),
     State("my_date_picker_2", "end_date")]
)
def update_graph_4(n_clicks, region_list, start_date, end_date):
    # creo dataframe specifico con la regione selezionata:
    df_region = regioni[regioni["denominazione_regione"].isin(region_list)
                        & regioni["data_range"].ge(start_date)
                        & regioni["data_range"].le(end_date)]
    data = []
    for regione in region_list:
        trace = go.Scatter(
            x=df_region["data"].unique(),
            y=df_region[df_region["denominazione_regione"].eq(regione)]["dimessi_guariti"],
            mode="lines+markers",
            name=regione)
        data.append(trace)

    layout_regione = go.Layout(
        title="Andamento Dimessi Guariti per Regione",
        xaxis=dict(title="Data Rilevazione"),
        yaxis=dict(title="Numero Dimessi Guariti"),
    )

    graph_4 = {
        "data": data,
        "layout": layout_regione
    }
    return graph_4


@app.callback(
    Output("my_graph_5", "figure"),
    [Input("submit-button_2", "n_clicks")],
    [State("my_region_2", "value"),
     State("my_date_picker_2", "start_date"),
     State("my_date_picker_2", "end_date")]
)
def update_graph_5(n_clicks, region_list, start_date, end_date):
    # creo dataframe specifico con la regione selezionata:
    df_region = regioni[regioni["denominazione_regione"].isin(region_list)
                        & regioni["data_range"].ge(start_date)
                        & regioni["data_range"].le(end_date)]
    data = []
    for regione in region_list:
        trace = go.Scatter(
            x=df_region["data"].unique(),
            y=df_region[df_region["denominazione_regione"].eq(regione)]["terapia_intensiva"],
            mode="lines+markers",
            name=regione)
        data.append(trace)

    layout_regione = go.Layout(
        title="Andamento Ricoverati in Terapia Intensiva per Regione",
        xaxis=dict(title="Data Rilevazione"),
        yaxis=dict(title="Numero Ricoverati in Terapia Intensiva"),
    )

    graph_5 = {
        "data": data,
        "layout": layout_regione
    }
    return graph_5


@app.callback(
    Output("my_graph_6", "figure"),
    [Input("submit-button_2", "n_clicks")],
    [State("my_region_2", "value"),
     State("my_date_picker_2", "start_date"),
     State("my_date_picker_2", "end_date")]
)
def update_graph_6(n_clicks, region_list, start_date, end_date):
    # creo dataframe specifico con la regione selezionata:
    df_region = regioni[regioni["denominazione_regione"].isin(region_list)
                        & regioni["data_range"].ge(start_date)
                        & regioni["data_range"].le(end_date)]
    data = []
    for regione in region_list:
        trace = go.Scatter(
            x=df_region["data"].unique(),
            y=df_region[df_region["denominazione_regione"].eq(regione)]["ricoverati_con_sintomi"],
            mode="lines+markers",
            name=regione)
        data.append(trace)

    layout_regione = go.Layout(
        title="Andamento Ricoverati con Sintomi per Regione",
        xaxis=dict(title="Data Rilevazione"),
        yaxis=dict(title="Numero Ricoverati con Sintomi"),
    )

    graph_6 = {
        "data": data,
        "layout": layout_regione
    }
    return graph_6


@app.callback(
    Output("my_graph_7", "figure"),
    [Input("submit-button_2", "n_clicks")],
    [State("my_region_2", "value"),
     State("my_date_picker_2", "start_date"),
     State("my_date_picker_2", "end_date")]
)
def update_graph_7(n_clicks, region_list, start_date, end_date):
    # creo dataframe specifico con la regione selezionata:
    df_region = regioni[regioni["denominazione_regione"].isin(region_list)
                        & regioni["data_range"].ge(start_date)
                        & regioni["data_range"].le(end_date)]
    data = []
    for regione in region_list:
        trace = go.Scatter(
            x=df_region["data"].unique(),
            y=df_region[df_region["denominazione_regione"].eq(regione)]["isolamento_domiciliare"],
            mode="lines+markers",
            name=regione)
        data.append(trace)

    layout_regione = go.Layout(
        title="Andamento Isolamento Domiciliare per Regione",
        xaxis=dict(title="Data Rilevazione"),
        yaxis=dict(title="Numero di Pazienti in Isolamento"),
    )

    graph_7 = {
        "data": data,
        "layout": layout_regione
    }
    return graph_7


@app.callback(
    Output("my_graph_8", "figure"),
    [Input("submit-button_2", "n_clicks")],
    [State("my_region_2", "value"),
     State("my_date_picker_2", "start_date"),
     State("my_date_picker_2", "end_date")]
)
def update_graph_8(n_clicks, region_list, start_date, end_date):
    # creo dataframe specifico con la regione selezionata:
    df_region = regioni[regioni["denominazione_regione"].isin(region_list)
                        & regioni["data_range"].ge(start_date)
                        & regioni["data_range"].le(end_date)]
    data = []
    for regione in region_list:
        trace = go.Scatter(
            x=df_region["data"].unique(),
            y=df_region[df_region["denominazione_regione"].eq(regione)]["nuovi_attualmente_positivi"],
            mode="lines+markers",
            name=regione)
        data.append(trace)

    layout_regione = go.Layout(
        title="Andamento Nuovi Casi Positivi per Regione",
        xaxis=dict(title="Data Rilevazione"),
        yaxis=dict(title="Numero Nuovi Casi"),
    )

    graph_8 = {
        "data": data,
        "layout": layout_regione
    }
    return graph_8


@app.callback(
    Output("my_state_1", "figure"),
    [Input("my_state", "value")],
)
def update_state_1(state):
    # creo dataframe specifico con la regione selezionata:

    state_graph = [go.Scatter(
        x=nuovo_df[nuovo_df["location"].eq(country)]["days_since"],
        y=nuovo_df[nuovo_df["location"].eq(country)]["total_cases"],
        mode="lines+markers",
        name=country,
    ) for country in state]

    fig = {
        "data": state_graph,
        "layout": {"title": "Andamento dei casi Totali di Covid",
                   "xaxis": dict(title="Giorni Trascorsi dal 500mo Caso Rilevato"),
                   "yaxis": dict(title="Numero Casi")}
    }
    return fig


@app.callback(
    Output("my_state_2", "figure"),
    [Input("my_state", "value")],
)
def update_state_2(state):
    # creo dataframe specifico con la regione selezionata:

    state_graph = [go.Scatter(
        x=nuovo_df[nuovo_df["location"].eq(country)]["days_since"],
        y=nuovo_df[nuovo_df["location"].eq(country)]["total_deaths"],
        mode="lines+markers",
        name=country,
    ) for country in state]

    fig = {
        "data": state_graph,
        "layout": {"title": "Andamento dei Decessi Totali per Covid",
                   "xaxis": dict(title="Giorni Trascorsi dal 500mo Caso Rilevato"),
                   "yaxis": dict(title="Numero Casi")}
    }
    return fig


@app.callback(
    Output("my_state_3", "figure"),
    [Input("my_state", "value")],
)
def update_state_3(state):
    # creo dataframe specifico con la regione selezionata:

    state_graph = [go.Scatter(
        x=nuovo_df[nuovo_df["location"].eq(country)]["days_since"],
        y=nuovo_df[nuovo_df["location"].eq(country)]["new_cases"],
        mode="lines+markers",
        name=country,
    ) for country in state]

    fig = {
        "data": state_graph,
        "layout": {"title": "Andamento dei Nuovi Casi di Covid",
                   "xaxis": dict(title="Giorni Trascorsi dal 500mo Caso Rilevato"),
                   "yaxis": dict(title="Numero Casi")}
    }
    return fig


@app.callback(
    Output("my_state_4", "figure"),
    [Input("my_state", "value")],
)
def update_state_4(state):
    # creo dataframe specifico con la regione selezionata:

    state_graph = [go.Scatter(
        x=nuovo_df[nuovo_df["location"].eq(country)]["days_since"],
        y=nuovo_df[nuovo_df["location"].eq(country)]["new_deaths"],
        mode="lines+markers",
        name=country,
    ) for country in state]

    fig = {
        "data": state_graph,
        "layout": {"title": "Andamento dei Nuovi Decessi per Covid",
                   "xaxis": dict(title="Giorni Trascorsi dal 500mo Caso Rilevato"),
                   "yaxis": dict(title="Numero Casi")}
    }
    return fig


# Setup server clause

if __name__ == "__main__":
    app.run_server()
