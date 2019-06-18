import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import flask

from py2dash.component_makers import list_diff, mk_navigation_links_div_list

app = dash.Dash(
    __name__,
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
)

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


def mk_layout_for_page(path, template_funcs):
    div_list = list()
    for func in template_funcs:
        layout_component = func(path)
        if isinstance(layout_component, list):
            div_list.extend(layout_component)
        else:
            div_list.append(layout_component)
    return div_list


pages = ['/', '/page-1', '/page-2']

contents_of_page = {
    '/': [],
    '/page-1': [dcc.Input(id='input-1-state', type='text', value='Montreal'),
               dcc.Input(id='input-2-state', type='text', value='Canada'),
               html.Button(id='submit-button', n_clicks=0, children='Submit')],
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
    lambda path: mk_navigation_links_div_list(list_diff(pages, path))
]

layout_index = html.Div(mk_layout_for_page('/', template_funcs))
layout_page_1 = html.Div(mk_layout_for_page('/page-1', template_funcs))
layout_page_2 = html.Div(mk_layout_for_page('/page-2', template_funcs))


layout_for_page = {
    'url_bar_and_content_div': url_bar_and_content_div,
    '/': layout_index,
    '/page-1': layout_page_1,
    '/page-2': layout_page_2,
}


def serve_layout():
    if flask.has_request_context():
        return layout_for_page['url_bar_and_content_div']
    return html.Div(list(layout_for_page.values()))


app.layout = serve_layout


# Index callbacks
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    return layout_for_page.get(pathname, layout_index)


# Page 1 callbacks
@app.callback(Output('/page-1--output', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value')])
def update_output(n_clicks, input1, input2):
    return ('The Button has been pressed {} times,'
            'Input 1 is "{}",'
            'and Input 2 is "{}"').format(n_clicks, input1, input2)


# Page 2 callbacks
@app.callback(Output('/page-2--output', 'children'),
              [Input('page-2-dropdown', 'value')])
def display_value(value):
    print('display_value')
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
