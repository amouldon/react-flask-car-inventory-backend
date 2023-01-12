from flask import Flask
from .auth.routes import auth
from .api.routes import api
from config import Config
from models import db, ma
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
app.register_blueprint(auth)
app.register_blueprint(api)

db.init_app(app)
ma.init_app(app)

migrate = Migrate(app, db)
