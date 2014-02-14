from flask import Flask, url_for, request
from flask.ext.inform import Inform
from flask.ext.inform.view import View, Select, Input
from collections import OrderedDict

app = Flask(__name__)
inform = Inform(app)


class Multiplier(View):
    
    def __init__(self, multiplier):
        self.multiplier = multiplier
        self.base_url = url_for('Multiplier.get', multiplier=self.multiplier)
        logging.warning('base url = %r', self.base_url)
        self.n = None
        
    @View.form
    def multiply(self, n=Input()):
        self.n = n
        return self
        
    @View.value
    def answer(self):
        if self.n is not None:
            self.n * self.multiplier


class Demo(View):
    
    @View.form
    def multiplier(self, multiplier=Select([1, 2, 4])):
        logging.warning('multipolie')
        return Multiplier(multiplier)

inform.add_url_rules('/', Demo)
inform.add_url_rules('/multiplier/<int:multiplier>', Multiplier)

if __name__ == '__main__':
    app.run(debug=True)