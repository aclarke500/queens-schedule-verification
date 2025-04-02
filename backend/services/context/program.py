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

def get_program_requirements(major: str):
    # For exact match:
    response = supabase.table('program_requirements').select('content').eq('major', major).execute()
    
    return response.data

def get_unique_majors()->str:
    response = supabase.table('program_requirements').select('major').execute()
    majors = [item['major'] for item in response.data]
    majors = list(set(majors))  # Convert to set and back to list to get unique values
    if 'false' in majors:
        majors.remove('false')
    return majors

# so we are looking up program requirements, what program is the most likely?
program_llm = ChatOpenAI(openai_api_key=api_key, temperature=0)
program_prompt = ChatPromptTemplate([
   ("system", """You are a smart assistant to a university course chatbot. Your job is to determine **if the user is referring to a specific Computer Science major or option** in their conversation.

Majors (also called options or specializations) include:
{majors}

Rules:
- ❌ Do NOT assume a major unless it is clearly referenced.
- ✅ Only include a major if it is explicitly mentioned (e.g., 'AI option') or the user refers to **something unique** to that major.
- 🧠 If the conversation is **generic** (e.g., asking about stats courses, electives, internships), do NOT include any majors.
- If the user does not specify a major, return an empty array like `"major": []`.

Output:
Always return a JSON object of the form:
  "major": ["ai", "biomed"]

Do not include any text, explanation, or formatting outside the JSON.
""")

])
program_parser = StructuredOutputParser.from_response_schemas([ResponseSchema(name="major", description="Array: like ['ai', 'funco']")])

program_chain = program_prompt | program_llm | program_parser


def get_majors(text):
    majors = get_unique_majors()
    response = program_chain.invoke({"majors":majors, "history":text})
    return response['major']


def get_program_context(text):
    majors_in_text = get_majors(text) # calls LLM
    if not (len(majors_in_text)):
        majors_in_text.append('funco')
    # since majors in text might be an array, we do this in a loop
    program_context = ''
    for major in majors_in_text:
        chunk = get_program_requirements(major)
        for row in chunk:
            program_context+=row['content']
    
    return program_context.strip()
