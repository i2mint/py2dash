"""
Tools to mint dash constructs.

mint_docs_of_dash_component(func_or_docstr) returns a list of dicts

"""
import dash_core_components as dcc

import re
from warnings import warn

kwarg_section_re = re.compile('Keyword arguments:\n(.+)', re.MULTILINE)

no_match_output = None


def mk_extractor_group_num(pattern,
                           pattern_method='search',
                           match_method='group',
                           no_match_output=None,
                           *args, **kwargs):
    if isinstance(pattern, str):
        pattern = re.compile(pattern)
    pattern_func = getattr(pattern, pattern_method)

    def extractor(s):
        m = pattern_func(s)
        if m:
            return getattr(m, match_method)(*args, **kwargs)
        else:
            return no_match_output

    return extractor


extract_kwarg_section = mk_extractor_group_num(
    re.compile('Keyword arguments:\n(.+)', re.DOTALL), 'search', 'group', None, 1)


def extract_kwarg_lines(docstr):
    tt = extract_kwarg_section(docstr)
    w = re.split('\n', tt)
    lines = []
    line = ''
    for ww in w:
        if ww.startswith('- '):
            if line:
                lines.append(line)
            line = ww
        else:
            line += ww
    return lines


a_value_equal_to = 'a value equal to: '
n_a_value_equal_to = len(a_value_equal_to)


def rm_extra_quotes(s):
    if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
        return s[1:-1]
    else:
        return s


def detect_and_split_options(type_string):
    if type_string.startswith(a_value_equal_to):
        return list(map(rm_extra_quotes, type_string[n_a_value_equal_to:].split(', ')))
    else:
        return type_string


def parse_type(type_string):
    type_list = type_string.split(' | ')
    if len(type_list) == 1:
        return detect_and_split_options(type_list[0])
    else:
        return list(map(detect_and_split_options, type_list))


split_specs_p = re.compile(';')
p = re.compile('-\ (?P<argname>\w+) \((?P<specs>.+)\): (?P<description>.+)')


def mint_lines(lines, warn_on_error=False):
    plines = list()
    for line in lines:
        try:
            d = p.match(line).groupdict()
            splits = split_specs_p.split(d.pop('specs', ''))
            if len(splits) > 0:
                d['type'] = parse_type(splits[0].strip())
                # if len(splits) > 1:
                #     d['option'] = splits[1].strip()
            plines.append(d)
        except Exception as e:
            if warn_on_error:
                warn(f"Error with line:\n{line}\n:Error was: {e}")
    return plines


def mint_docs_of_dash_component(func_or_docstr, warn_on_error=False):
    """
    Get a list of {} dicts for every argument found in the input function docs.
    Is only specific to (most of) the documentation format used by dash core components.

    :param func_or_docstr: function of doc string of function
    :param warn_on_error: Whether to warn when errors encountered in parsing lines
    :return: A list of "mint" dicts
    """
    if callable(func_or_docstr) and hasattr(func_or_docstr, '__doc__'):
        func_or_docstr = func_or_docstr.__doc__
    lines = extract_kwarg_lines(func_or_docstr)
    return mint_lines(lines, warn_on_error)


def mk_mint_docs_df_for_module(module=dcc):
    import pandas as pd
    d = list()
    for attr_name in filter(lambda x: not x.startswith('_'), dir(module)):
        attr = getattr(module, attr_name)
        if callable(attr):
            d.extend([dict(dd, obj_name=attr_name) for dd in mint_docs_of_dash_component(attr, warn_on_error=False)])
    return pd.DataFrame(d)[['obj_name', 'argname', 'type', 'description']]


if __name__ == '__main__':
    print(mk_mint_docs_df_for_module())
