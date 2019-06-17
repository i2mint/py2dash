from otolite.skdash.controller import Controller, estimators
# from sklearn.tree import DecisionTreeRegressor
#
# func = DecisionTreeRegressor

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as dhc
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from otolite.skdash.util import extract_name_and_default, SignatureExtractor

extract_signature = SignatureExtractor(attrs=('name', 'default', 'annotation'))

undefined = extract_name_and_default(dcc.Input)[0]['default']

from py2dash.component_makers import div_list_from_func
from py2dash.component_makers import dropdown_from_list

from otolite.skdash.controller import run_model

# func = LinearRegression
# func = DecisionTreeRegressor
func = run_model

div_list = div_list_from_func(func)
if func == run_model:
    div_list.extend([
        dhc.Button(id='submit-button', n_clicks=0, children='Submit'),
        dhc.Div(id='output-state')])


# app.layout = html.Div(div_list, style={'columnCount': 2})


class Ids:
    def __init__(self, _attrs=()):
        self._attrs = list(_attrs)

    def __getattr__(self, _id):
        if isinstance(_id, self.__class__):
            _id = _id._id
        assert isinstance(_id, str), "_id should be a string"
        if _id not in self._attrs:
            setattr(self, _id, _id)
            self._attrs.append(_id)

        return _id

    def __dir__(self):  # to see attr in autocompletion
        return self._attrs

    def __iter__(self):
        yield from self._attrs


ids = Ids()

app.layout = dhc.Div([
    dhc.Div([
        dhc.Label('Learner Kind'),
        dropdown_from_list(Controller.list_learner_kinds(), id=ids.learner_kind)]),
    dhc.Div([
        dhc.Label('Result'),
        dhc.Div(id=ids.result)])
])


@app.callback(
    Output(ids.result, 'children'),
    [Input(ids.learner_kind, 'value')]
)
def update_output_div(input_val):
    return div_list_from_func(dict(estimators)[input_val])


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
