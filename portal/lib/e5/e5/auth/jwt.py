from e5 import app, portal, login_manager

from flask import request, render_template, redirect, flash, url_for, Markup
from flask_login import UserMixin, login_required, current_user, login_user, logout_user, fresh_login_required

from flask_jwt import JWT, jwt_required, current_identity

from e5.auth import User
from bson.objectid import ObjectId

from datetime import datetime, timedelta


## JWT IMPL
def authenticate(username, password):

    user = app.config['USER_COLLECTION'].find_one({"username": username.lower()})
    if user == None:
        print "JWT: USER NOT FOUND ERROR"
        return None

    user_obj = User(user['_id'], user['username'], user['fullname'], user['otp_secret'])

    if user and User.validate_login(user['password'], password):
        print "JWT: LOGIN SUCCESS"
        return user_obj

    print "JWT: INCORRECT PASSWORD"
    return None

def identity(payload):
    id = payload['identity']
    print "id=" + id
    user = app.config['USER_COLLECTION'].find_one({'_id': ObjectId(id)})
    if user == None:
        print "JWT: USER NOT FOUND ERROR"
        return None
    user_obj = User(user['_id'], user['username'], user['fullname'], user['otp_secret'])
    return user_obj

jwt = JWT(app, authenticate, identity)

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


## ALTERNATIVE
"""
@app.route('api/auth')
def create_token(user):
    payload = {
        # subject
        'sub': user.id,
        #issued at
        'iat': datetime.utcnow(),
        #expiry
        'exp': datetime.utcnow() + timedelta(days=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token.decode('unicode_escape')
"""
