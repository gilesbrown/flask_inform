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
    
    
class FormDescriptor(Descriptor):    
    
    def __init__(self, function):
        super(FormDescriptor, self).__init__(function)
        argspec = getargspec(self.function)
        nones = repeat(None, len(argspec.args) - len(argspec.defaults))
        self.inputs = []
        for name, named in zip(argspec.args, chain(nones, argspec.defaults)):
            print "INPUT?", name, named, Input, isinstance(named, Input)
            if named is not None and isinstance(named, Input):
                named.set('name', name)
                self.inputs.append(named)
    
    def __get__(self, obj, objtype):
        if obj is None:
            return self
        #action = obj.url_for(self.function)
        action = '/banana'
        logging.warning('ACTION %r FOR %r %r', action, self, self.inputs)
        return Form(self.function.__get__(obj, objtype), self.inputs, id=self.name, action=action)
    
    def as_view_func(self, objtype):
        def view_func(*args, **kwargs):
            return 'VIEW FUNC NOW! %r %r' % (args, kwargs)
        return view_func