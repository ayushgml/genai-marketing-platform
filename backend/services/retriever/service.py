import logging
from flask import request, jsonify
from . import retriever_bp
from .utils import perform_similarity_search

@retriever_bp.route('/search', methods=['POST'])
def similarity_search():
    data = request.get_json()
    query = data.get('query')
    k = data.get('k', 2)
    
    if not query:
        return jsonify({"status": "error", "message": "Query is required"}), 400
    
    try:
        results = perform_similarity_search(query, k)
        return jsonify({"status": "success", "results": results}), 200
    except Exception as e:
        logging.error(f"Error during similarity search: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
