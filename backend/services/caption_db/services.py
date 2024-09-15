import logging
from flask import jsonify
import boto3
from . import caption_db_bp
from services.captioning.service import generate_marketing_captions

dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
table = dynamodb.Table('campaign_storage') 

@caption_db_bp.route('/generate-captions/<client_id>/<product_id>', methods=['GET'])
def generate_captions(client_id, product_id):
    """Endpoint to generate and store captions in DynamoDB."""
    try:
        result = generate_marketing_captions(client_id, product_id)
        
        if result:
            store_captions_in_dynamodb(result)
            return jsonify(result), 200
        else:
            return jsonify({"status": "error", "message": "Caption generation failed"}), 500
    except Exception as e:
        logging.error(f"Error generating captions for client_id {client_id} and product_id {product_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
def generate_campaign_id(client_id, product_id):
    """Generate a unique campaign_id based on client_id and product_id."""
    return f"{client_id}_{product_id}"

def store_captions_in_dynamodb(campaign_data):
    """Stores the generated captions in DynamoDB."""
    try:
        campaign_id = generate_campaign_id(campaign_data['client_id'], campaign_data['product_id'])
        
        campaign_data['campaign_id'] = campaign_id

        table.put_item(Item=campaign_data)

        logging.info(f"Campaign data stored successfully for campaign_id {campaign_id}")
    except Exception as e:
        logging.error(f"Error storing campaign data in DynamoDB: {str(e)}")

@captioning_bp.route('/get-campaign/<campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    """Endpoint to retrieve captions from DynamoDB by campaign ID."""
    try:
        response = table.get_item(Key={'campaign_id': campaign_id})
        
        if 'Item' in response:
            return jsonify(response['Item']), 200
        else:
            return jsonify({"status": "error", "message": "Campaign not found"}), 404
    except Exception as e:
        logging.error(f"Error retrieving campaign {campaign_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
