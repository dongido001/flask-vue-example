from flask import Flask, request, jsonify, render_template, redirect, send_file
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from werkzeug.security import generate_password_hash, check_password_hash
# from waitress import serve

from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant, ChatGrant

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

import pprint
import os


app = Flask(__name__, static_folder='../dist', static_url_path='')

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['DEBUG'] = True
app.config['MONGODB_DB'] = os.getenv("MONGODB_DB", "vb")
app.config['MONGODB_HOST'] = os.getenv("MONGODB_HOST", "localhost")
app.config['MONGODB_PORT'] = int(os.getenv("MONGODB_PORT", 27017))
app.config['MONGODB_USERNAME'] = os.getenv("MONGODB_USERNAME", "")
app.config['MONGODB_PASSWORD'] = os.getenv("MONGODB_PASSWORD", "")

db = MongoEngine(app)
jwt = JWTManager(app)

from .documents import User, Role

@app.route('/')
@app.route('/api')
def index():
    entry = os.path.join('../dist/', 'index.html')
    return send_file(entry)

# TODO. add @jwt_required
@app.route('/api/generate_video_token', methods=['POST'])
# @jwt_required
def generate_video_token():

    # current_user = get_jwt_identity()

    # required for all twilio access tokens
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    api_key = os.getenv('TWILIO_API_KEY')
    api_secret = os.getenv('TWILIO_API_SECRET')
    service_id = os.getenv('TWILIO_SERVICE_ID')

    identity = request.json.get('identity')

    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a Video grant and add to token
    video_grant = VideoGrant()
    chat_grant = ChatGrant(service_id)
    token.add_grant(video_grant)
    token.add_grant(chat_grant)

    # Return token info as JSON
    return jsonify({
        'token': token.to_jwt().decode()
    })


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'role': user['role']}

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user['email']

@app.route('/api/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({
            "status": "error",
            "msg": "Missing JSON in request",
        }), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    _user = User.objects(email=email).first()

    if not _user or not _user.check_password_hash(password):
        return jsonify({"msg": "Bad email or password"}), 401

    user_data = {
        'email': email,
        'role': _user.role
    }

    access_token = create_access_token(identity=user_data)
    return jsonify(access_token=access_token, status="success"), 200

@app.route('/api/add_user', methods=['POST'])
def add_new_user():
    if not request.is_json:
        return jsonify({
            "status": "error",
            "msg": "Missing JSON in request",
        }), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('last_name', None)
    title = request.json.get('title', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    if not first_name:
        return jsonify({"msg": "Missing first_name parameter"}), 400
    if not last_name:
        return jsonify({"msg": "Missing last_name parameter"}), 400
    if not title:
        return jsonify({"msg": "Missing title parameter"}), 400

    _user = User.objects(email=email).first()

    if _user:
        return jsonify({"msg": "User with that email already exists"}), 401
    
    _role = Role.objects(role="player").first()

    new_user = User(email=email, password=generate_password_hash(password), 
                    first_name=first_name, last_name=last_name, title=title, role=_role.id)
    new_user.save()

    user_data = {
        'email': 'test',
        'role': 'player'
    }

    access_token = create_access_token(identity=user_data)
    return jsonify(access_token=access_token, status="success"), 200
    
@app.route('/api/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/api/add_role')
def add_role():
    # new_role1 = Role(role="player")
    # new_role2 = Role(role="admin")
    # new_role3 = Role(role="facilitator")
    # new_role1.save(); new_role2.save(); new_role3.save(); 

    pass

if __name__ == '__main__':
    # serve(app, host='0.0.0.0', port=5000)
    app.run()

