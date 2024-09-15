import logging
from flask import jsonify, request
from . import campaign_bp
from .utils import insert_record_into_db


@campaign_bp.route('/generate-campaign/<client_id>/<product_id>', methods=['GET', 'POST'])
def generate_campaign(client_id, product_id):
    try:
        result = insert_record_into_db(request.json, client_id, product_id)
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"status": "error", "message": "Campaign generation failed"}), 500
    except Exception as e:
        logging.error(f"Error generating campaign for client_id {client_id} and product_id {product_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
