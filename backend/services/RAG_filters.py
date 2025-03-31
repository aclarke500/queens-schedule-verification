from langchain_openai import ChatOpenAI

from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('open_ai_key')
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.0, openai_api_key=api_key)

SUPABASE_URL = os.getenv("supabase_url")
SUPABASE_KEY = os.getenv("supabase_service")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# need supabase to find out what majors are there - more calls but more resiliant to db changes
def get_unique_column_values(table_name: str, column_name: str) -> list:
    response = supabase.table(table_name).select(column_name).execute()
   

    all_values = [row[column_name] for row in response.data if column_name in row]
    unique_values = sorted(set(filter(lambda x: x is not None, all_values)))
    return unique_values


column_values = get_unique_column_values('chunks', 'major')
column_values.remove('false') # not a majors


rag_filter_prompt = ChatPromptTemplate.from_messages([
    ("system", f"""
You are a smart assistant that decides whether to apply academic filters (like major, option, or specialization) based on the user's recent conversation history.

Your job is to analyze the **entire message history** and determine if the user is asking about a **specific major** (e.g., AI, Biomedical, Software Design, etc.).

Return the following fields in a JSON object:

- `specilization`: Boolean — Is the query related to a specialization?
- `option`: Boolean — Is it referring to a program option?
- `major`: String — The major name (must be one of: {', '.join(column_values)}), or an empty string if not applicable.
- `is_major_dependent`: Boolean — True if the query depends on a specific major, False otherwise.

Rules:
- Only apply filters if the user **explicitly or strongly implies** a specific program or stream.
- If the message is general (e.g., about credit counts or policies), set all fields to False or empty.
- Never hallucinate — return `"is_major_dependent": false` unless there's clear evidence.

Respond only with a valid JSON object.
"""),
    ("user", "{chat_history}")
])


# spec, option, major
rag_filter_llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=api_key)
rag_filter_parser = StructuredOutputParser.from_response_schemas([
    ResponseSchema(name="specilization", description="Boolean: 'True' or 'False'"),
    ResponseSchema(name="option", description="Boolean: 'True' or 'False'"),
    ResponseSchema(name="major", description=f"String: must be one of {column_values}"),
    ResponseSchema(name="is_major_dependent", description="Boolean: 'True' or 'False'")
])

rag_filter_chain = rag_filter_prompt | rag_filter_llm | rag_filter_parser


def get_filters_for_RAG(messages:list)->dict:
    filter_result = rag_filter_chain.invoke({"chat_history", f"{messages}"})
    return filter_result