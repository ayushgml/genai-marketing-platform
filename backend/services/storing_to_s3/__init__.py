from flask import Blueprint

storing_bp = Blueprint('storing_to_s3', __name__)

from . import service 
