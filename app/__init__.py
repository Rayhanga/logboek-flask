from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

from .config import Config

# from .auths import auth

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

from app import authenticators, routes, models, errors