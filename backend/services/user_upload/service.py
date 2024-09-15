import logging
from flask import Blueprint, jsonify
from .utils import handle_user_file_upload
from . import user_upload_bp

# Define the route for uploading files
@user_upload_bp.route('/upload/<user_id>', methods=['POST'])
def upload_user_files(user_id):
    """Route for uploading a description file and an image file."""
    try:
        response, status_code = handle_user_file_upload(user_id)
        return jsonify(response), status_code
    except Exception as e:
        logging.error(f"Error uploading files for user_id {user_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
