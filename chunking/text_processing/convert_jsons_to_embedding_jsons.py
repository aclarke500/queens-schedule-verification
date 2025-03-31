import json
import openai
import dotenv
import time
from tqdm import tqdm
import os

# Load environment variables
dotenv.load_dotenv()

# Get OpenAI API key
openai.api_key = os.getenv("open_ai_key")

if not openai.api_key:
    raise ValueError("❌ Missing 'OPENAI_API_KEY' in your .env file!")


# Load the two JSON files
with open('data/chunks.json', 'r') as f:
    chunks = json.load(f)

with open('data/chunks_other.json', 'r') as f:
    chunks_other = json.load(f)

# Combine the two lists into one
all_chunks = chunks + chunks_other
embedded_chunks = []

for chunk in tqdm(all_chunks, desc="Embedding chunks"):
    try:
        content = chunk["content"]
        response = openai.embeddings.create(
            model="text-embedding-3-small",  # 👈 switch to -3-large if needed
            input=content
        )
        embedding = response.data[0].embedding
        chunk["embedding"] = embedding
        embedded_chunks.append(chunk)
        time.sleep(0.5) # be nice to the rate limiter
    except Exception as e:
        print("Error embedding chunk:", e)

with open("data/chunk_embeddings.json", "w", encoding="utf-8") as f:
    json.dump(embedded_chunks, f, indent=2)