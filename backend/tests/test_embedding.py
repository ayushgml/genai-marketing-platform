import pytest
from flask import Flask
from services.embedding.service import embedding_bp
from unittest.mock import patch, MagicMock

# Create a test client for Flask
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(embedding_bp, url_prefix='/embedding')
    client = app.test_client()
    yield client

# Mock the S3 and ChromaDB interactions
@patch('services.embedding.utils.get_s3_file')
@patch('services.embedding.utils.Image.open')
@patch('services.embedding.utils.vector_store.add_texts')
@patch('services.embedding.utils.update_dynamo_db')
def test_process_embedding_success(mock_dynamo, mock_add_texts, mock_image_open, mock_get_s3_file, client):
    # Mocking S3 image and description fetching
    mock_get_s3_file.side_effect = [
        b'test_image_data',   # Mock image
        b'test_description'   # Mock description
    ]

    mock_image_open.return_value = MagicMock()  # Mock the PIL Image.open behavior

    # Mocking successful ChromaDB and DynamoDB operations
    mock_add_texts.return_value = None
    mock_dynamo.return_value = None

    # Send a GET request to process a specific product_id
    response = client.get('/embedding/process/12345')
    
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.data}")
    
    assert response.status_code == 200
    assert b"success" in response.data


# Mocking the failure case when S3 returns no image or description
@patch('services.embedding.utils.get_s3_file')
def test_process_embedding_failure(mock_get_s3_file, client):
    # Mocking empty S3 image fetch (None return)
    mock_get_s3_file.return_value = None

    response = client.get('/embedding/process/12345')
    assert response.status_code == 500
    assert b"error" in response.data
