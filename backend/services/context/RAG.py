import openai
from supabase import create_client
import numpy as np
from langchain_openai import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# setup api keys
load_dotenv()
SUPABASE_URL = os.getenv('supabase_url')
SUPABASE_SERVICE_KEY = os.getenv('supabase_service')
api_key = os.getenv('open_ai_key')
openai.api_key = api_key

# create supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
# have one function that gives users query, and spits back some relevant chunks
def embed_query(query:str)->np.array:
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    return response.data[0].embedding




# rephrase conversation for rag
llm = ChatOpenAI(model="gpt-4o", api_key=api_key)

parser = StructuredOutputParser.from_response_schemas([ResponseSchema(name="query", description="String: i.e 'CISC 101 compared to CISC 121'")])
prompt = ChatPromptTemplate([
   ("system", """
You are an intelligent assistant helping to drive a context-aware RAG system. Your job is to analyze the entire user conversation and extract a focused query string that captures **what should be looked up** in the vector database to help the user.
 Your task:
 
- Read the **entire chat history** to understand the user’s intent.
- Prioritize the **most recent user messages**, but use earlier messages for disambiguation.
- Return a **concise, semantically rich query** (5–20 words) that captures what the user is trying to learn, resolve, or understand.

Examples:
- If the user asks “Do I need stats for AI?”, return: `"AI option statistics requirements"`
- If the user asks “What’s the difference between biomed and software design?”, return: `"biomedical computing vs software design comparison"`
- If the user says “How do internships work?”, return: `"computing internship program structure"`

Output format:
Respond with a JSON object like this:
{{
  "query": "your focused search string here"
}}

 Do not:
- Include unnecessary formatting or markdown
- Paraphrase the user's entire message
- Ask follow-up questions
- Return an empty string — always infer a search query, even if it’s broad
"""),
   ("system", "{messages}")

])
chain = prompt | llm | parser

def get_query(chat_history):
    """Extracts a focused search query from chat history using an LLM.

    Args:
        chat_history: List of message dictionaries containing conversation history.
            Each message should have 'role' and 'content' keys.

    Returns:
        str: A concise query string (5-20 words) capturing the key information need.

    Raises:
        None
    """
    response = chain.invoke({"messages":chat_history})
    return response['query']



def get_general_context(messages, n=5):
    """Retrieves relevant context chunks from vector database based on conversation.

    Uses the conversation to generate a search query, embeds it, and finds matching
    chunks from the vector database.

    Args:
        messages: List of message dictionaries containing conversation history.
            Each message should have 'role' and 'content' keys.
        n: Optional; Number of context chunks to retrieve. Defaults to 5.

    Returns:
        str: Concatenated content from the retrieved context chunks.

    Raises:
        None
    """
    query = get_query(messages)
    vector = embed_query(query)
    # non filtered chunks
    response = supabase.rpc("match_chunks", {
    "query_embedding": vector,
    "match_count": n
    }).execute()
    chunks = response.data

    context = ''
    for chunk in chunks:
        context+=chunk['content']
   
    return context
