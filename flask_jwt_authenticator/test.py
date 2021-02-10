from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
import json
from endpoints import endpoints_bp
import unittest
from model.user import User
from db import db

class TestAuthentication(TestCase):

    username = 'Bob'
    email = 'bob@alice.com'
    password = 'BobAlice123_'

    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'SuperSecretPepperSalt'
        app.register_blueprint(endpoints_bp)
        db.init_app(app)
        return app

    def test_registration(self):
        response = self.client.post('/register', data=json.dumps({'username': self.username, 'email': self.email, 'password': self.password}),
                                    content_type='application/json')
        self.assert200(response, f"Error registering user {self.username}, email {self.email}, password {self.password}")

    def test_login(self):
        response = self.client.post('/auth', data=json.dumps({'username': self.username, 'password': self.password}), 
                                    content_type='application/json')

        self.assert200(response, f"Error logging in with user {self.username}")

    def setUp(self):        
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()