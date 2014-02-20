from flask import Flask
from flask.ext.inform import Inform, Document, element_property

app = Flask(__name__)
inform = Inform(app)

model = {
    1: {'isbn10': '140523069X', 'title': 'Really Useful Engines'},
}


class Book(Document):
    """ A book. """
    
    def __init__(self, id):
        self.id = id
    
    @Document.property
    def isbn10(self):
        return model[self.id].get('isbn10')


class LibraryCatalog(Document):
    """ A catalog of library content. """
    
    @element
    def created_at(self):
        """ Time of creation. """
        return datetime(2014, 2, 14)
   
    #@Document.property 
    #def book(self):
    #    return Book(1)
    
    #@Document.property
    #def books(self):
    #    return [dict((url, url) for id in model]
    @Document.property
    def offset 
    
                     
    @Document.get
    def more(self, offset=Input()):
        self.offset = offset
        self.more.offset = offset + 10
        return self
    
inform.add_rules(LibraryCatalog, '/')
inform.add_rules(Book, '/book/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)