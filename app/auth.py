from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
import jwt
import datetime
from flask import current_app

# User registration logic
def register():
    data = request.get_json()
    
    print("Hellooooo", data)
    if not data.get('username') or not data.get('password') or not data.get('role'):
        return jsonify({'message': 'Missing data!'}), 400
    
    
    # hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    hashed_password = generate_password_hash(data['password'], method='HS256')


    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'message': 'Username already exists!'}), 400
    
    new_user = User(username=data['username'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully!'}), 201

# User login logic
def login():
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing data!'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid username or password!'}), 401
    
    token = jwt.encode({
    'user_id': user.id,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
}, current_app.config['SECRET_KEY'], algorithm='HS256')

    print("Generated Token:", token)

    
    return jsonify({'token': token}), 200
