from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_required,logout_user,login_user,current_user
from flask_restful import Api
from flask_cors import CORS
from main import app

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
api = Api(app)
CORS(app, supports_credentials=True)