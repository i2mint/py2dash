"""
The example below started with the code in section "Dynamically Create a Layout for Multi-Page App Validation"
of https://dash.plot.ly/urls (as of June 17, 2019), and was then refactored many times to
exhibit the abstract patterns within, and make it have a more "parametrized form".

"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import flask

from py2dash.component_makers import list_diff, mk_navigation_links_div_list, mk_layout_for_page

app = dash.Dash(
    __name__,
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
)

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


contents_of_page = {
    '/': [],
    '/page-1': [dcc.Input(id='input-1-state', type='text', value='Montreal'),
                dcc.Input(id='input-2-state', type='text', value='Canada'),
                html.Button(id='submit-button', n_clicks=0, children='Submit'),
                dcc.Input(id='input_3', type='text', value='nothing')],
    '/page-2': dcc.Dropdown(
        id='page-2-dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    )
}

template_funcs = [
    lambda path: html.H2(path),
    contents_of_page.get,
    lambda path: html.Div(id=path + '--output'),
    lambda path: html.Br(),
    lambda path: mk_navigation_links_div_list(list_diff(list(contents_of_page.keys()), path))
]

layout_for_page = {
    'url_bar_and_content_div': url_bar_and_content_div,
    '/': html.Div(mk_layout_for_page('/', template_funcs)),
    '/page-1': html.Div(mk_layout_for_page('/page-1', template_funcs)),
    '/page-2': html.Div(mk_layout_for_page('/page-2', template_funcs)),
}


def serve_layout():
    if flask.has_request_context():
        return layout_for_page['url_bar_and_content_div']
    return html.Div(list(layout_for_page.values()))


app.layout = serve_layout

dflt_layout = layout_for_page['/']


# Index callbacks
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    return layout_for_page.get(pathname, dflt_layout)


# Page 1 callbacks
@app.callback(Output('/page-1--output', 'children'),
              [Input('submit-button', 'n_clicks'), Input('input_3', 'value')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value')])
def update_output(n_clicks, input3, input1, input2):
    return ('The Button has been pressed {} times, (input3: {})'
            'Input 1 is "{}",'
            'and Input 2 is "{}"').format(n_clicks, input3, input1, input2)


# Page 2 callbacks
@app.callback(Output('/page-2--output', 'children'),
              [Input('page-2-dropdown', 'value')])
def display_value(value):
    print('display_value')
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
