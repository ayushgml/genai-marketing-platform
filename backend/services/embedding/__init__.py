from flask import Blueprint

embedding_bp = Blueprint('embedding', __name__)

from . import service  # noqa: F401 (imported but unused)

