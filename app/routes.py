from flask import Blueprint, request, jsonify, g
from .auth import register, login
from .models import User, Train, db
import jwt
from functools import wraps
from flask import current_app

api_blueprint = Blueprint('api', __name__)

# Middleware to check JWT token for protected routes
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'], options={"verify_exp": False})
            print("Decoded token:", decoded_token)
            token = request.headers.get('Authorization')
            print("Received token:", token)

            user = User.query.get(decoded_token['user_id'])
            g.user = {'id': user.id, 'username': user.username, 'role': user.role}
        except Exception as e:
            return jsonify({'message': 'Token is invalid or expired!'}), 401
        
        return f(*args, **kwargs)
    
    return decorator

# Registering routes
@api_blueprint.route('/', methods=['GET'])
def home():
    return {"message": "Railway Management API is running!"}

# User registration route
@api_blueprint.route('/register', methods=['POST'])
def register_user():
    return register()

# User login route
@api_blueprint.route('/login', methods=['POST'])
def login_user():
    return login()

# Admin route to add a new train
@api_blueprint.route('/train', methods=['POST'])
@token_required
def add_train():
    if g.user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized!'}), 403
    
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

# Function to register the booking routes
def register_booking_routes(api_blueprint):
    from .booking import book_seat, get_booking_details

    @api_blueprint.route('/book', methods=['POST'])
    @token_required
    def book_seat_route():
        return book_seat()

    @api_blueprint.route('/booking/<int:booking_id>', methods=['GET'])
    @token_required
    def get_booking_route(booking_id):
        return get_booking_details(booking_id)

