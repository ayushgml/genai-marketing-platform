from flask import Blueprint

retriever_bp = Blueprint('retriever', __name__)

from . import service  # noqa: F401 (imported but unused)

