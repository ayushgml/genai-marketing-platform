import logging
from flask import jsonify
import boto3
from . import caption_db_bp
from app.config import Config
from services.captioning.service import generate_marketing_captions
from services.campaign.utils import get_campaign_from_client, get_campaign_from_client_only
import json

dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION) 
table = dynamodb.Table(Config.DYNAMODB_CAMPAIGNS_TABLE_NAME) 

@caption_db_bp.route('/generate-captions/<client_id>/<product_id>', methods=['GET'])
def generate_captions(client_id, product_id):
    """Endpoint to generate and store captions in DynamoDB."""
    try:
        result = generate_marketing_captions(client_id, product_id)
        if result:
            store_captions_in_dynamodb(result)
            return jsonify(result), 200
        else:
            return jsonisfy({"status": "error", "message": "Caption generation failed"}), 500
    except Exception as e:
        logging.error(f"Error generating captions for client_id {client_id} and product_id {product_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
def get_campaign_id(client_id, product_id):
    """Generate a unique campaign_id based on client_id and product_id."""
    campaign_id = get_campaign_from_client(client_id, product_id)['campaign_id']
    client_id = get_campaign_from_client(client_id, product_id)['client_id']
    product_id = get_campaign_from_client(client_id, product_id)['client_id']
    return campaign_id,client_id,product_id

def store_captions_in_dynamodb(campaign_data):
    """Stores the generated captions in DynamoDB."""
    try:
        campaign_id,client_id,product_id = get_campaign_id(campaign_data['client_id'], campaign_data['product_id'])
        campaign_data['campaign_id'] = campaign_id
        # campaign_data['client_id'] = client_id
        # campaign_data['product_id'] = product_id

        table.put_item(Item=campaign_data)

        logging.info(f"Campaign data stored successfully for campaign_id {campaign_id}")
    except Exception as e:
        logging.error(f"Error storing campaign data in DynamoDB: {str(e)}")

@caption_db_bp.route('/get-campaign/<campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    """Endpoint to retrieve captions from DynamoDB by campaign ID."""
    try:
        # response = table.get_item(Key={"campaign_id": campaign_id})
        response = table.query(
        KeyConditionExpression = "campaign_id = :cid",
        ExpressionAttributeValues={
            ":cid": campaign_id
        }
        )
        if 'Items' in response:
            return jsonify(response['Items']), 200
        else:
            return jsonify({"status": "error", "message": "Campaign not found"}), 404
    except Exception as e:
        logging.error(f"Error retrieving campaign {campaign_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@caption_db_bp.route('/get-captions/<client_id>',methods=['GET'])    
def get_all_captions_for_user(client_id):
    """
    Fetch all captions corresponding to every campaign of a given user.

    """
    try:
        campaigns_from_rds = get_campaign_from_client_only(client_id)
        # print("Ayush")
        # print(campaigns_from_rds)
        if not campaigns_from_rds:
            return jsonify({"status": "error", "message": "No campaigns found in RDS for the given client_id"}), 404
        
        all_campaigns = []
        # Step 3: Iterate through each campaign_id and fetch the details from DynamoDB
        for campaign in campaigns_from_rds:
            campaign_id = campaign['campaign_id']
            print(campaign_id)
            # Query DynamoDB using campaign_id
            # response = table.get_item(Key={"campaign_id": campaign_id})
            response = table.query(
            KeyConditionExpression = "campaign_id = :cid",
            ExpressionAttributeValues={
                ":cid": campaign_id
            }
        )
            # Iterating through all objects in `campaign_day`
            for item in response['Items']:
                campaign_days = item.get('campaign_day', [])
                
                for day in campaign_days:
                    hashtags_json = json.loads(day['hashtags'])  # Convert hashtags JSON string to Python dict
                    print(f"Day: {day['day']}")
                    print(f"Caption: {hashtags_json['caption']}")
                    print(f"Hashtags: {hashtags_json['hashtags']}")
                    print() 
                    all_campaigns.append(hashtags_json)
            
        if all_campaigns:
            return jsonify(all_campaigns), 200
        else:
            return jsonify({"status": "error", "message": "No campaigns found in DynamoDB for the given client_id"}), 404

    except Exception as e:
        logging.error(f"Error fetching campaigns for client_id {client_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@caption_db_bp.route('/get-captions/<client_id>/<product_id>',methods=['GET'])
def get_captions_for_user(client_id,product_id):
    """
    Fetch all captions corresponding to every campaign of a given user.

    """
    try:
        campaign = get_campaign_from_client(client_id,product_id)
        # print("Ayush")
        # print(campaigns_from_rds)
        if not campaign:
            return jsonify({"status": "error", "message": "No campaigns found in RDS for the given client_id"}), 404
        
        all_campaigns = []
        # Step 3: Iterate through each campaign_id and fetch the details from DynamoDB
        campaign_id = campaign['campaign_id']
        print(campaign_id)
        # Query DynamoDB using campaign_id
        # response = table.get_item(Key={"campaign_id": campaign_id})
        response = table.query(
        KeyConditionExpression = "campaign_id = :cid",
        ExpressionAttributeValues={
            ":cid": campaign_id
        }
    )
        # Iterating through all objects in `campaign_day`
        for item in response['Items']:
            campaign_days = item.get('campaign_day', [])
            
            for day in campaign_days:
                hashtags_json = json.loads(day['hashtags'])  # Convert hashtags JSON string to Python dict
                print(f"Day: {day['day']}")
                print(f"Caption: {hashtags_json['caption']}")
                print(f"Hashtags: {hashtags_json['hashtags']}")
                print() 
                all_campaigns.append(hashtags_json)
            
        if all_campaigns:
            return jsonify(all_campaigns), 200
        else:
            return jsonify({"status": "error", "message": "No campaigns found in DynamoDB for the given client_id"}), 404

    except Exception as e:
        logging.error(f"Error fetching campaigns for client_id {client_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


# @caption_db_bp.route('/get-captions/<client_id>/<product_id>',methods=['GET'])
# def get_captions_for_product(client_id,product_id):
#     """
#     Fetch all captions for a specific product (product_id) for a given user.
#     """
#     try:
#         response = table.query(
#             KeyConditionExpression = "client_id = :cid AND product_id = :pid",
#             ExpressAttributesValues={
#                 ":cid": client_id,
#                 ":pid": product_id
#             }
#         )

#         if 'campaign_day' in response and response['campaign_day']:
#             return jsonify(response['campaign_day']),200
#         else:
#             return jsonify({"status": "error", "message": "No captions found for the given product_id"}), 404
        
#     except Exception as e:
#         logging.error(f"Error fetching captions for product_id {product_id} and client_id {client_id}: {str(e)}")
#         return jsonify({"status": "error", "message": str(e)}), 500
    

        
