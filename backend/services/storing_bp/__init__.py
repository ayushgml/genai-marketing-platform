from flask import Blueprint

storing_bp = Blueprint('storing_bp', __name__)

from . import service 
