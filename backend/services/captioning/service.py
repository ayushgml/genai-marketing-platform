import logging
from flask import jsonify
from . import captioning_bp
from .utils import generate_marketing_captions

@captioning_bp.route('/generate-captions/<client_id>/<product_id>', methods=['GET'])
def generate_captions(client_id, product_id):
    try:
        result = generate_marketing_captions(client_id, product_id)
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"status": "error", "message": "Caption generation failed"}), 500
    except Exception as e:
        logging.error(f"Error generating captions for client_id {client_id} and product_id {product_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
