from dataclasses import dataclass

import dash_core_components as dcc
import dash_html_components as hc

from py2dash.util import extract_name_and_default, SignatureExtractor

extract_signature = SignatureExtractor(attrs=('name', 'default', 'annotation'))

undefined = extract_name_and_default(dcc.Input)[0]['default']


def ensure_list(x):
    if isinstance(x, str):
        return [x]
    else:
        return x


def list_diff(a, b=()):
    """

    :param a: An iterable
    :param b: A string or list-like
    :return: list(a) without the elements of b, but in the same order as a
    >>> list_diff(['hello', 'world', 'howdyoudo?'])
    ['hello', 'world', 'howdyoudo?']
    >>> list_diff(['hello', 'world', 'howdyoudo?'], 'world')
    ['hello', 'howdyoudo?']
    """
    return [x for x in a if x not in ensure_list(b)]


def navigate_to_path_text(path):
    return f'Navigate to path {path}'


def mk_navigation_links(paths, link_str_for=navigate_to_path_text, sep_maker=hc.Br):
    element_list = []
    for path in paths:
        element_list.append(hc.Div(dcc.Link(link_str_for(path), href=path), className="nav-link"))
    return element_list


def mk_layout_for_page(path, template_funcs):
    """
    Make an element_list for a layout of a page by applying each template function of template_funcs to
    the given path.
    :param path: input to the functions of template_funcs
    :param template_funcs: The template functions (should all take any valid input path and return an
        html component or list thereof)
    :return: A list (to be given to children of dash_html_components.Div)
    """
    element_list = list()
    for func in template_funcs:
        layout_component = func(path)
        if isinstance(layout_component, list):
            element_list.extend(layout_component)
        else:
            element_list.append(layout_component)
    return element_list


class Ddiv(hc.Div):
    def __add__(self, x):
        if self.children is None:
            self.children = []
        if isinstance(x, Ddiv):
            self.children
        if not isinstance(x, list):
            x = [x]


@dataclass(init=True, repr=True, eq=True, frozen=True)
class SpecialArg:
    name: str


not_specified = SpecialArg('not_specified')
choose_first_element = SpecialArg('choose_first_element')


def input_type_for_py_obj(obj):
    if isinstance(obj, str):
        return 'text'
    elif isinstance(obj, (float, int)):
        return 'number'
    elif isinstance(obj, bool):
        return 'text'
    else:
        return None


input_type_for_annotation = {
    str: 'text',
    float: 'number',
    int: 'number',
    bool: 'text'
}


def input_type_from_arg_spec(sig):
    input_type = input_type_for_annotation.get(sig.get('annotation', None), None)
    if input_type is not None:
        return input_type
    dflt_val = sig.get('default', None)
    return input_type_for_py_obj(dflt_val)


def labeled_div(_id, element_list, label=None):
    if label is None:
        label = _id
    hc.Div([hc.Label(label), element_list])

    # dropdown_from_list(Controller.list_learner_kinds(), id=ids.learner_kind)])


def component_for_arg_spec(arg_spec, id_prefix=''):
    children = []
    _id = id_prefix + '-' + arg_spec['name']
    children.append(hc.Label(arg_spec['name']))
    if arg_spec.get('default', None) is not None:
        value = arg_spec['default']
        # if isinstance(value, bool):  # TODO: Finish better handling of booleans
        #     element_list.append(dcc.Checklist(id=_id))
        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
            value = str(value)
    else:
        value = ''

    children.append(dcc.Input(id=_id, value=value, type=input_type_from_arg_spec(arg_spec)))
    return hc.Div(children, className="arg-container")


def element_list_from_func(func):
    """ TODO: Deprecate """
    arg_name_and_dflt = extract_name_and_default(func)
    elements = list()
    elements.append(hc.H3(func.__name__))
    for d in arg_name_and_dflt:
        elements.append(component_for_arg_spec(d, id_prefix=f"{func.__name__}"))
    return elements


def dash_mint_for_arg(arg_spec, id_prefix=''):
    children = []
    _id = id_prefix + '-' + arg_spec['name']
    children.append(hc.Label(arg_spec['name']))
    if arg_spec.get('default', None) is not None:
        value = arg_spec['default']
        # if isinstance(value, bool):  # TODO: Finish better handling of booleans
        #     element_list.append(dcc.Checklist(id=_id))
        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
            value = str(value)
        children.append(dcc.Input(id=_id, value=value, type=input_type_from_arg_spec(arg_spec)))
    else:
        value = ''
        children.append(dcc.Input(id=_id, type=input_type_from_arg_spec(arg_spec)))

    # divs.append(dcc.Input(id=_id, value=value, type=input_type_from_arg_spec(arg_spec)))

    mint = dict()
    mint['layout_element'] = hc.Div(children, className="function-input")
    mint['input_callback_specs'] = {'component_id': _id, 'component_property': 'value'}
    return mint


def dash_mint_for_func(func):
    arg_specs = extract_signature(func)
    children = list()
    input_callback_specs = list()
    func_name = func.__name__
    children.append(hc.H3(func_name))
    for arg_spec in arg_specs:
        arg_mint = dash_mint_for_arg(arg_spec, id_prefix=f"{func_name}")
        children.append(arg_mint['layout_element'])
        input_callback_specs.append(arg_mint['input_callback_specs'])
    func_id = f"{func_name}-container"
    output_id = f"{func_name}-output"
    func_title_name = func_name[0].upper() + func_name[1:].lower()
    output_element = hc.Div(id=output_id, className="function-output")
    output_callback_spec = {'component_id': output_id, 'component_property': 'children'}
    return dict(func_id=func_id,
                func_title_name=func_title_name,
                input_elements=children,
                input_callback_specs=input_callback_specs,
                output_callback_spec=output_callback_spec,
                output_element=output_element)


def options_dict_from_list(options):
    return [{'label': x, 'value': x} for x in options]


def dropdown_from_list(options_list, value=choose_first_element, **kwargs):
    kws = dict(kwargs, options=options_dict_from_list(options_list))
    if value == choose_first_element:
        value = options_list[0]
    if value != not_specified:
        kws['value'] = value

    return dcc.Dropdown(**kws)


class FuncMint:
    pass
