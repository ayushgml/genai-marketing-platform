from flask import Blueprint

fetch_bp = Blueprint('fetching', __name__)

from . import service
