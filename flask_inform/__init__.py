import logging
import re
import inspect
import posixpath
from functools import wraps
from pkg_resources import resource_filename
from flask import render_template, send_from_directory
from flask_inform.filters import inform_filters, Item, Link
from flask_inform.descriptors import FormDescriptor
from flask_inform.document import Document
from flask_inform.viewfunc import ViewFunc
from flask_inform.elements import Input, Select
from xml.etree.ElementTree import ElementTree


UNDEFINED = object()
NULL = unicode('null')

# in-place prettyprint formatter

def indent(elem, level=0, tab='\t'):
    i = "\n" + level*tab
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + tab
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i



def view_func(f):
    
    from xml.etree.ElementTree import tostring
    print "RENDERED:", f
    @wraps(f)
    def render(*args, **kwargs):
        res = f(*args, **kwargs)
        etree = getattr(res, '__etree__', None)
        if etree is None:
            return 'NONE'
        etree = etree()
        indent(etree)
        et = ElementTree(etree)
        from StringIO import StringIO
        sio = StringIO()
        sio.write('<!DOCTYPE html>\n')
        #write(file, encoding="us-ascii", xml_declaration=None, method="xml") 
        et.write(sio, 'utf-8', method='html')
        return sio.getvalue()
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
        instance = method.im_class(id)
        return method(instance, *args[1:])
    return instantiate

import logging

class Inform(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.add_url_rule('/informed.js', 'informed.js', informed_js)
        #app.jinja_loader.searchpath.insert(0, resource_filename(__name__, 'templates'))
        #app.jinja_env.filters.update(inform_filters)

    def add_url_rules(self, document_class, rule):
        endpoint = document_class.__name__
        self.app.add_url_rule(rule, endpoint, ViewFunc(document_class))
        print "add_url_rules!"
        #format_endpoint = '{view.__name__}.{method}'.format
        #endpoint = format_endpoint(view=view, method='get')
        #logging.warning("add_url_rules: %r %r %r", rule, endpoint, view.get)
        #self.app.add_url_rule(rule, endpoint, view_func(view.get))
        #for name in view.__descriptors__:
        #    desc = getattr(view, name)
        #    #logging.warning("OH %r", desc)
        #    if isinstance(desc, FormDescriptor):
        #        subrule = posixpath.join(rule, name)
        #        endpoint = format_endpoint(view=view, method=name)
        #        logging.warning("add FORM: %r %r %r", subrule, endpoint, desc)
        #        self.app.add_url_rule(subrule, endpoint, getattr(view, name).as_view_func(view))
                
        #for name in view.__descriptors__:
        #    descriptor = getattr(view, name)
        #    if isinstance(descriptor, Form):
        #        endpoint = view.__name__ + '.' + name
        #        print endpoint
        #        self.app.add_url_rule(base, endpoint, rendered(getattr(view, name)))

        #if hasattr(view, 'index'):
        #    self.app.add_url_rule(base, '{0.__name__}.index'.format(view), rendered(view.index))
        #
        #if hasattr(view, 'get'):
        #    self.app.add_url_rule(base + '<int:id>', '{0.__name__}.get'.format(view), rendered(instantiated(view.get)))

def form():
    def decorator(f):
        return FormDescriptor(f)
    return decorator