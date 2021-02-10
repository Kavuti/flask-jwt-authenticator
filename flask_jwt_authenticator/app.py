import os
import logging
from db import db
from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import safe_str_cmp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('JWT_AUTH_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('JWT_AUTH_SECRET_KEY')

from endpoints import endpoints_bp
from model.user import User, get_hashed_pass
db.init_app(app)
app.register_blueprint(endpoints_bp)

with app.app_context():
    db.create_all()

def authenticate(username, password):
    db_user = User.query.filter_by(username=username).first()
    if db_user and safe_str_cmp(db_user.password.encode('utf-8'), get_hashed_pass(password)):
        return db_user


def identity(payload):
    user_id = payaload['identity']
    return User.query.filter_by(id=user_id).first()


jwt = JWT(app, authenticate, identity)


@app.errorhandler(500)
def on_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal error'
    }), 500


@app.route("/identity")
def identity():
    return jsonify({
        "identity": f"{current_identity}"
    })

@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()


if __name__ == "__main__":
    app.run()