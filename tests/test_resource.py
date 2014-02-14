from nose.tools import eq_
from xml.etree.ElementTree import tostring
from flask import Flask
from flask_inform.view import View, Input, Select


class ViewLike(object):

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)
    
    def url_for(self, function):
        return '/{0.__name__}'.format(function)


def test_form_input():
    
    class Multiplier(ViewLike):
        @View.form
        def multiply(self, n=Input()):
            return n * self.multiplier
           
    view = Multiplier(multiplier=2)
    eq_(tostring(view.multiply), '<form><input name="n" /></form>')
    eq_(view.multiply(n=3), 6)
   
    
def test_form_select():
    
    options = [1, 2]

    class Chooser(ViewLike):
        @View.form
        def choose(self, s=Select(options)):
            return options.index(s)
           
    view = Chooser()
    eq_(tostring(view.choose), 
        ''.join((
          '<form>',
            '<select name="s">',
              '<option value="1">1</option>',
              '<option value="2">2</option>',
            '</select>',
          '</form>',
        ))
    )
    eq_(view.choose(s=2), 1)
    
  
def body_inner_html(e, startswith='<html><body>', endswith='</body></html>'):
    s = tostring(e)
    eq_(s[:len(startswith)], startswith)
    eq_(s[-len(endswith):], endswith)
    return s[len(startswith):-len(endswith)]


def test_view_value(): 
    
    class Person(View):
        @View.value
        def age(self):
            return 43
        
    person = Person()
    expected = '<code class="json" id="age">43</code>'
    eq_(body_inner_html(person.etree()), expected)
    

def test_view_link(): 
    
    class Person(View):
        @View.link
        def father(self):
            return '/person/415'  # people are numbers right?
        
    person = Person()
    expected = '<a href="/person/415" id="father" />'
    eq_(body_inner_html(person.etree()), expected)