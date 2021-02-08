from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required
from model.user import User, get_hashed_pass
from db import db

endpoints_bp = Blueprint('endpoints', __name__)

@endpoints_bp.route('/register', methods=['POST'])
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

    already_taken = User.query.filter((User.username==user_data['username'])).first()
    if already_taken:
        return jsonify({
            'status': 'fail',
            'message': 'The username has been already taken'
        }), 422
    
    already_taken = User.query.filter((User.username==user_data['email'])).first()
    if already_taken:
        return jsonify({
            'status': 'fail',
            'message': 'There is already a user with this email'
        }), 422

    user_object = User(user_data['username'], user_data['email'], get_hashed_pass(user_data['password']))
    user_object.save()
    return jsonify({
        'status': 'success'
    }), 200


# @endpoints_bp.route("/identity")
# @jwt_required
# def remove_myself():

    