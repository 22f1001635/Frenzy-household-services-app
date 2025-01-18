from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config) #initialize object import

from api import *

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run(debug=True)