

import dash
import dash_table
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.exceptions import PreventUpdate
import time
import os
import stat

session_file_path = "./session_items.log"

def read_session_file():

    '''
    Display all historic sesssions
    :return:
    '''
    f = open(session_file_path)
    lines = f.readlines()
    session_history = []
    max_num_url = 0
    for line in lines:
        session_history.append(line.split(','))
        max_num_url = max(max_num_url,len(line.split(',')))
    print('found number websites visited: ',len(session_history))
    for i in range(len(lines)):
        add_sessions = max_num_url - len(session_history[i])
        for j in range(add_sessions):
            session_history[i].append('')

    df_session_history = pd.DataFrame(session_history)
    df_session_history.columns = ['visit'+str(i+1) for i in df_session_history.columns]

    #df_session_history = df_session_history.transpose()
    #df_session_history = df_session_history[df_session_history.columns[-1]].to_frame().reset_index()
    #df_session_history.columns = [i for i in range(len(df_session_history.columns))]

    return df_session_history

def read_session_file2():

    f = open(session_file_path)
    lines = f.readlines()
    session_history = []
    for i,line in enumerate(lines[::-1]):
        session_history.append(line.split(','))
        if i>0:
            break
    df = pd.DataFrame(session_history).T
    df.columns = ['URL','Page']
    df['Page'] = df.index
    df = df[['Page','URL']]

    #df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv').iloc[0].to_frame()

    print(df.head())


    return df



df= read_session_file2()

app = dash.Dash(__name__)

app.layout = html.Div(children=[

    html.H1(children='Web User Tracking Dashboard', style={'textAlign': 'center', 'padding': '50px',
                                                        'backgroundColor': '#557A95', 'color': 'white',
                                                        'font-family': 'sans-serif', 'font-size': 40, 'float': 'center',
                                                        'width': '86%'}),
    html.Div(id='table',children=[
        dash_table.DataTable(
            id='table_dash',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
        )
    ]),
    dcc.Interval(id='interval-component', interval=20_000)
    ])

@app.callback(
    output=dash.dependencies.Output('table', 'children'),
    inputs=[dash.dependencies.Input('interval-component', 'n_intervals')])
def update_table(n_intervals):
    if not n_intervals:
        raise PreventUpdate

    how_long_ago = time.time() - os.stat(session_file_path)[stat.ST_MTIME]

    # specify for how long no update will be checked! in seconds
    #if how_long_ago > 10:
    #    raise PreventUpdate
    print('update tables')

    df= read_session_file2()
    print(df)

    return [dash_table.DataTable(
        id='table_dash',
        columns=[{"name": str(i), "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_cell={'textAlign': 'left'})]


if __name__ == '__main__':
    app.run_server(debug=True)