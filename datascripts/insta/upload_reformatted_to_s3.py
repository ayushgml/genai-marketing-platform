import json
import requests
import boto3
import os

# Initialize the S3 client
s3 = boto3.client('s3')

# S3 bucket name and base folder path
bucket_name = 'genai-incredibles-aeh-767397765800'
base_folder = 'insta_posts/'

# Function to upload image and description to S3
def upload_image_and_description_to_s3(product_id, image_url, description):
    # Create folder structure in the bucket for this product_id
    folder_path = f"{base_folder}{product_id}/"

    # Fetch the image from the image_url
    try:
        image_response = requests.get(image_url, stream=True)
        if image_response.status_code != 200:
            print(f"Image for product_id {product_id} is not fetchable from URL: {image_url}")
            return  # Skip to the next product if the image is not available
        print(f"Image fetched successfully from {image_url}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the image for product_id {product_id}: {e}")
        return

    # Create the image filename
    image_filename = folder_path + 'image.png'

    # Upload the image to S3
    try:
        s3.upload_fileobj(image_response.raw, bucket_name, image_filename, ExtraArgs={'ContentType': 'image/png'})
        print(f"Image uploaded successfully to S3: {bucket_name}/{image_filename}")
    except Exception as e:
        print(f"Error uploading image for product_id {product_id} to S3: {e}")
        return

    # Create the description filename and save the description as a text file in S3
    description_filename = folder_path + 'description.txt'
    
    try:
        # Convert the description to bytes and upload
        s3.put_object(Bucket=bucket_name, Key=description_filename, Body=description.encode('utf-8'), ContentType='text/plain')
        print(f"Description uploaded successfully to S3: {bucket_name}/{description_filename}")
    except Exception as e:
        print(f"Error uploading description for product_id {product_id} to S3: {e}")
        return

# Function to process the JSON file and loop through each post
def process_json_and_upload(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            posts_data = json.load(f)
        print(f"Data successfully loaded from {json_file}")
    except FileNotFoundError:
        print(f"Error: {json_file} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file}.")
        return

    # Loop through each post in the JSON file
    for post in posts_data:
        product_id = post.get('post id')
        if product_id > 435:
            image_url = post.get('image_url')
            description = post.get('description', '')

            # Upload image and description to S3
            upload_image_and_description_to_s3(product_id, image_url, description)

# Example usage
json_file = 'reformatted_posts.json'  # Replace with the actual JSON file path
process_json_and_upload(json_file)
