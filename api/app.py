from flask import Flask, request, jsonify, render_template, redirect
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from werkzeug.security import generate_password_hash, check_password_hash
from waitress import serve

from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

import pprint
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['DEBUG'] = True
app.config['MONGODB_DB'] = os.getenv("MONGODB_DB", "vb")
app.config['MONGODB_HOST'] = os.getenv("MONGODB_HOST", "localhost")
app.config['MONGODB_PORT'] = int(os.getenv("MONGODB_PORT", 27017))
app.config['MONGODB_USERNAME'] = os.getenv("MONGODB_USERNAME", "")
app.config['MONGODB_PASSWORD'] = os.getenv("MONGODB_PASSWORD", "")
db = MongoEngine(app)
jwt = JWTManager(app)

from documents import User

@app.route('/')
def index():
    return jsonify([

    ])

# TODO. add @jwt_required
@app.route('/generate_video_token', methods=['POST'])
def generate_video_token():

    # required for all twilio access tokens
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    api_key = os.getenv('TWILIO_API_KEY')
    api_secret = os.getenv('TWILIO_API_SECRET')

    identity = request.json.get('identity')

    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a Video grant and add to token
    video_grant = VideoGrant()
    token.add_grant(video_grant)

    # Return token info as JSON
    return jsonify({
        'token': str(token.to_jwt())
    })


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'roles': user['role']}

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user['username']

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({
            "status": "error",
            "msg": "Missing JSON in request",
        }), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    _user = User.objects(username=username).first()

    if not _user or not _user.check_password_hash(password):
        return jsonify({"msg": "Bad username or password"}), 401

    user_data = {
        'username': 'test',
        'role': 'Admin'
    }

    access_token = create_access_token(identity=user_data)
    return jsonify(access_token=access_token), 200


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/add_user')
def add_user():
    # new_user = User()
    # new_user.username = 'test'
    # new_user.password = generate_password_hash('test')
        
    # new_user.save()

    # print(new_user)
    pass

if __name__ == '__main__':
    # serve(app, host='0.0.0.0', port=5000)
    app.run()

