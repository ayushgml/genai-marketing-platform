from flask import Blueprint

caption_db_bp = Blueprint('caption_db', __name__)

from . import service