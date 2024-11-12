from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import send_from_directory
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household_services.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue(path):
    if path != "" and os.path.exists(app.root_path + '/frontend/' + path):
        return send_from_directory('frontend', path)
    else:
        return send_from_directory('frontend', 'index.html')