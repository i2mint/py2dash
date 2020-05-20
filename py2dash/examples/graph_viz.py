if __name__ == '__main__':
    from py2dash.app_makers import dispatch_funcs
    from graphviz import Source


    # TODO: Goal is to get something like: https://graphs.grevian.org/graph
    # TODO: (1) Make the text box for source be bigger and have newlines be possible.
    # TODO: (2) Provide Enum for engine
    # TODO: (3.1) return image binary (instead of d.source) and have dispatch recognize this and handle properly
    # TODO: (3.2) Use annotations (graphviz type) and dispatch-side mapping between types and handling
    # TODO: (4) (For Thor): Tools to make such function wrappers (partial-like, adding annotations, mapping) easier.
    def mk_graph(source: str = "", engine='dot'):
        d = Source(source, engine=engine)
        return d.source


    app = dispatch_funcs([mk_graph])
    app.run_server(debug=True)
