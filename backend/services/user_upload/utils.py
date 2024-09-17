import os
import logging
import boto3
import uuid
from flask import request
from app.config import Config


s3 = boto3.client('s3', region_name=Config.AWS_REGION)

def upload_file_to_s3(file, bucket_name, key):
    """Upload a file to S3."""
    try:
        s3.upload_fileobj(file, bucket_name, key)
        return True
    except Exception as e:
        logging.error(f"Error uploading file to S3: {e}")
        return False

def construct_s3_key(user_id, product_id, file_type, extension):
    """Construct the S3 key for a given user ID, product ID, file type, and extension."""
    return f"{Config.S3_BASE_UPLOAD_FOLDER}{user_id}/{product_id}/{file_type}{extension}"

def handle_user_file_upload(user_id):
    """Handle the uploading of a description file and an image file."""
    # Generate a unique product_id using UUID
    product_id = str(uuid.uuid4())
    print(request)
    description_file = request.files.get('description')
    image_file = request.files.get('image')

    if not description_file or not image_file:
        return {"status": "error", "message": "Missing description file or image file"}, 400

    # Get the extension of the image file dynamically based on the uploaded file
    image_extension = os.path.splitext(image_file.filename)[1]  # e.g., '.jpg' or '.png'
    description_extension = '.txt'

    # Construct the S3 keys with user_id, product_id, and appropriate file types/extensions
    description_key = construct_s3_key(user_id, product_id, 'description', description_extension)
    image_key = construct_s3_key(user_id, product_id, 'image', image_extension)

    # Upload files to S3
    description_uploaded = upload_file_to_s3(description_file, Config.S3_BUCKET_NAME, description_key)
    image_uploaded = upload_file_to_s3(image_file, Config.S3_BUCKET_NAME, image_key)

    if description_uploaded and image_uploaded:
        return {"status": "success", "message": "Files uploaded successfully", "product_id": product_id}, 200
    else:
        return {"status": "error", "message": "Error uploading files"}, 500
