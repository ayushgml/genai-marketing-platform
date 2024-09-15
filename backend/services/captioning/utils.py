import io
import boto3
import logging
from PIL import Image
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
from app.config import Config
from services.retriever.utils import perform_similarity_search
from services.embedding.utils import extract_image_features, get_s3_file
from services.campaign.utils import get_campaign_from_client

# Initialize logging
logger = logging.getLogger(__name__)

# Initialize AWS S3 client
s3 = boto3.client('s3', region_name=Config.AWS_REGION)

# OpenAI client for generating captions
llm = ChatOpenAI(model="gpt-4", openai_api_key=Config.OPENAI_API_KEY, max_tokens=4096)

def fetch_product_data(client_id, product_id):
    """Fetch the image and description from S3 for a given product."""
    
    image_key = f"client_uploads/{client_id}/{product_id}/image.png"
    description_key = f"client_uploads/{client_id}/{product_id}/description.txt"
    
    image_data = get_s3_file(Config.S3_BUCKET_NAME, image_key)
    description_data = get_s3_file(Config.S3_BUCKET_NAME, description_key)

    if not image_data or not description_data:
        logger.error(f"Missing image or description for client_id {client_id} and product_id {product_id}")
        return None, None

    description_text = description_data.decode('utf-8')
    
    try:
        image = Image.open(io.BytesIO(image_data))
    except Exception as e:
        logger.error(f"Error opening image for client_id {client_id} and product_id {product_id}: {e}")
        return None, None

    campaign_data = get_campaign_from_client(client_id, product_id)

    return image, description_text, campaign_data["campaign_type"], campaign_data["target_demographic"], campaign_data["length"]

def generate_captions_from_context(query, context, campaign_type, demographic, length):
    """Generate 7 days worth of captions and hashtags based on query and context."""
    prompt = [
        HumanMessage(content=f"Using the following context: {context}. Create {length} days' worth of Instagram captions to market this product: {query}. For each day, generate captions along with relevant hashtags."),
        AIMessage(content=f"Each day should have a unique caption and a unique set of hashtags. Campaign type should be {campaign_type}. Target demographic is {demographic}."),
        HumanMessage(content="Output should be in the format: {\"day\": \"Day 1\", \"caption\": \"Caption text\", \"hashtags\": \"#hashtag1 #hashtag2\"}"),
    ]

    try:
        response = llm(prompt)
        content = response.content.strip()

        days_content = content.split("\n\n")

        captions = []
        for i, day_content in enumerate(days_content):
            lines = day_content.split("\n")
            caption = lines[0]
            hashtags = lines[1] if len(lines) > 1 else ""

            captions.append({
                "day": f"Day {i+1}",
                "caption": caption,
                "hashtags": hashtags
            })

        return captions

    except Exception as e:
        logger.error(f"Error generating captions from context: {e}")
        return None

def generate_marketing_captions(client_id, product_id):
    """Main function to generate 7 days of Instagram captions and hashtags."""
    
    # Fetch product data from S3
    image, description_text, campaign_type, demographic, length = fetch_product_data(client_id, product_id)
    
    if not image or not description_text:
        return None

    # Extract image features
    image_features = extract_image_features(image)
    
    # Combine image features with the product description
    combined_text = f"Features: {image_features}\nDescription: {description_text}"

    # Perform similarity search using the combined text
    context = perform_similarity_search(combined_text)

    # Generate captions based on the query and the retrieved context
    captions = generate_captions_from_context(combined_text, context, campaign_type, demographic, length)

    if not captions:
        return None

    # Return the final JSON response
    return {
        "client_id": client_id,
        "product_id": product_id,
        "campaign_day": captions
    }
