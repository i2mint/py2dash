########################################################################################################################
# A module's classes signatures' analysis
import pandas as pd
import numpy as np
import inspect
from typing import Callable, Iterator


def module_classes(module):
    return filter(inspect.isclass, module.__dict__.values())


class SignatureExtractor:
    def __init__(self, attrs=('name', 'default')):
        def param_mint(param):
            return {k: getattr(param, k) for k in attrs}

        self.param_mint = param_mint

    def __call__(self, obj):
        return [self.param_mint(p) for p in inspect.signature(obj).parameters.values()]


extract_name_and_default = SignatureExtractor(attrs=('name', 'default'))


def name_arg_default_dict_of_callables(callables: Iterator[Callable]) -> dict:
    """
    Get an {callable_name: {arg_name: arg_default, ...}, ...} dict from a collection of callables.
    See also: name_arg_default_dict_of_callables and arg_default_dict_of_module_classes
    :param callables: Iterable of callables
    :return: A dict
    """
    d = dict()
    for obj in callables:
        try:
            d[obj.__name__] = {x['name']: x['default'] for x in extract_name_and_default(obj)}
        except Exception as e:
            pass  # TODO: Give choice to warn instead of ignore
    return d

def arg_default_dict_of_module_callables(module, obj_filt=callable) -> dict:
    """
    Get an {callable_name: {arg_name: arg_default, ...}, ...} dict from a collection of callables taken from
    an input module (callables filtered using the given obj_filt.
    :param module: Module to extract callables from
    :param obj_filt: The filter to apply to the module's objects to get the collection of callables
    :return: A dict
    """
    return name_arg_default_dict_of_callables(filter(obj_filt, module.__dict__.values()))


def arg_default_dict_of_module_classes(module) -> dict:
    """
    Get an {callable_name: {arg_name: arg_default, ...}, ...} dict from the collection of all classes of module.
    :param module: Module to extract callables from
    :return: A dict
    """
    return arg_default_dict_of_module_callables(module, obj_filt=inspect.isclass)


def non_null_counts(df: pd.DataFrame, null_val=np.nan):
    if null_val is np.nan:
        non_null_lidx = ~df.isna()
    else:
        non_null_lidx = df != null_val
    row_null_zero_count = non_null_lidx.sum(axis=1)
    col_null_zero_count = non_null_lidx.sum(axis=0)
    return row_null_zero_count, col_null_zero_count


def df_of_callable_arg_default_dict(callable_arg_default_dict, null_fill='') -> pd.DataFrame:
    """
    Get a dataframe from a callable_arg_default_dict
    :param module:
    :param null_fill:
    :return:
    """
    d = pd.DataFrame.from_dict(callable_arg_default_dict)
    row_null_zero_count, col_null_zero_count = non_null_counts(d, null_val=np.nan)
    row_argsort = np.argsort(row_null_zero_count)[::-1]
    col_argsort = np.argsort(col_null_zero_count)[::-1]
    return d.iloc[row_argsort, col_argsort].fillna(null_fill)


def module_classes_signatures_df(module, null_fill='') -> pd.DataFrame:
    """
    :param module:
    :param null_fill:
    :return:
    """
    d = arg_default_dict_of_module_classes(module)
    return df_of_callable_arg_default_dict(d, null_fill=null_fill)


########################################################################################################################
# Exposing sklearn

import inspect
import sklearn


def might_be_an_estimator(obj):
    return hasattr(obj, '__init__') and hasattr(obj, 'fit') and hasattr(obj, 'predict')


def might_be_a_transformer(obj):
    return hasattr(obj, '__init__') and hasattr(obj, 'fit') and hasattr(obj, 'transformer')


def module_iterator(root_module, recursive=True):
    root_module_name = root_module.__name__
    for k, v in root_module.__dict__.items():
        if not k.startswith('_'):
            if inspect.ismodule(v):
                if hasattr(v, '__name__') and v.__name__.startswith(root_module_name):
                    yield k, v
                    if recursive:
                        yield from module_iterator(v, recursive=True)


filt_for_kind = {
    'estimator': might_be_an_estimator,
    'transformer': might_be_a_transformer,
}


def find_sklearn_resources(kind='estimator', root_module=sklearn, recursive=True):
    filt = filt_for_kind[kind]
    for k, v in module_iterator(root_module, recursive=recursive):
        if hasattr(v, '__all__'):
            for vv in v.__all__:
                obj = getattr(v, vv)
                if filt(obj):
                    yield vv, obj
