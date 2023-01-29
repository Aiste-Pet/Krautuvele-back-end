import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.app_context().push()


basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.db")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

from app.admin import *
from app import views
