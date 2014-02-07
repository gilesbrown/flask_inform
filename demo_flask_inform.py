from flask import Flask, url_for
from flask.ext.inform import Inform, View, Value, rendered, Link
from collections import OrderedDict

app = Flask(__name__)
inform = Inform(app)

philosophers = {
    1: {
        'name': 'Socrates',
    },
    2: {
        'name': 'Plato',
    },
}


class PhilosopherList(View):

    philosophers = Value()

    def __init__(self, philosophers):
        self.philosophers = list(philosophers)

class classmethod(classmethod):
    def __init__(self, function):
        super(classmethod, self).__init__(function)
        self.__name__ = function.__name__




class Philosopher(View):

    name = Value()
    nationality = Value()
    yob = Value()

    def __init__(self, id_):
        self.id = id_
        self.__dict__.update(philosophers[id_])
        print "INIT(%r)" % id_
        print "ID: %r" % self.id


    def post(cls):
        pass

    def summarize(self, items=('name', 'nationality')):
        summary = OrderedDict()
        summary['url'] = Link(url_for('Philosopher.get', id=self.id))
        for item in self.__view_items__:
            summary[item] = getattr(self, item)
        return summary

    #@rendered
    @classmethod
    def index(cls):
        #return PhilosopherList(cls(id).summarize() for id in sorted(philosophers.keys()))
        #phil0 = cls(1)
        #summary = phil0.summarize()
        #print phil0, summary, hasattr(phil0, 'id')
        #return PhilosopherList([summary])
        return PhilosopherList(cls(id).summarize() for id in sorted(philosophers.keys()))

    def get(self):
        print "GET GET GET"
        return self

class Demo(View):

    philosopher = Link('Philosopher.index')

print type(Philosopher), type(Philosopher(1)), Philosopher(1).id

inform.add_view_routes(Philosopher)
inform.add_view_routes(Demo, '/')


if __name__ == '__main__':
    app.run(debug=True)
