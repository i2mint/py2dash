from sklearn.utils.testing import all_estimators
from functools import wraps


def stringify_output(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        return str(func(*args, **kwargs))
    return wrapped


funcs = [stringify_output(x[1]) for x in all_estimators()][:70]

if __name__ == '__main__':
    from py2dash.app_makers import dispatch_funcs
    print("**********************************************************")
    print(f"Dispatching {len(funcs)} functions. (Note that it takes about 1-3s per 10 functions to dispatch, "
          "so might have to wait sometimes.")
    print("**********************************************************")
    app = dispatch_funcs(funcs)
    app.run_server(debug=True)
