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


class ViewType(type):

    _item_order = []

    def __new__(metacls, name, bases, dict_):

        # To determine ordering we need to look-up the items by object
        items = set()
        for objname, obj in dict_.items():

            if objname.startswith('_'):
                continue

            if getattr(obj, '__name__', UNDEFINED) is UNDEFINED:
                obj.__name__ = objname

            if inspect.isfunction(obj):
                print "NAME?", obj
                spec = inspect.getargspec(obj)
                #if spec.args[:1] == ['cls']:
                #    print "CLASSY:", obj
                #    dict_[objname] = classmethod(obj)
                #else:
                #    dict_[objname] = rendered(obj)

            items.add(obj)

        __view_items__ = []
        for obj in metacls._item_order:
            if obj in items:
                __view_items__.append(obj.__name__)

        # This will only ever be non-empty if you write a nested class
        metacls._item_order = [obj for obj in metacls._item_order if obj not in items]

        dict_['__view_items__'] = __view_items__

        cls = super(ViewType, metacls).__new__(metacls, name, bases, dict_)
        return cls


class View(object):

    __metaclass__ = ViewType

    def __render__(self):
        print "RENDER ME", self.__view_items__, getattr(self, self.__view_items__[0])
        items = [Item(getattr(self, item), item) for item in self.__view_items__]
        print "ITEMS?", items
        status_code = 200
        return render_template('inform.html', items=items, status_code=status_code), status_code


class Value(object):
    def __init__(self):
        ViewType._item_order.append(self)
    def __get__(self, obj, objtype):
        return obj.__dict__.get(self.__name__, NULL)

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
