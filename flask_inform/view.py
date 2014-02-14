import inspect
from cStringIO import StringIO
from xml.etree.ElementTree import Element, ElementTree


UNDEFINED = object()
NULL = unicode('null')
NL = b'\n'
TAB = b'\t'


# http://effbot.org/zone/element-lib.htm#prettyprint
def indent(elem, level=0, per_level=TAB):
    i = NL + per_level * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + per_level
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class ViewType(type):

    descriptors = []

    class Descriptor(object):
        def __init__(self):
            ViewType.descriptors.append(self)


    def __new__(metacls, name, bases, dict_):

        # To determine ordering we need to look-up the items by object
        descriptors = set()

        for objname, obj in dict_.items():

            if objname.startswith('_'):
                continue

            # Ensure descriptors know their own names
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

            descriptors.add(obj)

        __descriptors__ = []
        for obj in metacls.descriptors:
            if obj in descriptors:
                __descriptors__.append(obj.__name__)

        # This will only ever be non-empty if you write a nested class
        metacls.descriptors = [obj for obj in metacls.descriptors if obj not in descriptors]

        dict_['__descriptors__'] = __descriptors__

        cls = super(ViewType, metacls).__new__(metacls, name, bases, dict_)
        return cls



class View(object):

    __metaclass__ = ViewType

    def _items(self):
        return [getattr(self, name) for name in self.__descriptors__]

    def _to_html(self):
        html = Element('html')
        body = Element('body')
        body.extend(item._to_etree() for item in self._items())
        html.append(body)
        indent(html)
        sio = StringIO()
        sio.write('<!DOCTYPE html>\n')
        ElementTree(html).write(sio)
        return sio.getvalue()


class Form(ViewType.Descriptor):

    def __init__(self, function):
        super(Form, self).__init__()
        self.function = function

    def __get__(self, obj, objtype):
        class Blah(object):
            def __init__(self, obj, function):
                self.obj = obj
                self.function = function

            def _to_etree(self):
                print "OBJ: %r" % obj
                return Element('form')
            def __call__(self, *args, **kwargs):
                self.function(*args, **kwargs)
        return Blah(obj, self.function)

    def _to_etree(self):
        return Element('form')

form = Form



#    def __render__(self):
#        print "RENDER ME", self.__view_items__, getattr(self, self.__view_items__[0])
#        items = [Item(getattr(self, item), item) for item in self.__view_items__]
#        print "ITEMS?", items
#        status_code = 200
#        return render_template('inform.html', items=items, status_code=status_code), status_code



class Value(object):
    def __init__(self):
        ViewType._item_order.append(self)
    def __get__(self, obj, objtype):
        return obj.__dict__.get(self.__name__, NULL)
