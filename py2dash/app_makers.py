import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import inspect
import os
import shutil
from dash.dependencies import Output, Input, State

from py2dash import component_makers as cm


def dispatch_func_to_app(app, func, execute_on_change=False):
    func_mint = cm.dash_mint_for_func(func)
    output = Output(**func_mint['output_callback_spec'])

    if execute_on_change:
        arg_list = list(map(lambda x: Input(**x), func_mint['input_callback_specs']))
        app.callback(output, arg_list)(func)
    else:
        arg_list = list(map(lambda x: State(**x), func_mint['input_callback_specs']))
        def curried_func(n_clicks, *args, **kwargs):
            return func(*args, **kwargs)
        app.callback(output,
                     [Input('submit-button', 'n_clicks')],
                     arg_list)(curried_func)


def dispatch_funcs_to_app(app, funcs):
    for func in funcs:
        dispatch_func_to_app(app, func)


# def dispatch_funcs_old(funcs):
#     app = dash.Dash(__name__)

#     def page_of_func(func=None):
#         if func is not None:
#             return f"/{func.__name__}"
#         else:
#             return '/'

#     layout_for_page = dict()
#     layout_for_page['/'] = html.Div(children=[], id='root')

#     for func in funcs:
#         func_mint = cm.dash_mint_for_func(func)
#         page = page_of_func(func)
#         layout_for_page.update(
#             {page: html.Div(func_mint['input_elements'] + [func_mint['output_element']],
#                             id=func_mint['func_id'])})

#     pages = list(layout_for_page.keys())
#     for page, v in layout_for_page.items():
#         v.children.extend(cm.mk_navigation_links(cm.list_diff(pages, page),
#                                                           link_str_for=lambda x: f"{x}-link"))

#     url_bar_and_content_div = html.Div([
#         dcc.Location(id='url', refresh=False),
#         html.Div(id='page-content')
#     ])
#     layout_for_page['url_bar_and_content_div'] = url_bar_and_content_div

#     def serve_layout():
#         if flask.has_request_context():
#             return layout_for_page['url_bar_and_content_div']
#         return html.Div(list(layout_for_page.values()))

#     app.layout = serve_layout

#     dflt_layout = layout_for_page['/']

#     @app.callback(Output('page-content', 'children'),
#                   [Input('url', 'pathname')])
#     def display_page(pathname):
#         return layout_for_page.get(pathname, dflt_layout)

#     dispatch_funcs_to_app(app, funcs)

#     return app


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
        'dash.Dash': dict()
    }
}

try:
    from i2.chain_map import ChainMapTree
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


def mk_submit_button():
    return html.Button(id='submit-button', n_clicks=0, children='Execute', className="submit-button")


def inject_stylesheets(target_dir, plugins=None):
    os.makedirs(target_dir, exist_ok=True)
    source_dir = os.path.join(os.path.dirname(__file__), 'css')
    print(f'found source css dir: {source_dir}')
    src_files = os.listdir(source_dir)
    for filename in src_files:
        full_path = os.path.join(source_dir, filename)
        if os.path.isfile(full_path):
            print(f'found file to copy: {full_path}')
            shutil.copy(full_path, os.path.join(target_dir, filename))


def dispatch_funcs(funcs, configs=None, convention=None):
    from pprint import pprint
    caller_frame = inspect.stack()[1]
    caller_module = inspect.getmodule(caller_frame[0])
    name = caller_module.__name__
    # make the configuration for this function call by merging configs and convention
    configs = mk_configs('dispatch_funcs', configs=configs, convention=convention)

    print(configs)

    # make the app  (TODO: objectify or functionalize this kind of operation)
    app_kwargs = dict(**configs.get('dash.Dash', {'name': name}))

    print(app_kwargs)

    app = dash.Dash(**app_kwargs)
    add_app_attrs(app, **configs.get('add_app_attrs', {}))

    list_class = 'function-list'
    style_definitions = configs.get('style', None)
    if style_definitions:
        project_root_dir = style_definitions.get('root_dir', None)
        if project_root_dir:
            print(f'found project root dir: {project_root_dir}')
            assets_dir = os.path.join(project_root_dir, 'assets')
            inject_stylesheets(assets_dir, configs.get('style.plugins', None))
        list_type = style_definitions.get('list_type', None)
        if list_type:
            list_class += ' ' + list_type
    # add default stylesheet to project

    # pprint(app.__dict__)

    def url_for_func(func=None):
        if func is not None:
            return f"/{func.__name__}"
        else:
            return '/'

    func_mint_for_url = dict()
    element_for_url = dict()

    element_for_url['/'] = html.Nav(children=[], id='home', className=list_class)
    func_mint_for_url['/'] = {'func_title_name': 'Home'}

    for func in funcs:
        func_mint = cm.dash_mint_for_func(func)
        url = url_for_func(func)
        func_children = func_mint['input_elements'] + [func_mint['output_element']]
        if not configs.get('execute_on_change', False):
            # print('appending submit button')
            func_children.append(mk_submit_button())
        element_for_url[url] = html.Div(func_children, id=func_mint['func_id'], className='function-container')
        func_mint_for_url[url] = func_mint

    urls = list(element_for_url.keys())
    for url, v in element_for_url.items():
        v.children.extend(cm.mk_navigation_links(
            cm.list_diff(urls, url), link_str_for=lambda x: func_mint_for_url.get(x, {}).get('func_title_name')))

    url_bar_and_content_container = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', className='root')
    ])
    element_for_url['url_bar_and_content_container'] = url_bar_and_content_container

    def serve_layout():
        if flask.has_request_context():
            return element_for_url['url_bar_and_content_container']
        element_list = list(element_for_url.values())
        return html.Div(element_list)

    app.layout = serve_layout

    home_element = element_for_url['/']

    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        return element_for_url.get(pathname, home_element)

    dispatch_funcs_to_app(app, funcs)

    return app
