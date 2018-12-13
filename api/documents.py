from flask_mongoengine.wtf import model_form
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Document):
    username = db.StringField()
    password = db.StringField()

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % (self.username)
