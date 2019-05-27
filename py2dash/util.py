import inspect
import os
import pickle
import argh

home_dir = os.path.expanduser('~')

dispatch_to_cli = argh.dispatch_command


class SignatureExtractor:
    def __init__(self, attrs=('name', 'default')):
        def param_mint(param):
            return {k: getattr(param, k) for k in attrs}

        self.param_mint = param_mint

    def __call__(self, obj):
        return [self.param_mint(p) for p in inspect.signature(obj).parameters.values()]


extract_name_default = SignatureExtractor(attrs=('name', 'default'))
extract_name_default_annotation = SignatureExtractor(attrs=('name', 'default'))

