from json import dumps as json_dumps
from simplegeneric import generic
from datetime import datetime

class href(unicode):
    pass


import inspect
from operator import methodcaller
from itertools import chain, repeat
from xml.etree import ElementTree

REQUIRED = object()


class Element(ElementTree.Element):
    
    def __init__(self, *children, **extra):
        tag = extra.pop('tag', self.__class__.__name__.lower())
        text = extra.pop('text', None)
        # remove trailing '_' so 'class_' -> 'class'
        extra = {k.rstrip('_'): v for k, v in extra.items()}
        super(Element, self).__init__(tag, **extra)
        self.text = text
        self.extend(children)
        
    def __etree__(self):
        return self
    
class HTML(Element):
    pass

class Head(Element):
    pass

class Body(Element):
    pass

class Meta(Element):
    pass

class Code(Element):
    pass

class Script(Element):
    pass

class A(Element):
    pass

class Time(Element):
    pass


class Form(Element):
    def __init__(self, function, inputs, **extra):
        super(Form, self).__init__(*inputs, **extra)
        self.function = function
        self.inputs = inputs
        
    def __call__(self, **kw):
        print "CALL:", kw, self.function
        values = {}
        for input in self.inputs:
            from xml.etree.ElementTree import tostring
            print "INPUT?", '%%', repr(tostring(input)), '%%'
            value = kw.pop(input.name, input.default)
            if value is REQUIRED:
                raise ValueError('whoops')
            values[input.name] = value 
        return self.function(**values)
    

class Input(Element):
    name = property(methodcaller('get', 'name'))
    def __init__(self, *children, **extra):
        self.default = extra.pop('default', None)
        super(Input, self).__init__(*children, **extra)


class Option(Element):
    pass

class Select(Input):
    def __init__(self, options):
        super(Select, self).__init__()
        if hasattr(options, 'items'):
            for key, value in options.items():
                self.append(Option())
        else:
            for value in options:
                option = Option(value=unicode(value))
                option.text = option.get('value')
                self.append(option)



@generic
def obj_to_element(obj, **kw):
    return Code(text=json_dumps(obj), class_='json', **kw)

@obj_to_element.when_type(ElementTree.Element)
def obj_to_element_when_element(obj, **kw):
    print "YES IT IS!"
    return obj

@obj_to_element.when_type(href)
def obj_to_element_when_href(obj, **kw):
    return A(href=obj, **kw)

@obj_to_element.when_type(datetime)
def obj_to_element_when_href(obj, **kw):
    return Time(text=obj.isoformat(), **kw)