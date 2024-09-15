from flask import Blueprint

campaign_bp = Blueprint('campaign', __name__)

from . import service
