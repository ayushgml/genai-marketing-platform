import os
import io
import boto3
import botocore
import base64
from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.messages import HumanMessage, AIMessage
from PIL import Image
import io
import logging
from dotenv import load_dotenv
from boto3.dynamodb.conditions import Key
from concurrent.futures import ThreadPoolExecutor, as_completed
import tiktoken
import logging
from langchain_chroma import Chroma
import uuid
import chromadb
import warnings

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load environment variables from .env file
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

# Initialize the embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)

# Initialize the Chroma client and vector store
client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT, ssl=False)
vector_store = Chroma(
    collection_name="insta_posts",  # Make sure this matches your collection name
    embedding_function=embedding_model,
    client=client
)

# Example: Perform similarity search on a given query
def perform_similarity_search(query, k=2):
    """Perform a similarity search on the vector store."""
    try:
        results = vector_store.similarity_search(
            query,  # Text query for the similarity search
            k=k,    # Number of similar results to return
            filter={"source": "insta_posts"}  # Optional filter (modify as needed)
        )
        
        # Display the results
        for res in results:
            print(f"* {res.page_content} [{res.metadata}]")
            
    except Exception as e:
        logger.error(f"Error during similarity search: {e}")

# Example usage
query = "Yellow dropper, white bottle, pastel pink cap, light green container, cream texture, exfoliating treatment, polypeptide formula, lightweight oil, glycolic acid, daily sunscreen, hydrating cream, smooth texture, AHA blend, moisturizing formula, translucent liquid."
perform_similarity_search(query, k=2)
