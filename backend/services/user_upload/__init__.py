from flask import Blueprint

# Define the blueprint
user_upload_bp = Blueprint('user_upload_bp', __name__)

# Import the service to register routes
from . import service
