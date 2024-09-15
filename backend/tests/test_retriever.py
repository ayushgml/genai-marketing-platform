import pytest
from flask import Flask, json
from services.retriever.service import retriever_bp
from unittest.mock import patch, MagicMock

# Create a test client for Flask
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(retriever_bp, url_prefix='/retriever')
    client = app.test_client()
    yield client

# Mock the ChromaDB similarity search
@patch('services.retriever.utils.vector_store.similarity_search')
def test_similarity_search_success(mock_similarity_search, client):
    # Mock the ChromaDB results
    mock_similarity_search.return_value = [
        MagicMock(page_content="Mock content 1", metadata={"product_id": "123"}),
        MagicMock(page_content="Mock content 2", metadata={"product_id": "456"})
    ]

    # Create a mock query
    query_data = {
        "query": "Yellow dropper, white bottle",
        "k": 2
    }

    # Send a POST request with the query
    response = client.post('/retriever/search', data=json.dumps(query_data), content_type='application/json')
    assert response.status_code == 200
    assert b"success" in response.data
    results = json.loads(response.data)["results"]
    assert len(results) == 2
    assert results[0]["content"] == "Mock content 1"
    assert results[1]["content"] == "Mock content 2"

# Test the case where query is missing
def test_similarity_search_no_query(client):
    # Send a POST request without query data
    response = client.post('/retriever/search', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400
    assert b"Query is required" in response.data

# Mock a failure in ChromaDB
@patch('services.retriever.utils.vector_store.similarity_search')
def test_similarity_search_failure(mock_similarity_search, client):
    # Simulate an exception being thrown by the ChromaDB client
    mock_similarity_search.side_effect = Exception("ChromaDB error")

    query_data = {
        "query": "Yellow dropper, white bottle",
        "k": 2
    }

    response = client.post('/retriever/search', data=json.dumps(query_data), content_type='application/json')
    assert response.status_code == 500
    assert b"error" in response.data
