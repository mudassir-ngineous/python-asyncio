import glob
from importlib import import_module
from os.path import dirname, basename, isfile

modules = glob.glob(dirname(__file__) + '/*.py')

__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]


def load():
    port = 5006
    apps = dict()
    for i, m in enumerate(__all__):
        p = port + i
        import_module('dashboard.bokeh_server.bokeh_apps.{m}'.format(m=m)).main(port=p)
        apps[m] = p

    return apps
