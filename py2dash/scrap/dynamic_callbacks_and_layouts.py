import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
# from dash.dependencies import Event
from flask_caching import Cache

import zlib
import sys, os, traceback
import logging


class baseApp(object):
    def __init__(self, app, server, name='App', title='Application', ctx='', loglevel=logging.ERROR, use_cache=False,
                 app_path='./data'):
        self.app = app
        self.server = server
        self.name = name
        self.title = title
        self.ctx = ctx
        self.logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)
        logging.basicConfig(filename=ctx + '.' + __name__ + '.' + self.__class__.__name__ + '.log', filemode='w',
                            level=loglevel, format='%(asctime)s %(levelname)s:%(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S ')
        self.logger.debug('init app, ctx:{ctx}'.format(ctx=self.ctx))
        self.store = {}
        if use_cache is True:
            self.init_cache()

        self.datastore = app_path + 'data/'
        if self.datastore is not None and len(self.datastore) > 1:
            os.makedirs(self.datastore, exist_ok=True)

    def init_cache(self):
        self.cache = Cache(self.app.server, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': './cache/' + self.name})
        return self

    def header(self):
        return html.Div([
            html.H1(self.title, className='display-4')
        ], className='jumbotron')

    def footer(self):
        return html.Footer([
            html.Div([
                html.Span(['ps tools (c)'], className='text-muted')
            ], className='container')], className='footer')

    def getComponentId(self, name):
        return '{name}_{ctx}'.format(name=name, ctx=self.ctx)

    def register_callbacks(self, callbacks):
        print('registering {} callbacks for {}'.format(len(callbacks), self.name))

        for callback_data in callbacks:
            # self.logger.debug('%s] callback_data[0]: %s',self.ctx,callback_data[0])
            # self.logger.debug('%s] callback_data[1]: %s',self.ctx,callback_data[1])
            # self.logger.debug('%s] callback_data[2]: %s',self.ctx,callback_data[2])
            # self.logger.debug('%s] callback_data[3]: %s',self.ctx,callback_data[3])
            # self.logger.debug('%s] callback_data[4]: %s',self.ctx,callback_data[4])

            dynamically_generated_function = self.create_callback(callback_data[0])
            callback_kwargs = dict(output=callback_data[0], inputs=callback_data[1], state=callback_data[2])
            self.app.callback(**callback_kwargs)(dynamically_generated_function)

    def print_exception(self, e, ctx, name, *params):
        print('[{ctx}] Exception in {name} : {msg}'.format(ctx=ctx, name=name, msg=e))
        print('[{ctx}] Exception parameters:'.format(ctx=ctx), *params)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        traceback.print_tb(exc_tb)

    def create_callback(self, output_element, retfunc):
        """creates a callback function"""

        def callback(*input_values):
            print('callback fired with :"{}"  output:{}/{}'.format(input_values, output_element.component_id,
                                                                   output_element.component_property))
            retval = []
            if input_values is not None and input_values != 'None':
                try:
                    retval = retfunc(*input_values)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = traceback.extract_tb(exc_tb, 1)[0][2]
                    filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print('Callback Exception:', e, exc_type, filename, exc_tb.tb_lineno, fname)
                    print('parameters:', *input_values)
                    traceback.print_tb(exc_tb)

            return retval

        return callback

    def define_callback(self, output, input, func=None, state=None): #, event=None, ):
        """defines the callback set"""
        return (
            Output(self.getComponentId(output[0]), output[1]),
            [Input(self.getComponentId(id), attr) for (id, attr) in input],
            [] if state is None else [State(self.getComponentId(id), attr) for (id, attr) in state],
            # [] if event is None else [Event(self.getComponentId(id), attr) for (id, attr) in event],
            self.dummy_callback if func is None else func
        )

    def dummy_callback(self, *input_data):
        print('dummy callback with:', *input_data)
        return []
