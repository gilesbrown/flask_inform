from flask import Flask
from flask.ext.inform import Inform, Document
from datetime import datetime

app = Flask(__name__)
inform = Inform(app)

class Book(Document):
    
    def __init__(self, id):
        self.id = id
        

class LibraryCatalog(Document):
    """ The service for accessing library contents. """
    
    __elements__ = ['created_at', 'book_1']
    
    def __init__(self):
        self.created_at = datetime.utcnow()
        self.book_1 = Book.url_for(id=1)
   
inform.add_url_rules(LibraryCatalog, '/')
inform.add_url_rules(Book, '/book/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)