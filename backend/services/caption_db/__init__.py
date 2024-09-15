from flask import Blueprint

captioning_bp = Blueprint('caption_db', __name__)

from . import service