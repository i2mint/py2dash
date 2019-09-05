from otolite.skdash.controller import Controller
# from sklearn.tree import DecisionTreeRegressor
#
# func = DecisionTreeRegressor

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from py2dash.py2dash.converters import ensure_bool

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from py2dash.util import extract_name_and_default, SignatureExtractor

extract_signature = SignatureExtractor(attrs=('name', 'default', 'annotation'))

undefined = extract_name_and_default(dcc.Input)[0]['default']


def input_type_for_py_obj(obj):
    if isinstance(obj, str):
        return 'text'
    elif isinstance(obj, (float, int)):
        return 'number'
    else:
        return None


input_type_for_annotation = {
    'str': 'text',
    'float': 'number',
    'int': 'number'
}


def input_type_from_signature(sig):
    if 'annotation' in sig and isinstance(sig['annotation'], str):
        return input_type_for_annotation.get(sig['annotation'], '')
    else:
        return input_type_for_py_obj(sig['default'])


def div_list_from_func(func):
    arg_name_and_dflt = extract_name_and_default(func)

    div_list = list()
    div_list.append(html.H3(func.__name__))
    for d in arg_name_and_dflt:
        div_list.append(html.Label(d['name']))
        if d['default'] is not None:
            value = d['default']
            if isinstance(value, bool) or not isinstance(value, (int, float, str)):
                value = str(value)
        else:
            value = ''

        div_list.append(dcc.Input(id=d['name'], value=value, type=input_type_from_signature(d)))
    return div_list


from sklearn.linear_model import LinearRegression

func = LinearRegression

div_list = div_list_from_func(func)
div_list.extend([
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-state')])

app.layout = html.Div(div_list, style={'columnCount': 2})

# print([State(x['name'], 'value') for x in extract_signature(func)])


states = [State(x['name'], 'value') for x in extract_signature(func)]


@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              states)
def run_model(n_clicks, mall_name, model_name: str, xy_name: str, method: str = 'predict', return_y: bool = False):
    return_y = ensure_bool(return_y)
    return Controller(mall_name).run_model(model_name, xy_name, method=method, return_y=return_y)


if __name__ == '__main__':
    app.run_server(debug=True)
