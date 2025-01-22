from flask import jsonify, request
from models.PublisherModel import Publisher
from config import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity

@jwt_required()
def get_publishers():
    current_user = get_jwt_identity()  # Identity of the logged-in user
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")
    
    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    publishers = Publisher.query.all()
    publisher_list = []
    for publisher in publishers:
        publisher_list.append({
            'id_pub': publisher.id_pub,
            'nama_pub': publisher.nama_pub
        })

    return jsonify({'status': 'success', 'data': {'publishers': publisher_list}}), 200

@jwt_required()
def get_publisher(publisher_id):
    publisher = Publisher.query.get(publisher_id)
    if not publisher:
        return jsonify({'status': 'error', 'message': 'Publisher not found'}), 404
    return jsonify(publisher.to_dict())

@jwt_required()
def add_publisher():
    current_user = get_jwt_identity()
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")

    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    data = request.get_json()
    publisher = Publisher(nama_pub=data['nama_pub'])  # Using 'nama_pub' instead of 'name'
    db.session.add(publisher)
    db.session.commit()
    return jsonify({'message': 'Publisher added successfully!', 'publisher': publisher.to_dict()}), 201

@jwt_required()
def update_publisher(publisher_id):
    current_user = get_jwt_identity()
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")

    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    publisher = Publisher.query.get(publisher_id)
    if not publisher:
        return jsonify({'status': 'error', 'message': 'Publisher not found'}), 404

    data = request.get_json()
    publisher.nama_pub = data.get('nama_pub', publisher.nama_pub)  # Using 'nama_pub' instead of 'name'

    db.session.commit()
    return jsonify({'message': 'Publisher updated successfully!', 'publisher': publisher.to_dict()})

@jwt_required()
def delete_publisher(publisher_id):
    current_user = get_jwt_identity()
    claims = get_jwt()  # Get all claims from the JWT token
    role = claims.get("role")

    # Admin role validation
    if role != 'admin':
        return jsonify({"message": "Admin access required."}), 403

    publisher = Publisher.query.get(publisher_id)
    if not publisher:
        return jsonify({'status': 'error', 'message': 'Publisher not found'}), 404

    db.session.delete(publisher)
    db.session.commit()
    return jsonify({'message': 'Publisher deleted successfully!'})