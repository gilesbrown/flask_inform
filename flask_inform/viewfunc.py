import logging
from flask import request
from xml.etree.ElementTree import ElementTree, Element
#from .elements import Element
from cStringIO import StringIO


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

def render_doc(doc, http_status=None):
    content = StringIO()
    content.write('<!DOCTYPE html>\n')
    html = Element('html')
    head = Element('head')
    head.append(Element('meta', name='http-method', content=request.method))
    if http_status is not None:
        head.append(Element('meta', name='http-status-code', content=unicode(http_status)))
    script= Element('script', src="/informed.js", text=' ')
    script.text = ' '
    head.append(script)
    html.append(head)
    body = Element('body')
    body.extend(doc.iter_elements())
    html.append(body)
    indent(html)
    tree = ElementTree(html)
    tree.write(content, method='html')
    return content.getvalue()


class ViewFunc(object):
    
    def __init__(self, document_class):
        self.document_class = document_class
        
    def __call__(self, *args, **kwargs):
        print "CALL:", args, kwargs
        instance = self.document_class(*args, **kwargs)
        return render_doc(instance, 200), 200
    
    