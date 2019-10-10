import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
from dash.dependencies import Output, Input

from py2dash import component_makers as cm


def dispatch_func_to_app(app, func):
    func_mint = cm.dash_mint_for_func(func)
    app.callback(Output(**func_mint['output_callback_spec']),
                 list(map(lambda x: Input(**x), func_mint['input_callback_specs'])))(func)


def dispatch_funcs_to_app(app, funcs):
    for func in funcs:
        dispatch_func_to_app(app, func)


def dispatch_funcs_old(funcs):
    app = dash.Dash(
        __name__,
        external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
    )

    def page_of_func(func=None):
        if func is not None:
            return f"/{func.__name__}"
        else:
            return '/'

    layout_for_page = dict()
    layout_for_page['/'] = html.Div(children=[], id='/-div')

    for func in funcs:
        func_mint = cm.dash_mint_for_func(func)
        page = page_of_func(func)
        layout_for_page.update(
            {page: html.Div(func_mint['input_divs'] + [func_mint['output_div']],
                            id=func_mint['func_id'])})

    pages = list(layout_for_page.keys())
    for page, v in layout_for_page.items():
        v.children.extend(cm.mk_navigation_links_div_list(cm.list_diff(pages, page),
                                                          link_str_for=lambda x: f"{x}-div"))

    url_bar_and_content_div = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])
    layout_for_page['url_bar_and_content_div'] = url_bar_and_content_div

    def serve_layout():
        if flask.has_request_context():
            return layout_for_page['url_bar_and_content_div']
        return html.Div(list(layout_for_page.values()))

    app.layout = serve_layout

    dflt_layout = layout_for_page['/']

    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        return layout_for_page.get(pathname, dflt_layout)

    dispatch_funcs_to_app(app, funcs)

    return app


def capitalize_first_letter(s):
    return s[0].upper() + s[1:].lower()


# TODO: external_stylesheets doesn't work when doing this:
# configs = {
#     'dash.Dash': {
#         'name': "My Own Lil' name",
#     },
#     'add_app_attrs': {
#         'title': 'Lil'
#     }
# }
# convention = {}
# app = dispatch_funcs(funcs, configs, convention)
# app.run_server(debug=True)
dflt_convention = {
    'dispatch_funcs': {
        'dash.Dash': dict(external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
    }
}

try:
    from py2mint.chain_map import ChainMapTree
except ImportError:
    from warnings import warn

    warn("You should really install https://github.com/i2mint/py2mint. Things won't work correctly if not")
    from collections import ChainMap as ChainMapTree  # replacement, but not actually recursive


#
# class Configs:
#     def __init__(self, namespace, configs=None, convention=None):
#         convention = (convention or dflt_convention).get(namespace, {})
#         self._chain_map = ChainMapTree((configs or {}), convention)


def mk_configs(namespace, configs=None, convention=None):
    convention = (convention or dflt_convention).get(namespace, {})
    return ChainMapTree((configs or {}), convention).to_dict()


def add_app_attrs(app, **kwargs):
    for k, v in kwargs.items():
        setattr(app, k, v)


def dispatch_funcs(funcs, configs=None, convention=None):
    from pprint import pprint
    # make the configuration for this function call by merging configs and convention
    configs = mk_configs('dispatch_funcs', configs=configs, convention=convention)

    print(configs)

    # make the app  (TODO: objectify or functionalize this kind of operation)
    app = dash.Dash(**dict({'name': __name__}, **configs.get('dash.Dash', {})))
    add_app_attrs(app, **configs.get('add_app_attrs', {}))

    print(dict({'name': __name__}, **configs.get('dash.Dash', {})))
    pprint(app.__dict__)

    def url_for_func(func=None):
        if func is not None:
            return f"/{func.__name__}"
        else:
            return '/'

    func_mint_for_url = dict()
    div_for_url = dict()

    div_for_url['/'] = html.Div(children=[], id='/-div')
    func_mint_for_url['/'] = {'func_title_name': 'Home'}

    for func in funcs:
        func_mint = cm.dash_mint_for_func(func)
        url = url_for_func(func)
        div_for_url[url] = html.Div(func_mint['input_divs'] + [func_mint['output_div']],
                                    id=func_mint['func_id'])
        func_mint_for_url[url] = func_mint

    urls = list(div_for_url.keys())
    for url, v in div_for_url.items():
        v.children.extend(cm.mk_navigation_links_div_list(
            cm.list_diff(urls, url), link_str_for=lambda x: func_mint_for_url.get(x, {}).get('func_title_name')))

    url_bar_and_content_div = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])
    div_for_url['url_bar_and_content_div'] = url_bar_and_content_div

    def serve_layout():
        if flask.has_request_context():
            return div_for_url['url_bar_and_content_div']
        return html.Div(list(div_for_url.values()))

    app.layout = serve_layout

    dflt_div = div_for_url['/']

    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        return div_for_url.get(pathname, dflt_div)

    dispatch_funcs_to_app(app, funcs)

    return app
