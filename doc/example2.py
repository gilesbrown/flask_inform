from flask import Flask
from flask.ext.inform import Inform, Document
from datetime import datetime

app = Flask(__name__)
inform = Inform(app)



class LibraryCatalog(Document):
    """ The service for accessing library contents. """
    
    __elements__ = ['created_at', 'book_1']
    
    def __init__(self):
        self.created_at = datetime.utcnow()
       
   
inform.add_url_rules(LibraryCatalog, '/')


if __name__ == '__main__':
    app.run(debug=True)