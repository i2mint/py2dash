from otolite.skdash.controller import Controller, estimators
# from sklearn.tree import DecisionTreeRegressor
#
# func = DecisionTreeRegressor

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from otolite.skdash.util import extract_name_and_default, SignatureExtractor
from py2dash.component_makers import div_list_from_func
from py2dash.component_makers import dropdown_from_list

extract_signature = SignatureExtractor(attrs=('name', 'default', 'annotation'))

undefined = extract_name_and_default(dcc.Input)[0]['default']

from otolite.skdash.controller import run_model


div_list_0 = []

# func = LinearRegression
# func = DecisionTreeRegressor
func = run_model

func_div_list = div_list_from_func(func)

if func == run_model:
    func_div_list.extend([
        html.Button(id='submit-button', n_clicks=0, children='Submit'),
        html.Div(id='output-state')])


# app.layout = html.Div(func_div_list, style={'columnCount': 2})


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
        return super().__dir__() + self._attrs

    def __iter__(self):
        yield from self._attrs


ids = Ids()

# app.layout = html.Div([
#     html.Label('Learner Kind'),
#     dropdown_from_list(Controller.list_learner_kinds(), id=ids.dropdown),
#     html.Button(id=ids.submit_learner, n_clicks=0, children='Submit Learner'),
#     html.Label('Result'),
#     html.Div(id=ids.result)
# ])
#
# @app.callback(
#     Output(ids.result, 'children'),
#     [Input(ids.submit_learner, 'n_clicks')],
#     [State(ids.dropdown, 'value')],
# )
# def update_output_div(n_clicks, input_val):
#     return str(extract_signature(dict(estimators)[input_val]))


div_list_0.extend([
    html.Label('Learner Kind'),
    dropdown_from_list(Controller.list_learner_kinds(), id=ids.dropdown),
    html.Label('Result'),
    html.Div(id=ids.result)
])

# showing different input types
html_input_types = ['text', 'number', 'password', 'email', 'range', 'search', 'tel', 'url', 'hidden']
for input_type in html_input_types:
    div_list_0.append(html.Label(input_type))
    div_list_0.append(dcc.Input(id=input_type + '_example', name=input_type, type=input_type))


app.layout = html.Div(div_list_0)

@app.callback(
    Output(ids.result, 'children'),
    [Input(ids.dropdown, 'value')]
)
def update_output_div(input_val):
    return str(extract_signature(dict(estimators)[input_val]))

# app.layout = html.Div([html.Label('Dropdown'),
#     dcc.Dropdown(
#         options=[
#             {'label': 'New York City', 'value': 'NYC'},
#             {'label': u'Montréal', 'value': 'MTL'},
#             {'label': 'San Francisco', 'value': 'SF'}
#         ],
#         value='MTL')])

# print([State(x['name'], 'value') for x in extract_signature(func)])

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
