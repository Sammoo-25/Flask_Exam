from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
#, template_folder='.//templates', static_folder='.//static'
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# from .routes import *


# from . import routes


from .routes import home, product, registration, user

from .models import Users
