from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("open_ai_key")

llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=api_key)

response_schemas = [
    ResponseSchema(name="lookup_courses", description="Boolean: Should we fetch specific courses?"),
    ResponseSchema(name="lookup_program_info", description="Boolean: Should we check program plans, options, or specializations?"),
    ResponseSchema(name="rag_general", description="Boolean: Should we perform RAG on general university content?"),
    ResponseSchema(name="rag_courses", description="Boolean: Should we perform RAG for course-related questions?"),
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a planning assistant that determines which context sources need to be retrieved based on the user's recent message history.

Analyze the message history and return a JSON object with the following **four Boolean fields**, using `true` or `false` (all fields are required):

- `lookup_courses`: Is the user asking about one or more specific courses?
- `lookup_program_info`: Should we fetch major plans, specializations, or option requirements?
- `rag_general`: Should we retrieve general content using semantic search (RAG)?
- `rag_courses`: Should we use RAG to get fuzzy course information?

Even if a field does not apply, include it in the output with a value of `false`.

 Only return a valid JSON object with these exact four keys. Do not include comments, extra text, or markdown formatting.
"""),
    ("user", "{chat_history}")
])


context_planner_chain = prompt | llm | parser

def get_context_retrieval_flags(chat_history: str) -> dict:
    """Gets flags indicating which context sources to retrieve based on chat history.

    This function analyzes the chat history and determines which context sources
    (courses, program info, general content, etc.) should be retrieved to help
    inform the response.

    Args:
        chat_history: String containing the conversation history with the user

    Returns:
        dict: Dictionary with Boolean flags for each context source:
            - lookup_courses: Whether to fetch specific course info
            - lookup_program_info: Whether to get program/specialization info  
            - rag_general: Whether to do RAG on general university content
            - rag_courses: Whether to do RAG for course-related info
    """
    return context_planner_chain.invoke({"chat_history": chat_history})
