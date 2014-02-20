from flask import url_for
from .elements import obj_to_element, href

class DocumentMetaType(type):
    def __new__(meta, name, bases, clsdict):
        #clsdict['__init__'] = wrapped_init(clsdict.get('__init__'))
        #clsdict['__descriptors__'] = Descriptor.pop_order(clsdict)
        return super(DocumentMetaType, meta).__new__(meta, name, bases, clsdict)


class Document(object):
    """ A base class for Inform documents. """
    
    __metaclass__ = DocumentMetaType
    __elements__ = []
    
    def iter_elements(self):
        return [obj_to_element(getattr(self, name), id=name) for name in self.__elements__]
   
    @classmethod 
    def url_for(cls, **kwargs):
        return href(url_for('Book', **kwargs))