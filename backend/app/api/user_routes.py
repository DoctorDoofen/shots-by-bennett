from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, db

user_routes = Blueprint('users', __name__)


@user_routes.route('/')
@login_required
def users():
    """
    Query for all users and returns them in a list of user dictionaries
    """
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:id>')
@login_required
def user(id):
    """
    Query for a user by id and returns that user in a dictionary
    """
    user = User.query.get(id)
    return user.to_dict()


# Update current user
@user_routes.route('/update', methods=['PUT'])
@login_required
def update_current_user():
    user = User.query.get(current_user.id)

    if not user:
        return {"error": "User not found"}, 404

    data = request.get_json()

    username = data.get("username")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    if username:
        user.username = username
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email
    if password:
        user.password = password  # This uses the `@password.setter` to hash it

    db.session.commit()

    return {
        "message": "User account updated successfully",
        "user": user.to_dict()
    }






# Delete current user
@user_routes.route('/delete', methods=['DELETE'])
@login_required
def delete_current_user():
    user = User.query.get(current_user.id)

    if not user:
        return {"error": "User not found"}, 404

    db.session.delete(user)
    db.session.commit()

    return {"message": "User account deleted successfully"}





