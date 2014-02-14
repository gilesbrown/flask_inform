from nose.tools import eq_
from flask_inform.view import View, form


def test_view():

    class MyView(object):

        @form
        def myform(self):
            return 'you called?'

    instance = MyView()

    eq_(instance.myform._to_etree(), '<html>')
