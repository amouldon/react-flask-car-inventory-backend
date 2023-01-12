from flask_sqlalchemy import SQLAlchemy
import uuid, secrets
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow
from datetime import datetime
db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default='', unique=True)

    def __init__(self, email, password=''):
        self.id = self.set_id()
        self.email = email
        self.token = self.set_token(30)
        self.password = self.set_password(password)

    def set_token(self, length):
        return secrets.token_hex(length)
        
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return 'User ' + str(self.email) + ' has been added to the database'


class Car(db.Model):
    id = db.Column(db.String, primary_key=True)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    year = db.Column(db.String(100))
    color = db.Column(db.String(50), nullable=True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, year, brand, model, color, user_token):
        self.id = self.set_id()
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color
        self.user_token = user_token
    
    def __repr__(self):
        return 'A car has just been added to the database'
    
    def set_id(self):
        return (secrets.token_urlsafe())

class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'brand','model', 'year', 'color']

car_schema = CarSchema()
cars_schema = CarSchema(many=True)