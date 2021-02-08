from db import db
import hashlib
import os

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

def get_hashed_pass(password):
    hasher = hashlib.sha256()
    hasher.update(bytes(password, 'utf-8'))
    hasher.update(bytes(os.getenv('JWT_AUTH_SECRET_KEY', 'supersecretpeppersalt'), 'utf-8'))
    return hasher.hexdigest()