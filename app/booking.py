from flask import request, jsonify
from .models import Booking, Train, User
from . import db
from .routes import api_blueprint  # Import api_blueprint from routes.py

# Book a seat
@api_blueprint.route('/book', methods=['POST'])
def book_seat():
    data = request.get_json()

    # Check for required data
    if not data.get('user_id') or not data.get('train_id'):
        return jsonify({'message': 'Missing user_id or train_id!'}), 400

    # Find the user and the train
    user = User.query.get(data['user_id'])
    train = Train.query.get(data['train_id'])

    if not user or not train:
        return jsonify({'message': 'Invalid user or train!'}), 404

    # Check if seats are available
    if train.available_seats <= 0:
        return jsonify({'message': 'No available seats!'}), 400

    # Create a new booking
    new_booking = Booking(user_id=user.id, train_id=train.id)
    db.session.add(new_booking)

    # Decrement available seats
    train.available_seats -= 1
    db.session.commit()

    return jsonify({'message': 'Seat booked successfully!'}), 201

# Get specific booking details
@api_blueprint.route('/booking/<int:booking_id>', methods=['GET'])
def get_booking_details(booking_id):
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({'message': 'Booking not found!'}), 404

    booking_data = {
        'user_id': booking.user_id,
        'train_id': booking.train_id,
        'timestamp': booking.timestamp
    }

    return jsonify({'booking': booking_data}), 200
