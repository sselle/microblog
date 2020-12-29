from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# init app and config
app=Flask(__name__)
app.config.from_object(Config)

# create and initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# create and initialize login manager
login = LoginManager(app)

from app import routes, models