import os
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_authenticator import app

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('JWT_AUTH_DATABASE_URI')
db = SQLAlchemy(app)

import model.user
