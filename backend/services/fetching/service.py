# import logging
# from flask import jsonify, Blueprint
# from .utils import fetch_image_and_description

# fetch_bp = Blueprint('fetch', __name__)

# @fetch_bp.route('image/<product_id>', methods=['GET'])
# def fetch_image_and_description_route(product_id):
#     try:
#         response, status_code = fetch_image_and_description(product_id)
        
#         return jsonify(response), status_code
        
#     except Exception as e:
#         logging.error(f"Error fetching image and description for {product_id}: {str(e)}")
#         return jsonify({"status": "error", "message": str(e)}), 500

import logging
from flask import jsonify, Blueprint
from .utils import fetch_image_and_description
from . import fetch_bp

# fetch_bp = Blueprint('fetching', __name__)

@fetch_bp.route('/image/<product_id>', methods=['GET'])
def fetch_image_and_description_route(product_id):
    try:
        response, status_code = fetch_image_and_description(product_id)
        return jsonify(response), status_code
    except Exception as e:
        logging.error(f"Error fetching image and description for {product_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
