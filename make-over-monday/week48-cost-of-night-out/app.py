import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = pd.read_excel('cost.xlsx')

options = list(set(df.Item))
default_options = ['2 Longdrinks', 'Big Mac', 'Taxi', 'Club entry']

app.layout = html.Div([
    html.H2('The cost of a night out in selected cities'),
    html.H4('Choose activities and compare the cost of a night out around the world'),
    dcc.Checklist(
        id='features-options',
        options=[{'label': x, 'value': x} for x in options],
        values=default_options,
        labelStyle={'display': 'inline-block', 'margin': '6px'}),
    html.Button(id='submit-button', n_clicks=0, children='Compare'),
    html.Div([
        html.Div([dcc.Graph(id='heatmap')], style={
             'width': '50%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='bars')], style={
            'width': '48%', 'display': 'inline-block'}),
    ])

])

# pivot for calculations
df = df.pivot_table(index='City', columns='Item', values='Cost')


def filter_activities(df, activities):
    dfp = df[activities]
    dfp['Total'] = dfp.sum(axis=1)
    dfp = dfp.round(0).sort_values(by=['Total'])
    cities = list(dfp.index)
    return (dfp, cities)


@app.callback(
    dash.dependencies.Output('bars', 'figure'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('features-options', 'values')]
)
def update_graph(n_clicks, activities):
    dfp, cities = filter_activities(df, activities)
    return {
        'data': [go.Bar(
            x=list(dfp['Total']),
            y=cities,
            orientation='h',
            marker=dict(color='rgba(190, 192, 213, 1)')
        )],
        'layout': go.Layout(
            title='Total cost ($)',
            paper_bgcolor='rgb(248, 248, 255)',
            plot_bgcolor='rgb(248, 248, 255)',
            yaxis=dict(automargin=True)
        )
    }


@app.callback(
    dash.dependencies.Output('heatmap', 'figure'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('features-options', 'values')]
)
def update_graph(n_clicks, activities):
    dfp, cities = filter_activities(df, activities)
    return {
        'layout': go.Layout(
            title='Cost per activity ($)',
            paper_bgcolor='rgb(248, 248, 255)',
            yaxis=dict(automargin=True)
        ),
        'data': [go.Heatmap(
            x=activities,
            y=cities,
            z=dfp[activities].values,
            colorscale='Reds')]
    }


if __name__ == '__main__':
    app.run_server(debug=True)
