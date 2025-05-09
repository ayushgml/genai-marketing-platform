import io
import boto3
import botocore
import base64
import logging
import uuid
from PIL import Image
from boto3.dynamodb.conditions import Key
from concurrent.futures import ThreadPoolExecutor, as_completed
from tiktoken import get_encoding
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import HumanMessage, AIMessage
from langchain_chroma import Chroma
import chromadb
import warnings
from app.config import Config

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Setup logging
logger = logging.getLogger(__name__)

# Initialize clients with configurations
s3 = boto3.client('s3', region_name=Config.AWS_REGION)
dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
table = dynamodb.Table(Config.DYNAMODB_TABLE_NAME)

# Initialize the embedding model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_key=Config.OPENAI_API_KEY
)

# Initialize the ChromaDB client and vector store
chromadb_client = chromadb.HttpClient(
    host=Config.CHROMADB_HOST,
    port=Config.CHROMADB_PORT,
    ssl=False
)
vector_store = Chroma(
    collection_name="insta_posts",
    embedding_function=embedding_model,
    client=chromadb_client
)

# Initialize token encoder
encoder = get_encoding("cl100k_base")

# Utility Functions


def list_product_ids(bucket_name, base_folder):
    """List all product IDs in the specified folder of the S3 bucket."""
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


def update_dynamo_db(product_id, chromadb_id, campaign_id):
    """Link S3 resources and ChromaDB embeddings in DynamoDB."""
    try:
        table.put_item(
            Item={
                'product_id': product_id,
                'chroma_id': chromadb_id,
                'CampaignID': campaign_id
            }
        )
        logger.info(f"DynamoDB updated for product_id {product_id}")
    except Exception as e:
        logger.error(f"Error updating DynamoDB for product_id {product_id}: {e}")


def count_tokens(text):
    """Count the number of tokens in a text."""
    return len(encoder.encode(text))


def truncate_text(text, max_tokens):
    """Truncate the text to a maximum number of tokens."""
    tokens = encoder.encode(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
        text = encoder.decode(tokens)
    return text


def encode_image(image):
    """Encode a PIL image as a base64 string."""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    base64_image = base64.b64encode(buffer.read()).decode("utf-8")
    return base64_image


def extract_image_features(image):
    """Extract image features using Langchain's OpenAI and a base64-encoded image."""
    # Encode the image to base64 format
    base64_image = encode_image(image)
    
    # Initialize the OpenAI client
    llm = ChatOpenAI(
        model="gpt-4o",
        max_tokens=4096,
        openai_api_key=Config.OPENAI_API_KEY
    )
    
    # Create the prompt
    prompt = [
        AIMessage(content=(
            "Generate a list of features separated by commas of the products from this photo. "
            "Generate 10 prominent features from this image about whatever product it focuses on. "
            "Generate just a paragraph of words separated by commas. "
            "The features should not contain names of any brand or product. It can contain chemical names, "
            "colour, other visually identifiable features."
        )),
        HumanMessage(content=[
            {"type": "text", "text": "Describe the contents of this image."},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"
                },
            },
        ])
    ]

    try:
        # Send the prompt to the model
        response = llm(prompt)
        image_description = response.content.strip()
        return image_description

    except Exception as e:
        logger.error(f"Error in generating image features: {e}")
        return "Error in generating image features"


def process_product(product_id):
    """Process a single product ID: fetch data, generate embeddings, and update databases."""
    logger.info(f"Processing product_id {product_id}")
    image_key = f"{Config.S3_BASE_FOLDER}{product_id}/image.png"
    description_key = f"{Config.S3_BASE_FOLDER}{product_id}/description.txt"

    # Load image
    image_data = get_s3_file(Config.S3_BUCKET_NAME, image_key)

    if not image_data:
        logger.warning(f"Skipping product_id {product_id} due to missing image.")
        return False

    try:
        image = Image.open(io.BytesIO(image_data))
    except Exception as e:
        logger.error(f"Error opening image for product_id {product_id}: {e}")
        return False

    # Load description
    description_data = get_s3_file(Config.S3_BUCKET_NAME, description_key)

    if not description_data:
        logger.warning(f"Skipping product_id {product_id} due to missing description.")
        return False

    description_text = description_data.decode('utf-8')

    # Extract image features
    image_features = extract_image_features(image)

    # Concatenate features with the description
    combined_text = f"Features: {image_features}\nDescription: {description_text}"

    # Store embeddings in ChromaDB
    try:
        metadata = {
            "source": "insta_posts",
            "product_id": product_id,
            "image_s3_path": f"s3://{Config.S3_BUCKET_NAME}/{image_key}",
            "description_s3_path": f"s3://{Config.S3_BUCKET_NAME}/{description_key}"
        }
    
        # Add embeddings to ChromaDB
        vector_store.add_texts(
            [combined_text],
            metadatas=[metadata],
            ids=[str(product_id)]
        )
        logger.info(f"Embeddings added to ChromaDB for product_id {product_id}")
    except Exception as e:
        logger.error(f"Error adding embeddings to ChromaDB for product_id {product_id}: {e}")
        return False
    
    # Generate a unique CampaignID
    campaign_id = str(uuid.uuid4())
    
    # Update DynamoDB
    try:
        update_dynamo_db(product_id, str(product_id), campaign_id)
    except Exception as e:
        logger.error(f"Error updating DynamoDB for product_id {product_id}: {e}")
        return False

    return True


def process_all_products():
    """Process all products by listing product IDs and processing each one."""
    product_ids = list_product_ids(Config.S3_BUCKET_NAME, Config.S3_BASE_FOLDER)
    if not product_ids:
        logger.error("No product IDs found. Exiting.")
        return
    # Use ThreadPoolExecutor for concurrency
    with ThreadPoolExecutor(max_workers=Config.MAX_THREADS) as executor:
        futures = {executor.submit(process_product, pid): pid for pid in product_ids}
        for future in as_completed(futures):
            pid = futures[future]
            try:
                result = future.result()
                if not result:
                    logger.error(f"Processing failed for product_id {pid}")
            except Exception as e:
                logger.error(f"Unhandled exception processing product_id {pid}: {e}")
