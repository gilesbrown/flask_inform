import json
from inspect import getargspec
#from operator import methodcaller
from itertools import chain, repeat
from simplegeneric import generic
from .elements import Script, A, Code, Form, Input, HTML, Head, Meta, Body
#from xml.etree.ElementTree import Element
from flask import url_for


class href(unicode):
    pass


@generic
def etree(obj, **kw):
    return Code(text=json.dumps(obj), class_='json', **kw)


@etree.when_type(href)
def etree_when_href(obj, **kw):
    return A(href=obj, **kw)
    

class Descriptor(object):
    
    __order__ = []
    
    def __init__(self, function, name=None):
        Descriptor.__order__.append(self)
        self.function = function
        if name is None:
            self.name = function.__name__
        else:
            self.name = name
        
    @classmethod
    def pop_order(cls, clsdict):
        members = set(clsdict.values())
        names = [d.name for d in cls.__order__ if d in members]
        cls.__order__ = [d for d in cls.__order__ if d not in members]
        return names
    
    def __get__(self, obj, objtype):
        if obj is None:
            return self
        return etree(self.function(obj), id=self.name)


class ValueDescriptor(Descriptor):    
    pass


class LinkDescriptor(Descriptor):    
    def __get__(self, obj, objtype):
        if obj is None:
            return self
        return etree(href(self.function(obj)), id=self.name)
    
    
class ViewFunction(object):
    def __init__(self, fd):
        self.fd = fd
    def __call__(self, *args, **kwargs):
        return "I AM A VIEW"
    

class FormDescriptor(Descriptor):    
    
    def __init__(self, function):
        super(FormDescriptor, self).__init__(function)
        argspec = getargspec(self.function)
        nones = repeat(None, len(argspec.args) - len(argspec.defaults))
        self.inputs = []
        for name, named in zip(argspec.args, chain(nones, argspec.defaults)):
            if named is not None and isinstance(named, Input):
                named.set('name', name)
                self.inputs.append(named)
    
    def __get__(self, obj, objtype):
        if obj is None:
            return self
        action = obj.url_for(self.function)
        logging.warning('ACTION %r FOR %r', action, self)
        return Form(self.function.__get__(obj, objtype), self.inputs, id=self.name, action=action)
    
    def as_view_func(self, objtype):
        def view_func(*args, **kwargs):
            return 'VIEW FUNC NOW! %r %r' % (args, kwargs)
        return view_func
        
    
import logging

def wrapped_init(f):
    def __init__(self, *args, **kwargs):
        self.__args__ = args
        self.__kwargs__ = kwargs
        if f:
            f(self, *args, **kwargs)
    return __init__


class ViewType(type):
    def __new__(meta, name, bases, clsdict):
        clsdict['__init__'] = wrapped_init(clsdict.get('__init__'))
        clsdict['__descriptors__'] = Descriptor.pop_order(clsdict)
        return super(ViewType, meta).__new__(meta, name, bases, clsdict)


import logging

class View(object):
    __metaclass__ = ViewType
    
    def __etree__(self):
        head = Head(Script(src="/informed.js", text=''))
        #if self.status_code:
        #    head.append(Meta(name='http-status-code', 
        #                     content=unicode(self.status_code)))
        logging.warning('desc %r', self.__descriptors__)
        body = Body(*[getattr(self, name) for name in self.__descriptors__])
        res = HTML(head, body)
        return res
    
    def url_for(self, method):
        endpoint = '%s.%s' % (self.__class__.__name__, method.__name__)
        logging.warning("KWARGS: %r", self.__kwargs__)
        return url_for(endpoint, **self.__kwargs__)
        
    
    @staticmethod
    def form(function):
        return FormDescriptor(function)
    
    @staticmethod
    def value(function):
        return ValueDescriptor(function)
    
    @staticmethod
    def link(function):
        return LinkDescriptor(function)
    
    @classmethod
    def get(cls, *args, **kwargs):
        return cls()