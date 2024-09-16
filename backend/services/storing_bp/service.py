import logging
from flask import Blueprint, jsonify
from .utils import handle_upload_files
from . import storing_bp

@storing_bp.route('/upload/<product_id>', methods=['POST'])
def upload_files_route(product_id):
    """Route for uploading a description file and an image file."""
    try:
        response, status_code = handle_upload_files(product_id)
        return jsonify(response), status_code
    except Exception as e:
        logging.error(f"Error uploading files for product_id {product_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
