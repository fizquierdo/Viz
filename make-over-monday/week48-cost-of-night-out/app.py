import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = pd.read_excel('cost.xlsx')

options = list(set(df.Item))
default_options = ['2 Longdrinks', 'Big Mac', 'Taxi', 'Club entry']

app.layout = html.Div([
    html.H2('The cost of going out around the world'),
    html.H4('Cities are sorted by the sum of the cost of all possible activities'),
    dcc.Checklist(
        id='features-options',
        options=[{'label': x, 'value': x} for x in options],
        values=default_options,
        labelStyle={'display': 'inline-block', 'margin': '6px'}),
    html.Button(id='submit-button', n_clicks=0, children='Calculate'),
    dcc.Graph(id='heatmap'),
])


@app.callback(
    dash.dependencies.Output('heatmap', 'figure'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('features-options', 'values')]
)
def update_graph(n_clicks, values):
    dfp = df.pivot_table(index='City', columns='Item', values='Cost')
    dfp = dfp[options]
    dfp['Total'] = dfp.sum(axis=1)
    dfp = dfp.round(0).sort_values(by=['Total'])
    cities = list(dfp.index)
    return {
        'layout': go.Layout(title='Cost per activity in $'),
        'data': [go.Heatmap(
            x=values,
            y=cities,
            z=dfp[values].values)]
    }


if __name__ == '__main__':
    app.run_server(debug=True)
