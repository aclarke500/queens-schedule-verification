import openai
from supabase import create_client
import numpy as np

from dotenv import load_dotenv
import os

load_dotenv()
SUPABASE_URL = os.getenv('supabase_url')
SUPABASE_SERVICE_KEY = os.getenv('supabase_service')
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
openai.api_key = os.getenv('open_ai_key')
# have one function that gives users query, and spits back some relevant chunks
def embed_query(query:str)->np.array:
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    return response.data[0].embedding




def get_n_chunks(message, n=5):
    vector = embed_query(message)
    response = supabase.rpc("match_chunks", {
    "query_embedding": vector,
    "match_count": n
    }).execute()
    chunks = response.data

    context = "\n\n".join([f"{chunk['content']}" for chunk in chunks])

    return context
# need one functio to embded users query str -> vector
# need to do cosine similarity search of supabase
# need to return top ten matches


print(get_n_chunks('What GPA do I need to get into Computing second year?'))