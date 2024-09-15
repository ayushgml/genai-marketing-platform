import logging
from flask import jsonify
from . import embedding_bp
from .utils import process_product, process_all_products

@embedding_bp.route('/process/<product_id>', methods=['GET'])
def process_embedding(product_id):
    try:
        result = process_product(product_id)
        if result:
            return jsonify({"status": "success", "product_id": product_id}), 200
        else:
            return jsonify({"status": "error", "message": "Processing failed"}), 500
    except Exception as e:
        logging.error(f"Error processing embedding for {product_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@embedding_bp.route('/process_all', methods=['GET'])
def process_all_embeddings():
    try:
        process_all_products()
        return jsonify({"status": "success", "message": "All products processed"}), 200
    except Exception as e:
        logging.error(f"Error processing all embeddings: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
