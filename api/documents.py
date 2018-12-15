from flask_mongoengine.wtf import model_form
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Role(db.Document):
    """Roles: player, admin, facilitator"""
    role = db.StringField(required=True, max_length=50)

class User(db.Document):
    email = db.StringField(required=True)
    password = db.StringField()
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    title = db.StringField(max_length=50)
    role = db.ReferenceField(Role)

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % (self.username)
