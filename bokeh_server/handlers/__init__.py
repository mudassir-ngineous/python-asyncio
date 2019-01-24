import glob
import os
from abc import ABC, abstractmethod
from importlib import import_module
from os.path import dirname, basename, isfile

import tornado.web
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import server_document
from jinja2 import Environment, FileSystemLoader

from bokeh_server.bokeh_apps import load as load_apps

env = Environment(loader=FileSystemLoader('../templates'))

modules = glob.glob(dirname(__file__) + '/*.py')

__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]


class DashboardHandler(ABC, tornado.web.RequestHandler):
    base_url = 'http://localhost:{port}/bokeh'
    apps = dict()

    @abstractmethod
    async def get(self):
        DashboardHandler.data = await self.get_data()

        template = env.get_template('embed.html')
        fname = os.path.basename(self.handler_name).strip('.py')
        url = '{base_url}/{fname}'.format(
            base_url=DashboardHandler.base_url.format(port=DashboardHandler.apps[fname]),
            fname=fname)
        script = server_document(url=url)

        self.write(template.render(script=script, template="Tornado"))

    @staticmethod
    @abstractmethod
    def modify_doc(doc):
        """

        Entry point for designing of document, addition of widgets, plots etc
        :param doc: bokeh.Document
                must be implemented in child class
        :return:
        """
        pass

    @classmethod
    def get_bokeh_app(cls):
        if cls._bokeh_app is None:
            cls._bokeh_app = Application(FunctionHandler(cls.modify_doc))
        return cls._bokeh_app

    @abstractmethod
    async def get_data(self):
        """
        collects data sources for the app to run, must be implemented by child class
        :return:
        """
        pass


routes = [
    (r"/{m}".format(m=module_name), import_module('dashboard.bokeh_server.handlers.{m}'.format(m=module_name)).Handler)
    for
    module_name in __all__
]

DashboardHandler.apps = load_apps()
