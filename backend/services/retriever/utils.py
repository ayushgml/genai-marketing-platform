import logging
from langchain.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb
from app.config import Config

# Initialize logging
logger = logging.getLogger(__name__)

# Initialize the embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=Config.OPENAI_API_KEY)

# Initialize the ChromaDB client and vector store
chromadb_client = chromadb.HttpClient(
    host=Config.CHROMADB_HOST,
    port=Config.CHROMADB_PORT,
    ssl=False
)
vector_store = Chroma(
    collection_name="insta_posts",  # Make sure this matches your collection name
    embedding_function=embedding_model,
    client=chromadb_client
)

def perform_similarity_search(query, k=2):
    """Perform a similarity search on the vector store based on a text query."""
    try:
        # Perform the similarity search
        results = vector_store.similarity_search(
            query=query,
            k=k,
            filter={"source": "insta_posts"}  # Filter by source, modify as needed
        )
        
        formatted_results = []
        for res in results:
            formatted_results.append({
                "content": res.page_content,
                "metadata": res.metadata
            })
        return formatted_results

    except Exception as e:
        logger.error(f"Error during similarity search: {e}")
        raise e
