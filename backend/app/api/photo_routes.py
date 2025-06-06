from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import Photo

photo_routes = Blueprint('photos', __name__)