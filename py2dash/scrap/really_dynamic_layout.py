from py2dash.app_makers import dispatch_funcs


def foo(a: int = 0, b: int = 0, c=0):
    return (a * b) + c


def bar(x, greeting='hello'):
    return f"{greeting} {x}"


def confuser(a: int = 0, x: float = 3.14):
    return (a ** 2) * x


funcs = [foo, bar, confuser]

if __name__ == '__main__':
    app = dispatch_funcs(funcs)
    app.run_server(debug=True)
