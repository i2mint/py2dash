import os


def foo(a: int = 0, b: int = 0, c=0):
    """This is foo. It computes something"""
    return (a * b) + c


def bar(x, greeting='hello'):
    """bar greets its input"""
    return f"{greeting} {x}"


def confuser(a: int = 0, x: float = 3.14):
    return (a ** 2) * x


funcs = [foo, bar, confuser]

if __name__ == '__main__':
    from py2dash.app_makers import dispatch_funcs
    print('file: {}'.format(os.path.realpath(__file__)))
    app = dispatch_funcs(funcs, {'style': {'root_dir': os.path.dirname(os.path.realpath(__file__))}})
    app.run_server(debug=True)

    # from py2dash.app_makers import dispatch_funcs
    #
    # configs = {}
    # which_one = 'some_configs'
    #
    # if which_one == 'simple':
    #     app = dispatch_funcs(funcs)
    #     app.run_server(debug=True)
    # elif which_one == 'some_configs':
    #     # But if you wanted to configure, or change the underlying convention, you could!
    #
    #     configs = {
    #         'dash.Dash': {
    #             'name': "My Own Lil' name",
    #         },
    #         'add_app_attrs': {
    #             'title': 'Lil'
    #         }
    #     }
    #     convention = {}
    #     app = dispatch_funcs(funcs, configs, convention)
    #     app.run_server(debug=True)
