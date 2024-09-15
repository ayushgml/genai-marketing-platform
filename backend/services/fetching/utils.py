import io
import boto3
import logging
import base64
from app.config import Config

# Setup logging
logger = logging.getLogger(__name__)

# Initialize S3 client
s3 = boto3.client('s3', region_name=Config.AWS_REGION)

def get_s3_file(bucket_name, file_key):
    """Fetch a file from S3."""
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        return response['Body'].read()
    except boto3.exceptions.S3UploadFailedError as e:
        logger.error(f"Error fetching {file_key} from S3: {e}")
        return None

def encode_image(image_data):
    """Encode image data as a base64 string."""
    return base64.b64encode(image_data).decode('utf-8')

def construct_s3_key(product_id, file_type):
    """Construct the S3 key for a given product ID and file type."""
    return f"{Config.S3_BASE_FOLDER}{product_id}/{file_type}"

def fetch_image_and_description(product_id):
    """Fetch image and description from S3 and prepare the response."""
    try:
        image_key = construct_s3_key(product_id, 'image.png')
        description_key = construct_s3_key(product_id, 'description.txt')

        image_data = get_s3_file(Config.S3_BUCKET_NAME, image_key)
        description_data = get_s3_file(Config.S3_BUCKET_NAME, description_key)

        if image_data and description_data:
            response = {
                "description": description_data.decode('utf-8'),
                "image": encode_image(image_data)
            }
            return response, 200
        else:
            return {"status": "error", "message": "Image or description not found"}, 404

    except Exception as e:
        logger.error(f"Error fetching image and description for {product_id}: {str(e)}")
        return {"status": "error", "message": str(e)}, 500
