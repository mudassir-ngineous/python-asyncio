import os

import tornado
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.server.server import Server

from bokeh_server.handlers.app2 import Handler

PORT = None


def main(host="localhost", port=5002):
    global PORT
    PORT = port
    fname = os.path.basename(__file__).strip('.py')
    bokeh_app = Application(FunctionHandler(Handler.modify_doc))
    io_loop = tornado.ioloop.IOLoop.current()
    bokeh_server = Server({'/bokeh/{name}'.format(name=fname): bokeh_app}, io_loop=io_loop, address=host, port=PORT)

    bokeh_server.start()
