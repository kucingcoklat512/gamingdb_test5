from flask import jsonify, request
from models.RatingModel import Rating
from config import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity

@jwt_required()
def get_ratings():
    current_user = get_jwt_identity()  # Identity of the logged-in user
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")
    
    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    ratings = Rating.query.all()
    rating_list = []
    for rating in ratings:
        rating_list.append({
            'id_rate': rating.id_rate,
            'nama_rate': rating.nama_rate
        })

    return jsonify({'status': 'success', 'data': {'ratings': rating_list}}), 200

@jwt_required()
def get_rating(id_rate):
    rating = Rating.query.get(id_rate)
    if not rating:
        return jsonify({'status': 'error', 'message': 'Rating not found'}), 404
    return jsonify(rating.to_dict())

@jwt_required()
def add_rating():
    current_user = get_jwt_identity()
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")

    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    data = request.get_json()
    rating = Rating(nama_rate=data['nama_rate'])  # Using 'nama_rate' for rating name
    db.session.add(rating)
    db.session.commit()
    return jsonify({'message': 'Rating added successfully!', 'rating': rating.to_dict()}), 201

@jwt_required()
def update_rating(id_rate):
    current_user = get_jwt_identity()
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")

    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    rating = Rating.query.get(id_rate)
    if not rating:
        return jsonify({'status': 'error', 'message': 'Rating not found'}), 404

    data = request.get_json()
    rating.nama_rate = data.get('nama_rate', rating.nama_rate)  # Using 'nama_rate' for rating name

    db.session.commit()
    return jsonify({'message': 'Rating updated successfully!', 'rating': rating.to_dict()})

@jwt_required()
def delete_rating(id_rate):
    current_user = get_jwt_identity()
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")

    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    rating = Rating.query.get(id_rate)
    if not rating:
        return jsonify({'status': 'error', 'message': 'Rating not found'}), 404

    db.session.delete(rating)
    db.session.commit()
    return jsonify({'message': 'Rating deleted successfully!'})
