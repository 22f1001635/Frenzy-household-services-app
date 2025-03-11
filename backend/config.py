import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    UPLOAD_FOLDER = os.path.abspath(os.getenv('UPLOAD_FOLDER', 'instance/uploads'))
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg').split(','))
    PROFILE_PIC_FOLDER = os.path.join(UPLOAD_FOLDER, 'profile_pictures')
    SERVICE_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'services')