from flask import Flask
from .config import Config
from services.embedding import embedding_bp
from services.retriever import retriever_bp
from services.captioning import captioning_bp
from services.fetching import fetch_bp
from services.caption_db import caption_db_bp
from services.campaign import campaign_bp
from services.user_upload import user_upload_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(embedding_bp, url_prefix='/embedding')
    app.register_blueprint(retriever_bp, url_prefix='/retriever')
    app.register_blueprint(captioning_bp, url_prefix='/captioning')
    app.register_blueprint(caption_db_bp, url_prefix = '/caption_db')
    app.register_blueprint(fetch_bp, url_prefix='/fetching')
    app.register_blueprint(campaign_bp, url_prefix='/campaign')
    app.register_blueprint(user_upload_bp, url_prefix='/user_upload')

    return app

