import os
import logging
import boto3
from flask import request
from dotenv import load_dotenv

load_dotenv()

class Config:
    AWS_REGION = os.getenv('AWS_REGION')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    S3_BASE_FOLDER = os.getenv('S3_BASE_FOLDER')

# Initialize S3 client
s3 = boto3.client('s3', region_name=Config.AWS_REGION)


def upload_file_to_s3(file, bucket_name, key):
    """Upload a file to S3."""
    try:
        s3.upload_fileobj(file, bucket_name, key)
        return True
    except Exception as e:
        logging.error(f"Error uploading file to S3: {e}")
        return False


def construct_s3_key(product_id, file_type, extension=''):
    """Construct the S3 key for a given product ID, file type, and extension."""
    return f"{Config.S3_BASE_FOLDER}{product_id}/{file_type}{extension}"


def handle_upload_files(product_id):
    """Handle the uploading of a description file and an image file."""
    description_file = request.files.get('description')
    image_file = request.files.get('image')

    if not description_file or not image_file:
        return {"status": "error", "message": "Missing description file or image file"}, 400

    description_key = construct_s3_key(product_id, 'description', '.txt')
    image_key = construct_s3_key(product_id, 'image', '.jpg')  # Change the extension if needed

    description_uploaded = upload_file_to_s3(description_file, Config.S3_BUCKET_NAME, description_key)
    image_uploaded = upload_file_to_s3(image_file, Config.S3_BUCKET_NAME, image_key)

    if description_uploaded and image_uploaded:
        return {"status": "success", "message": "Files uploaded successfully"}, 200
    else:
        return {"status": "error", "message": "Error uploading files"}, 500
