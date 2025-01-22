from flask import jsonify, request
from models.GenreModel import Genre
from config import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity

@jwt_required()
def get_genres():
    current_user = get_jwt_identity()  # Identity of the logged-in user
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")
    
    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    genres = Genre.query.all()
    genre_list = []
    for genre in genres:
        genre_list.append({
            'id_genre': genre.id_genre,
            'nama_genre': genre.nama_genre
        })

    return jsonify({'status': 'success', 'data': {'genres': genre_list}}), 200

@jwt_required()
def get_genre(genre_id):
    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({'status': 'error', 'message': 'Genre not found'}), 404
    return jsonify(genre.to_dict())

@jwt_required()
def add_genre():
    current_user = get_jwt_identity()
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")

    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    data = request.get_json()
    # Validasi input
    if not data.get('nama_genre'):
        return jsonify({'status': 'error', 'message': 'Name is required'}), 400
    
    genre = Genre(nama_genre=data['nama_genre'])
    db.session.add(genre)
    db.session.commit()
    return jsonify({'message': 'Genre added successfully!', 'genre': genre.to_dict()}), 201

@jwt_required()
def update_genre(genre_id):
    current_user = get_jwt_identity()
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")

    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({'status': 'error', 'message': 'Genre not found'}), 404

    data = request.get_json()
    genre.nama_genre = data.get('nama_genre', genre.nama_genre)  # Hanya memperbarui nama jika ada

    db.session.commit()
    return jsonify({'message': 'Genre updated successfully!', 'genre': genre.to_dict()})

@jwt_required()
def delete_genre(genre_id):
    current_user = get_jwt_identity()
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")

    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({'status': 'error', 'message': 'Genre not found'}), 404

    db.session.delete(genre)
    db.session.commit()
    return jsonify({'message': 'Genre deleted successfully!'})
