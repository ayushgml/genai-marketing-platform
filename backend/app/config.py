import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AWS_REGION = os.getenv('AWS_REGION')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    S3_BASE_FOLDER = os.getenv('S3_BASE_FOLDER')
    CHROMADB_HOST = os.getenv('CHROMADB_HOST')
    CHROMADB_PORT = os.getenv('CHROMADB_PORT')
    DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MAX_THREADS = int(os.getenv('MAX_THREADS', '5'))
