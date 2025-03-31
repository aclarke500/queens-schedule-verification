import openai
from supabase import create_client
import numpy as np
from services.RAG_filters import get_filters_for_RAG

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


def get_n_chunks(message, messages, n=5):
    filters=get_filters_for_RAG(messages)
    
    vector = embed_query(message)

    # non filtered chunks
    response = supabase.rpc("match_chunks", {
    "query_embedding": vector,
    "match_count": n
    }).execute()
    chunks = response.data


    #filtered chunks
    response = supabase.rpc("filter_chunks", {
    "query_embedding": vector,
    "match_count": n,
    "filter_option": filters.get("option"),
    "filter_specialization": filters.get("specilization"),  # or 'specialization' if fixed
    "filter_major": filters.get("major")
    }).execute()

    filtered_chunks = response.data


    # Combine both filtered and non-filtered chunks
    all_chunks = chunks + filtered_chunks
    
    # Remove duplicates by creating a dictionary with content as key
    unique_chunks = {}
    for chunk in all_chunks:
        unique_chunks[chunk['content']] = chunk
    
    context = "\n\n".join([chunk['content'] for chunk in unique_chunks.values()])

    return context
# need one functio to embded users query str -> vector
# need to do cosine similarity search of supabase
# need to return top ten matches

