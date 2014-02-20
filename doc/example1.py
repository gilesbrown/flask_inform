from flask import Flask
from flask.ext.inform import Inform, Document

app = Flask(__name__)
inform = Inform(app)


class LibraryCatalog(Document):
    """ A catalog of library contents. """
   
    
inform.add_url_rules(LibraryCatalog, '/')


if __name__ == '__main__':
    app.run(debug=True)