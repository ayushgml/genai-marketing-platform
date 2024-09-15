from flask import Blueprint

captioning_bp = Blueprint('captioning', __name__)

from . import service
