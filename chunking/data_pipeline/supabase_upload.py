from supabase import create_client
import json
import os
from tqdm import tqdm
import dotenv



# Load environment variables
dotenv.load_dotenv()
url = os.getenv("supabase_url")
key= os.getenv("supabase_service_key")

supabase = create_client(url, key)

with open("data/chunk_embeddings.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

for chunk in tqdm(chunks, desc="Uploading chunks"):
    data = {
        "content": chunk["content"],
        "source": chunk["url"],
        "section": chunk["section"],
        "url": chunk["url"],
        "specialization": chunk["specialization"],
        "major": chunk["major"],
        "option": chunk["option"],
        "embedding": chunk["embedding"]  # ✅ raw float array
    }

    response = supabase.table("chunks").insert(data).execute()
