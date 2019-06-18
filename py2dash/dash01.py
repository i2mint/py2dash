# from sklearn.tree import DecisionTreeRegressor
#
# func = DecisionTreeRegressor

# -*- coding: utf-8 -*-
import os
import dash
import dash_core_components as dcc
import dash_html_components as hc
from dash.dependencies import Input, Output, State

from otolite.skdash.util import extract_name_and_default, SignatureExtractor
from py2dash.component_makers import div_list_from_func
from py2dash.component_makers import dropdown_from_list

from otolite.skdash.controller import Controller, estimators
from otolite.skdash.controller import run_model

from py2dash.util import Ids

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# app = dash.Dash(__name__)
# app.css.append_css({'relative_package_path': 'bWLwgP.css'})

extract_signature = SignatureExtractor(attrs=('name', 'default', 'annotation'))

undefined = extract_name_and_default(dcc.Input)[0]['default']

# func = LinearRegression
# func = DecisionTreeRegressor
func = run_model

div_list = div_list_from_func(func)
if func == run_model:
    div_list.extend([
        hc.Button(id='submit-button', n_clicks=0, children='Submit'),
        hc.Div(id='output-state')])

# app.layout = html.Div(div_list, style={'columnCount': 2})


ids = Ids()

app.layout = hc.Div([
    hc.Div([
        hc.Label('Learner Kind'),
        dropdown_from_list(Controller.list_learner_kinds(), id=ids.learner_kind)]),
    hc.Div(id=ids.end_of_page)
])


@app.callback(
    Output(ids.end_of_page, 'children'),
    [Input(ids.learner_kind, 'value')]
)
def update_output_div(input_val):
    div_list = div_list_from_func(dict(estimators)[input_val])
    return div_list + [hc.P(), hc.Button(id='submit_button', n_clicks=0, children='Submit')]


@app.callback(
    Output(ids.end_of_page, 'children'),
    [Input(ids.learner_kind, 'value')]
)
def submit_estimator_params(input_val):
    div_list = div_list_from_func(dict(estimators)[input_val])
    return div_list + [hc.P(), hc.Button(id=ids.submit_button, n_clicks=0, children='Submit')]


def ensure_bool(x):
    if isinstance(x, bool):
        return x
    else:
        if isinstance(x, str):
            if x.lower().startswith('t'):
                return True
            elif x.lower().startswith('f'):
                return False
        elif isinstance(x, int):
            return bool(x)
    raise ValueError(f"Couldn't convert to a boolean: {x}")


# if func == run_model:
#     sig = extract_signature(func)
#     states = [State(x['name'], 'value') for x in extract_signature(func)]
#
#
#     # wrapper = app.callback(Output('output-state', 'children'),
#     #                        [Input('submit-button', 'n_clicks')],
#     #                       states)
#     # wrapped_func = wrapper(func)
#     @app.callback(Output('output-state', 'children'),
#                   [Input('submit-button', 'n_clicks')],
#                   states)
#     def run_model(tmp, n_clicks, mall_name, model_name: str, xy_name: str, method: str = 'predict', return_y: bool = False):
#         return_y = ensure_bool(return_y)
#         return Controller(mall_name).run_model(model_name, xy_name, method=method, return_y=return_y)
# else:
#     wrapped_func = func


# app.layout = html.Div([
#
#     daq.ToggleSwitch(
#         id='my-toggle-switch',
#         value=False,
#
#     ),
#     html.Div(id='toggle-switch-output'),
#
#     html.Label('Radio Items'),
#     dcc.RadioItems(
#         options=[
#             {'label': 'New York City', 'value': 'NYC'},
#             {'label': u'Montréal', 'value': 'MTL'},
#             {'label': 'San Francisco', 'value': 'SF'}
#         ],
#         value='MTL'
#     ),
#
#     html.Label('Checkboxes'),
#     dcc.Checklist(
#         options=[
#             {'label': 'New York City', 'value': 'NYC'},
#             {'label': u'Montréal', 'value': 'MTL'},
#             {'label': 'San Francisco', 'value': 'SF'}
#         ],
#         values=['MTL', 'SF']
#     ),
#
#     html.Label('Text Input'),
#     dcc.Input(value='MTL', type='text'),
#
#     html.Label('Slider'),
#     dcc.Slider(
#         min=0,
#         max=9,
#         marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
#         value=5,
#     ),
# ], style={'columnCount': 2})

if __name__ == '__main__':
    app.run_server(debug=True)