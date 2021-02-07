import os
import hashlib
import logging
from db import db
from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import safe_str_cmp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('JWT_AUTH_DATABASE_URI')
print(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from user import User
db.init_app(app)

with app.app_context():
    db.create_all()

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

@app.route('/register', methods=['POST'])
def register():
    user_data = request.get_json()
    if not user_data:
        return jsonify({'status': 'fail', 
                        'message': 'Data must be provided',
                        }), 400

    if not 'username' in user_data or not user_data['username']:
        return jsonify({
            'status': 'fail',
            'message': 'The username must be specified'
        }), 400
    if not 'email' in user_data or not user_data['email']:
        return jsonify({
            'status': 'fail',
            'message': 'The email must be specified'
        }), 400
    if not 'password' in user_data or not user_data['password']:
        return jsonify({
            'status': 'fail',
            'message': 'A password must be specified'
        }), 400

    already_taken = User.query.filter((User.username==user_data['username']) | (User.email==user_data['email'])).first()
    if already_taken:
        return jsonify({
            'status': 'fail',
            'message': 'The username is already taken'
        }), 422
    
    user_object = User(user_data['username'], user_data['email'], user_data['password'])
    user_object.save()
    return jsonify({
        'status': 'success',
        'user': user_object
    }), 200

@app.errorhandler(500)
def on_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal error'
    }), 500

if __name__ == "__main__":
    app.run()