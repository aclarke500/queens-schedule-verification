import json
import csv

with open("chunk_embeddings.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

with open("supabase_chunk_embeddings.csv", "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    # Header
    writer.writerow(["content", "source", "section", "url", "embedding"])
    print('ef')
    for chunk in chunks:
        embedding_str = "{" + ",".join(map(str, chunk["embedding"])) + "}"

        # Write raw row with no quoting
        writer.writerow([
            chunk["content"],
            chunk["source"],
            chunk["section"],
            chunk["url"],
            embedding_str  # ⚠️ stays unquoted!
        ])
