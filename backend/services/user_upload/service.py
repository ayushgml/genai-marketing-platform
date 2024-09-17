import logging
from flask import Blueprint, jsonify, make_response
from .utils import handle_user_file_upload
from . import user_upload_bp

# Define the route for uploading files
@user_upload_bp.route('/upload/<user_id>', methods=['POST'])
def upload_user_files(user_id):
    """Route for uploading a description file and an image file."""
    try:

        response, status_code = handle_user_file_upload(user_id)
        res = make_response(jsonify(response))
        res.headers['Access-Control-Allow-Origin']="*"
        print(res)
        return res
    except Exception as e:
        logging.error(f"Error uploading files for user_id {user_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
