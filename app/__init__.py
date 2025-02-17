from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .db import db
from .models import User, Train, Booking  
import os
from .models import db
from .routes import api_blueprint, register_booking_routes
from config import Config  

from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    db.init_app(app)
    
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    
    return app


