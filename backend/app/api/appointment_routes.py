from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime
from app.models import Appointment, db

appointment_routes = Blueprint('appointments', __name__)

@appointment_routes.route('/new', methods=['POST'])
@login_required
def create_appointment():
    data = request.json
    appointment = Appointment(
        title=data['title'],
        description=data.get('description'),
        scheduled_time=datetime.fromisoformat(data['scheduled_time']),
        user_id=current_user.id
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify(appointment.to_dict()), 201



@appointment_routes.route('/', methods=['GET'])
@login_required

def get_appointments():
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return jsonify([appt.to_dict() for appt in appointments]), 200


@appointment_routes.route('/<int:appointment_id>', methods=['PUT'])
@login_required
def update_appointment(appointment_id):
    data = request.json
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    appointment.title = data['title']
    appointment.description = data.get('description')
    appointment.scheduled_time = datetime.fromisoformat(data['scheduled_time'])
    db.session.commit()
    return jsonify(appointment.to_dict())


@appointment_routes.route('/<int:appointment_id>', methods=['DELETE'])
@login_required
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200







