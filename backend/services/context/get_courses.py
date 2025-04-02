from langchain_openai import ChatOpenAI

from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()
SUPABASE_URL = os.getenv('supabase_url')
SUPABASE_SERVICE_KEY = os.getenv('supabase_service')
api_key = os.getenv('open_ai_key')
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# setup for LLM call
course_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an intelligent assistant analyzing a user's conversation to extract course references.

Your task:
- Identify **any course codes** mentioned or discussed in the user's message history.
- Return your output as a JSON object with a single key:
  - `"courses"`: an array of course codes.

Formatting Rules:
- All course codes must be **uppercase**, in the format: `DEPT-XXX` (e.g., `CISC-101`).
- If a course is mentioned without a full department code (e.g., `101` or `CSC 101`), assume the department is **CISC**, **MATH**, or **COGS**, and infer the most likely match.
- Do not include courses that are uncertain or ambiguous.
- Only return a valid JSON object. Do not include any explanation, markdown, or extra text.
"""),
    ("user", "{chat_history}")
])


course_llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=api_key)
course_parser = StructuredOutputParser.from_response_schemas([
    ResponseSchema(name="courses", description="Array of courses, i.e `['CISC-101','CISC-121']`")
])

course_chain = course_prompt | course_llm | course_parser

def get_courses(history):
    response = course_chain.invoke({"chat_history": history})  # ✅
    return response['courses']


# querying supabase for the courses
def get_course_info(courses):
    response = supabase.table("courses").select("*").in_("course_id", courses).execute()
    data = response.data
    course_info = ''
    for d in data:
        course_info += (f"Course id: {d['course_id']}, {d['course_info']}")
        
    return course_info
    

def get_course_context(user_messages: list) -> str:
    """Gets course context from conversation history.

    Analyzes conversation history to extract course codes and retrieves course information
    from the database for those courses.

    Args:
        user_messages: List of message dictionaries containing conversation history.

    Returns:
        A string containing concatenated course information for all referenced courses.
        Each course entry includes the course ID and course description.
    """
    courses = get_courses(user_messages)
    course_info = get_course_info(courses)
    return course_info
    