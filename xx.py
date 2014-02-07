#class classmethod(classmethod):
#    def __init__(self, function):
#        super(classmethod, self).__init__(function)
#        self.__name__ = function.__name__
#

def rendered(f):
    def render(

class Boo(object):
    @classmethod
    def foo(cls, a):
        print cls, a


boo = Boo()
boo.foo(2)
print boo.foo.__name__
