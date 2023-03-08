import os
from sqlalchemy import MetaData
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_praetorian import Praetorian


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

app = Flask(__name__)
CORS(app)
app.app_context().push()


basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_prefixed_env()
app.config["SQLALCHEMY_DATABASE_URI"]
app.config["SECRET_KEY"]

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)
ma = Marshmallow(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
guard = Praetorian()

from app.admin import *
from app import views
