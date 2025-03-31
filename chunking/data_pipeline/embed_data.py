import openai
import json
import time
from tqdm import tqdm

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

embedded_chunks = []

for chunk in tqdm(chunks, desc="Embedding chunks"):
    try:
        content = chunk["content"]
        response = openai.embeddings.create(
            model="text-embedding-3-small",  # 👈 switch to -3-large if needed
            input=content
        )
        embedding = response.data[0].embedding
        chunk["embedding"] = embedding
        embedded_chunks.append(chunk)
        time.sleep(0.5)  # Optional: be nice to the rate limiter
    except Exception as e:
        print("Error embedding chunk:", e)

with open("chunk_embeddings.json", "w", encoding="utf-8") as f:
    json.dump(embedded_chunks, f, indent=2)