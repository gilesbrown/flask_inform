import re
import inspect
from functools import wraps
from pkg_resources import resource_filename
from flask import render_template, send_from_directory
from flask_inform.filters import inform_filters, Item, Link



UNDEFINED = object()
NULL = unicode('null')


def rendered(f):
    @wraps(f)
    def render(*args, **kwargs):
        res = f(*args, **kwargs)
        if hasattr(res, '__render__'):
            return res.__render__()
        status_code = 404
        return render_template('inform.html', items=[], status_code=status_code), status_code
    return render


def informed_js():
    response = send_from_directory(resource_filename(__name__, 'static'), 'informed.js')
    #response.headers.add('Last-Modified', datetime.datetime.now())
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    response.headers.add('Pragma', 'no-cache')
    return response


def instantiated(method):
    @wraps(method)
    def instantiate(id, *args, **kwargs):
        print args, kwargs
        instance = method.im_class(id)
        print "ARGS:", method.__class__, method, dir(method), method.im_class
        return method(instance, *args[1:])
    return instantiate


class Inform(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.add_url_rule('/informed.js', 'informed.js', informed_js)
        app.jinja_loader.searchpath.insert(0, resource_filename(__name__, 'templates'))
        app.jinja_env.filters.update(inform_filters)

    def add_view_routes(self, view, base=None):

        if base is None:
            base = '/' + re.sub('View$', '', view.__name__).lower() +'/'

        if hasattr(view, 'index'):
            self.app.add_url_rule(base, '{0.__name__}.index'.format(view), rendered(view.index))

        if hasattr(view, 'get'):
            self.app.add_url_rule(base + '<int:id>', '{0.__name__}.get'.format(view), rendered(instantiated(view.get)))
