# from jupyter_plotly_dash import JupyterDash

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# app = dash.Dash('SimpleExample')
#
# app.layout = html.Div([
#     dcc.RadioItems(
#         id='dropdown-color',
#         options=[{'label': c, 'value': c.lower()}
#                  for c in ['Red', 'Green', 'Blue']],
#         value='red'
#     ),
#     html.Div(id='output-color'),
#     dcc.RadioItems(
#         id='dropdown-size',
#         options=[{'label': i, 'value': j}
#                  for i, j in [('L', 'large'), ('M', 'medium'), ('S', 'small')]],
#         value='medium'
#     ),
#     html.Div(id='output-size')
#
# ])
#
#
# @app.callback(
#     dash.dependencies.Output('output-color', 'children'),
#     [dash.dependencies.Input('dropdown-color', 'value')])
# def callback_color(dropdown_value):
#     return "The selected color is %s." % dropdown_value
#
#
# @app.callback(
#     dash.dependencies.Output('output-size', 'children'),
#     [dash.dependencies.Input('dropdown-color', 'value'),
#      dash.dependencies.Input('dropdown-size', 'value')])
# def callback_size(dropdown_color, dropdown_size):
#     return "The chosen T-shirt is a %s %s one." % (dropdown_size,
#                                                    dropdown_color)
#
#


print(dcc.__version__)  # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])

page_1_layout = html.Div([
    html.H1('Page 1'),
    dcc.Dropdown(
        id='page-1-dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),

])


@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)


page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.RadioItems(
        id='page-2-radios',
        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value='Orange'
    ),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

trans_for = {
    'options': lambda v: [{'label': i, 'value': i} for i in v]
}

component_spec_for = {
    'radio': {'func': dcc.RadioItems, }
}


def div_children_for(key, **specs):
    val = component_spec_for.get(key, None)
    if val is None:
        return []
    else:
        for special_key in trans_for:
            if special_key in specs:
                specs[special_key] = trans_for[special_key](specs[special_key])

        # print(val['func'])
        # print(specs)
        t = [val['func'](**specs)]
        t.extend([html.Div(id=key), html.Br()])
        return t


def mk_page_layout(pathname, **kwargs):
    children = []

    children.append(html.H1(f'Page for {pathname}'))

    for key, specs in kwargs.items():
        children.extend(div_children_for(key, **specs))

    return html.Div(children)

    # if 'radio' in kwargs:
    #     key = 'radio'
    #     specs = kwargs.get(key, {})
    #     children.extend(div_children_for(key, **specs))
    #     children.extend([html.Div])
    #     if val is not None:
    #         children.extend(div_children_for(key))
    #         children.append(dcc.RadioItems(
    #             id=key,
    #             options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
    #             value='Orange'
    #         ))
    # return html.Div([
    #     html.H1(f'Page for {pathname}'),
    #
    #     dcc.RadioItems(
    #         id='page-2-radios',
    #         options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
    #         value='Orange'
    #     ),
    #     html.Div(id='page-2-content'),
    #     html.Br(),
    #     dcc.Link('Go to Page 1', href='/page-1'),
    #     html.Br(),
    #     dcc.Link('Go back to home', href='/')
    # ])


@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/special':
        specs = {
            'radio': {'options': ['foo', 'bar', 'again'],
                      'id': 'radio',
                      'value': 'foo'}
        }
        return mk_page_layout('blah blah', **specs)
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)
