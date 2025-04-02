import openai

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("open_ai_key")


def get_embedding(text: str) -> list[float]:
    """
    Get OpenAI embedding for a text string.
    
    Args:
        text: String to embed
        
    Returns:
        List of floats representing the embedding vector
    """
    try:
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return []
