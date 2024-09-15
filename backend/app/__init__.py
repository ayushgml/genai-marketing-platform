from flask import Flask
from .config import Config
from services.embedding import embedding_bp
from services.retriever import retriever_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(embedding_bp, url_prefix='/embedding')
    app.register_blueprint(retriever_bp, url_prefix='/retriever')

    return app
