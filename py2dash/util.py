import inspect
import os
import pickle
import argh

home_dir = os.path.expanduser('~')

dispatch_to_cli = argh.dispatch_command


class Ids:
    def __init__(self, _attrs=()):
        self._attrs = list(_attrs)

    def __getattr__(self, _id):
        if isinstance(_id, self.__class__):
            _id = _id._id
        assert isinstance(_id, str), "_id should be a string"
        if _id not in self._attrs:
            setattr(self, _id, _id)
            self._attrs.append(_id)

        return _id

    def __dir__(self):  # to see attr in autocompletion
        return self._attrs

    def __iter__(self):
        yield from self._attrs


class SignatureExtractor:
    def __init__(self, attrs=('name', 'default')):
        def param_mint(param):
            d = dict()
            for k in attrs:
                v = getattr(param, k)
                if v is not inspect._empty:
                    d[k] = v
            return d

        self.param_mint = param_mint

    def __call__(self, obj):
        return [self.param_mint(p) for p in inspect.signature(obj).parameters.values()]


extract_name_and_default = SignatureExtractor(attrs=('name', 'default'))


def get_skdash_dir(root_dir=home_dir):
    assert os.path.isdir(root_dir), f"The directory doesn't exist: {root_dir}"
    odir = os.path.join(root_dir, 'odir')
    if not os.path.isdir(odir):
        os.mkdir(odir)
    skdash_dir = os.path.join(odir, 'skdash')
    if not os.path.isdir(odir):
        os.mkdir(skdash_dir)
    return skdash_dir


def might_be_an_estimator(obj):
    return hasattr(obj, '__init__') and hasattr(obj, 'fit') and hasattr(obj, 'predict')


def might_be_a_transformer(obj):
    return hasattr(obj, '__init__') and hasattr(obj, 'fit') and hasattr(obj, 'transformer')


def module_iterator(root_module, recursive=True):
    root_module_name = root_module.__name__
    # yield root_module_name, root_module
    for k, v in root_module.__dict__.items():
        if not k.startswith('_'):
            if inspect.ismodule(v):
                if hasattr(v, '__name__') and v.__name__.startswith(root_module_name):
                    yield k, v
                    if recursive:
                        yield from module_iterator(v, recursive=True)


def module_all_iterator(module):
    module_name = module.__name__
    yield module_name, module
    for sub_module_name in getattr(module, '__all__', []):
        if not sub_module_name.startswith('_'):
            sub_module = getattr(module, sub_module_name)
            if inspect.ismodule(sub_module):
                yield from module_all_iterator(sub_module)


filt_for_kind = {
    'estimator': might_be_an_estimator,
    'transformer': might_be_a_transformer,
}


def find_sklearn_resources(kind='estimator', root_module=None, recursive=True):
    if root_module is None:
        import sklearn as root_module
    filt = filt_for_kind[kind]
    for k, v in module_iterator(root_module, recursive=recursive):
        if hasattr(v, '__all__'):
            for vv in v.__all__:
                obj = getattr(v, vv)
                # print(vv, obj)
                if filt(obj):
                    yield vv, obj
