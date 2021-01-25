import os
import hashlib
from flask import Flask
from flask_jwt import JWT
from werkzeug.security import safe_str_cmp

app = Flask(__name__)

from model import db
db.create_all()

from model import User


def authenticate(username, password):
    db_user = User.query.filter_by(username=username).first()
    hasher = hashlib.sha256()
    hasher.update(bytes(password, 'utf-8'))
    hasher.update(os.getenv('JWT_AUTH_SECRET_KEY'))
    if safe_str_cmp(db_user.password.encode('utf-8'), hasher.hexdigest()):
        return db_user

def identity(payload):
    user_id = payaload['identity']
    return User.query.filter_by(id=user_id).first()

jwt = JWT(app, authenticate, identity)

@app.route('/identity')
@jwt_required()
def get_identity():
    return f"{current_identity}"


if __name__ == "__main__":
    if os.getenv('JWT_AUTH_DEBUG'):
        app.run()
    else:
        bjoern.run(app, "0.0.0.0", 5000)