from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
import secrets
from flask_login import UserMixin, LoginManager

# Flask Security of passwords
from werkzeug.security import check_password_hash, generate_password_hash

# Import Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    username = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    user_date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref = 'owner', lazy = True)

    def __init__(self, email, username, password, first_name = '', last_name = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.username = username
        self.token = self.set_token()

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)
    
    def __repr__(self):
        return f"User {self.email} has been added to our Database!"
    
class Character(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    api_description = db.Column(db.String(10000))
    movies_appeared = db.Column(db.String(10000))
    super_power = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, api_description, movies_appeared, super_power, date_created, user_token):
        self.id = self.set_id()
        self.name = name
        self.description = api_description
        self.movies_appeared = movies_appeared
        self.super_power = super_power
        self.date_created = date_created
        self.user_token = user_token
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"Character {self.name} has been added to the Database!"

class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'api_description', 'movies_appeared', 'super_power', 'date_created']

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many = True)