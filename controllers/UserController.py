from flask import jsonify, request
from models.UserModel import User
from config import db
import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from datetime import timedelta

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Add role to the JWT claims
    access_token = create_access_token(
        identity=user.username,
        additional_claims={"role": user.role},
        expires_delta=timedelta(hours=20)
    )
    return jsonify({'access_token': access_token})

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password_hash(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

@jwt_required()
def get_users():
    current_user = get_jwt_identity()  # Identity of the logged-in user
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")
    
    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'username': user.username,
            'fullname': user.fullname,
            'role': user.role
        })

    return jsonify({'status': 'success', 'data': {'users': user_list}}), 200

@jwt_required()
def get_user(user_id):
    current_user = get_jwt_identity()  # Identity of the logged-in user
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")

    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404

    return jsonify({
        'status': 'success',
        'data': {'user': user.to_dict()},
        'message': 'User retrieved successfully!'
    }), 200

@jwt_required()
def add_user():
    current_user = get_jwt_identity()
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")

    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    new_user_data = request.get_json()
    hashed_pw = hash_password(new_user_data['password'])
    new_user = User(
        username=new_user_data['username'],
        password=hashed_pw,
        fullname=new_user_data['fullname'],
        role=new_user_data.get('role', 'user')  # Default role is 'user'
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully!', 'user': new_user.to_dict()}), 201

@jwt_required()
def update_user(user_id):
    current_user = get_jwt_identity()
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")

    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    update_data = request.get_json()
    user.username = update_data.get('username', user.username)
    user.password = update_data.get('password', user.password)
    user.fullname = update_data.get('fullname', user.fullname)
    user.role = update_data.get('role', user.role)  # Allow role update

    db.session.commit()
    return jsonify({'message': 'User updated successfully!', 'user': user.to_dict()}), 200

@jwt_required()
def patch_user(user_id):
    current_user = get_jwt_identity()
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")

    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    update_data = request.get_json()
    # Only update fields that are provided
    if 'username' in update_data:
        user.username = update_data['username']
    if 'password' in update_data:
        user.password = hash_password(update_data['password'])  # Update password if provided
    if 'fullname' in update_data:
        user.fullname = update_data['fullname']
    if 'role' in update_data:
        user.role = update_data['role']  # Update role if provided

    db.session.commit()
    return jsonify({'message': 'User updated successfully!', 'user': user.to_dict()}), 200


@jwt_required()
def delete_user(user_id):
    current_user = get_jwt_identity()
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")

    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'}), 200
