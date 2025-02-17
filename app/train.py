from flask import request, jsonify
from .models import Train
from . import db

# Import the api_blueprint from routes.py
from .routes import api_blueprint

# Add a new train - Admin only
@api_blueprint.route('/train', methods=['POST'])
def add_train():
    data = request.get_json()
    
    if not data.get('name') or not data.get('source') or not data.get('destination') or not data.get('total_seats'):
        return jsonify({'message': 'Missing data!'}), 400
    
    new_train = Train(
        name=data['name'],
        source=data['source'],
        destination=data['destination'],
        total_seats=data['total_seats'],
        available_seats=data['total_seats']  # Initially available seats are equal to total seats
    )
    
    db.session.add(new_train)
    db.session.commit()
    
    return jsonify({'message': 'Train added successfully!'}), 201

# Get seat availability between source and destination
@api_blueprint.route('/seats', methods=['GET'])
def get_seat_availability():
    source = request.args.get('source')
    destination = request.args.get('destination')

    if not source or not destination:
        return jsonify({'message': 'Missing source or destination!'}), 400

    trains = Train.query.filter_by(source=source, destination=destination).all()

    if not trains:
        return jsonify({'message': 'No trains found between the given stations!'}), 404

    train_data = [{
        'id': train.id,
        'name': train.name,
        'total_seats': train.total_seats,
        'available_seats': train.available_seats
    } for train in trains]

    return jsonify({'trains': train_data}), 200
