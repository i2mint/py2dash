from dataclasses import dataclass

import dash_core_components as dcc
import dash_html_components as hc
from dash.dependencies import Input, Output, State

from otolite.skdash.util import extract_name_and_default, SignatureExtractor

extract_signature = SignatureExtractor(attrs=('name', 'default', 'annotation'))

undefined = extract_name_and_default(dcc.Input)[0]['default']


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
    'str': 'text',
    'float': 'number',
    'int': 'number',
    'bool': 'text'
}


def input_type_from_signature(sig):
    if 'annotation' in sig and isinstance(sig['annotation'], str):
        return input_type_for_annotation.get(sig['annotation'], '')
    else:
        dflt_val = sig.get('default', None)
        return input_type_for_py_obj(dflt_val)


def labeled_div(_id, div_list, label=None):
    if label is None:
        label = _id
    hc.Div([hc.Label(label), div_list])

    # dropdown_from_list(Controller.list_learner_kinds(), id=ids.learner_kind)])


def div_list_from_func(func):
    arg_name_and_dflt = extract_name_and_default(func)

    div_list = list()
    div_list.append(hc.H3(func.__name__))
    for d in arg_name_and_dflt:
        div_list.append(hc.Label(d['name']))
        if d.get('default', None) is not None:
            value = d['default']
            if isinstance(value, bool) or not isinstance(value, (int, float, str)):
                value = str(value)
        else:
            value = ''

        div_list.append(dcc.Input(id=d['name'], value=value, type=input_type_from_signature(d)))
    return div_list


def options_dict_from_list(options):
    return [{'label': x, 'value': x} for x in options]


def dropdown_from_list(options_list, value=choose_first_element, **kwargs):
    kws = dict(kwargs, options=options_dict_from_list(options_list))
    if value == choose_first_element:
        value = options_list[0]
    if value != not_specified:
        kws['value'] = value

    return dcc.Dropdown(**kws)
