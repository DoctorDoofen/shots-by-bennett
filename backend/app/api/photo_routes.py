from flask import Blueprint, request, jsonify
from app.models import db, Photo
from flask_login import login_required

photo_routes = Blueprint('photos', __name__)

# UPLOAD Photo
@photo_routes.route('/', methods=['POST'])
@login_required
def create_photo():
    data = request.get_json()
    filename = data.get("filename")

    if not filename:
        return {"error": "Filename is required"}, 400

    photo = Photo(filename=filename)
    db.session.add(photo)
    db.session.commit()

    return jsonify(photo.to_dict()), 201

# GET all photos
@photo_routes.route('/', methods=['GET'])
def get_all_photos():
    photos = Photo.query.all()
    return jsonify([photo.to_dict() for photo in photos])

# GET one photo
@photo_routes.route('/<int:id>', methods=['GET'])
def get_photo(id):
    photo = Photo.query.get(id)
    if not photo:
        return {"error": "Photo not found"}, 404
    return jsonify(photo.to_dict())

# UPDATE photo
@photo_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_photo(id):
    photo = Photo.query.get(id)
    if not photo:
        return {"error": "Photo not found"}, 404

    data = request.get_json()
    filename = data.get("filename")

    if filename:
        photo.filename = filename
        db.session.commit()

    return jsonify(photo.to_dict())

# DELETE photo
@photo_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_photo(id):
    photo = Photo.query.get(id)
    if not photo:
        return {"error": "Photo not found"}, 404

    db.session.delete(photo)
    db.session.commit()

    return {"message": "Photo deleted successfully"}
