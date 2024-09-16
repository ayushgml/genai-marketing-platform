import logging
from flask import jsonify
import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
import os
from services.campaign.utils import get_campaign_from_client, get_campaign_from_client_only

load_dotenv()
AWS_REGION = os.getenv('AWS_REGION')
DYNAMODB_CAMPAIGNS_TABLE_NAME = os.getenv('DYNAMODB_CAMPAIGNS_TABLE_NAME')
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION) 
table = dynamodb.Table(DYNAMODB_CAMPAIGNS_TABLE_NAME) 

def get_all_captions_for_user(client_id):
    """
    Fetch all captions corresponding to every campaign of a given user.

    """
    try:
        campaigns_from_rds = get_campaign_from_client_only(client_id)
        if not campaigns_from_rds:
            return jsonify({"status": "error", "message": "No campaigns found in RDS for the given client_id"}), 404
        
        all_campaigns = []
        # Step 3: Iterate through each campaign_id and fetch the details from DynamoDB
        for campaign in campaigns_from_rds:
            campaign_id = campaign['campaign_id']
            
            # Query DynamoDB using campaign_id
            response = table.get_item(Key={'campaign_id': campaign_id})
            
            if 'Item' in response:
                all_campaigns.append(response['Item'])
            else:
                logging.warning(f"No campaign found in DynamoDB for campaign_id: {campaign_id}")
        
        # Step 4: Return the aggregated list of campaigns
        if all_campaigns:
            return jsonify(all_campaigns), 200
        else:
            return jsonify({"status": "error", "message": "No campaigns found in DynamoDB for the given client_id"}), 404

    except Exception as e:
        logging.error(f"Error fetching campaigns for client_id {client_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

def get_captions_for_product(client_id,product_id):
    """
    Fetch all captions for a specific product (product_id) for a given user.
    """
    try:
        response = table.query(
            KeyConditionExpression = "client_id = :cid AND product_id = :pid",
            ExpressAttributesValues={
                ":cid": client_id,
                ":pid": product_id
            }
        )

        print(response)

        if 'campaign_day' in response and response['campaign_day']:
            return jsonify(response['campaign_day']),200
        else:
            return jsonify({"status": "error", "message": "No captions found for the given product_id"}), 404
        
    except Exception as e:
        logging.error(f"Error fetching captions for product_id {product_id} and client_id {client_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
get_all_captions_for_user(123)
get_captions_for_product(123,123)