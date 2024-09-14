import os
import boto3
import botocore
from langchain import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from PIL import Image
import io
import json
import logging
from dotenv import load_dotenv
from boto3.dynamodb.conditions import Key
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables from ../../.env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

# Configuration from .env
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_BASE_FOLDER = os.getenv('S3_BASE_FOLDER')
CHROMADB_HOST = os.getenv('CHROMADB_HOST')
CHROMADB_PORT = os.getenv('CHROMADB_PORT')
DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MAX_THREADS = int(os.getenv('MAX_THREADS', '5'))  # Default to 5 if not set

# Optional RDS configuration
RDS_DBNAME = os.getenv('RDS_DBNAME')
RDS_USER = os.getenv('RDS_USER')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')
RDS_HOST = os.getenv('RDS_HOST')

# Initialize clients with configurations
s3 = boto3.client('s3', region_name=AWS_REGION)
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Functions
def list_product_ids(bucket_name, base_folder):
    """List all product IDs in the insta_posts folder of the S3 bucket."""
    paginator = s3.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': bucket_name, 'Prefix': base_folder, 'Delimiter': '/'}
    product_ids = set()

    for page in paginator.paginate(**operation_parameters):
        prefixes = page.get('CommonPrefixes', [])
        for prefix in prefixes:
            prefix_path = prefix.get('Prefix')
            product_id = prefix_path[len(base_folder):-1]  # Extract product_id from prefix
            product_ids.add(product_id)
    logger.info(f"Found {len(product_ids)} product IDs.")
    return list(product_ids)

def get_s3_file(bucket_name, file_key):
    """Fetch a file from S3."""
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        return response['Body'].read()
    except botocore.exceptions.ClientError as e:
        logger.error(f"Error fetching {file_key} from S3: {e}")
        return None

def update_dynamo_db(product_id, chromadb_id):
    """Link S3 resources and ChromaDB embeddings in DynamoDB."""
    try:
        table.put_item(
            Item={
                'product_id': product_id,
                'chroma_id': chromadb_id
            }
        )
        logger.info(f"DynamoDB updated for product_id {product_id}")
    except Exception as e:
        logger.error(f"Error updating DynamoDB for product_id {product_id}: {e}")

def extract_image_features(image):
    """Extract image features using GPT-4."""
    
    
    
    
    image_description = "Placeholder image features"
    return image_description

def process_product(product_id):
    """Process a single product ID: fetch data, generate embeddings, and update databases."""
    logger.info(f"Processing product_id {product_id}")
    image_key = f"{S3_BASE_FOLDER}{product_id}/image.png"
    description_key = f"{S3_BASE_FOLDER}{product_id}/description.txt"

    # Load image
    image_data = get_s3_file(S3_BUCKET_NAME, image_key)
    if not image_data:
        logger.warning(f"Skipping product_id {product_id} due to missing image.")
        return

    try:
        image = Image.open(io.BytesIO(image_data))
    except Exception as e:
        logger.error(f"Error opening image for product_id {product_id}: {e}")
        return

    # Load description
    description_data = get_s3_file(S3_BUCKET_NAME, description_key)
    if not description_data:
        logger.warning(f"Skipping product_id {product_id} due to missing description.")
        return

    description_text = description_data.decode('utf-8')

    # Extract image features
    image_features = extract_image_features(image)

    # Concatenate features with the description
    combined_text = f"Features: {image_features}\nDescription: {description_text}"

    # Generate embeddings
    try:
        embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)
        embeddings = embedding_model.embed(combined_text)
    except Exception as e:
        logger.error(f"Error generating embeddings for product_id {product_id}: {e}")
        return

    # Store embeddings in ChromaDB
    try:
        vector_store = Chroma(
            collection_name="insta_posts",
            embedding_function=embedding_model,
            host=CHROMADB_HOST,
            port=int(CHROMADB_PORT)
        )

        metadata = {
            "product_id": product_id,
            "image_s3_path": f"s3://{S3_BUCKET_NAME}/{image_key}",
            "description_s3_path": f"s3://{S3_BUCKET_NAME}/{description_key}"
        }

        vector_store.add_texts([combined_text], metadatas=[metadata], ids=[product_id])
        chromadb_id = product_id  # Assuming the ID used is the product_id
        logger.info(f"Embeddings added to ChromaDB for product_id {product_id}")
    except Exception as e:
        logger.error(f"Error adding embeddings to ChromaDB for product_id {product_id}: {e}")
        return

    # Update DynamoDB
    update_dynamo_db(product_id, chromadb_id)

def main():
    product_ids = list_product_ids(S3_BUCKET_NAME, S3_BASE_FOLDER)
    if not product_ids:
        logger.error("No product IDs found. Exiting.")
        return

    # Use ThreadPoolExecutor for concurrency
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(process_product, pid): pid for pid in product_ids}
        for future in as_completed(futures):
            pid = futures[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f"Unhandled exception processing product_id {pid}: {e}")

if __name__ == "__main__":
    main()
