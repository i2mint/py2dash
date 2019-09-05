from sklearn.utils.testing import all_estimators
from functools import wraps


def stringify_output(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        return str(func(*args, **kwargs))

    return wrapped


def pickle_output(func):
    import os
    import pickle
    func_name = func.__name__
    save_filepath = os.path.expanduser(f"~/{func_name}.p")

    @wraps(func)
    def wrapped(*args, **kwargs):
        obj = func(*args, **kwargs)
        pickle.dump(obj, open(save_filepath, 'wb'))
        return f"{str(obj)}\nSaved here: {save_filepath}"

    return wrapped


# choose here:
# oputput_decorator = stringify_output
oputput_decorator = pickle_output

funcs = [oputput_decorator(x[1]) for x in all_estimators()][:10]

if __name__ == '__main__':
    from py2dash.app_makers import dispatch_funcs

    print("**********************************************************")
    print(f"Dispatching {len(funcs)} functions. (Note that it takes about 1-3s per 10 functions to dispatch, "
          "so might have to wait sometimes.")
    print("**********************************************************")
    app = dispatch_funcs(funcs)
    app.run_server(debug=True)
