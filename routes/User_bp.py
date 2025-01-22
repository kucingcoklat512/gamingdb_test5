from flask import Blueprint
from controllers.UserController import login, get_users, get_user, update_user, patch_user, delete_user, add_user

user_bp = Blueprint('User_bp', __name__)

# Route for login user
user_bp.route('/api/login', methods=['POST'])(login)

# Get all users
user_bp.route('/api/users', methods=['GET'])(get_users)

# Get user by ID
user_bp.route('/api/users/<int:user_id>', methods=['GET'])(get_user)

# Add new user
user_bp.route('/api/users', methods=['POST'])(add_user)

# Update user
user_bp.route('/api/users/<int:user_id>', methods=['PUT'])(update_user)

# Partially update a user (patch)
user_bp.route('/api/users/<int:user_id>', methods=['PATCH'])(patch_user)

# Delete user
user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])(delete_user)
