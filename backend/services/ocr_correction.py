from langchain_openai import ChatOpenAI

from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv('open_ai_key')

CISC_courses = [
    "CISC 101", "CISC 102", "CISC 110", "CISC 121", "CISC 124", "CISC 151", "CISC 181",
    "CISC 203", "CISC 204", "CISC 220", "CISC 221", "CISC 223", "CISC 226", "CISC 235",
    "CISC 251", "CISC 271", "CISC 282", "CISC 320", "CISC 322", "CISC 324", "CISC 325",
    "CISC 326", "CISC 327", "CISC 330", "CISC 332", "CISC 335", "CISC 351", "CISC 352",
    "CISC 360", "CISC 365", "CISC 371", "CISC 422", "CISC 423", "CISC 426", "CISC 432",
    "CISC 434", "CISC 437", "CISC 447", "CISC 448", "CISC 451", "CISC 452", "CISC 453",
    "CISC 454", "CISC 455", "CISC 457", "CISC 458", "CISC 462", "CISC 465", "CISC 466",
    "CISC 468", "CISC 471", "CISC 472", "CISC 473", "CISC 474", "CISC 486", "CISC 490",
    "CISC 491", "CISC 492", "CISC 495", "CISC 496", "CISC 497", "CISC 498", "CISC 499",
    "CISC 500", "COCA 201", "COGS 100", "COGS 201", "COGS 499"
]

# Define LLM
llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=api_key)

# Output parser (list of course dicts)
parser = StructuredOutputParser.from_response_schemas([
    ResponseSchema(name="course_code", description="e.g. CISC 101"),
    ResponseSchema(name="day", description="Day of the week"),
    ResponseSchema(name="time_start", description="Start time, e.g. 9:30AM"),
    ResponseSchema(name="time_end", description="End time, e.g. 10:30AM"),
    ResponseSchema(name="location", description="Classroom or lecture hall")
])

correct_code_parser = StructuredOutputParser.from_response_schemas([
    ResponseSchema(name="course_code", description="e.g CISC 101")
])
# Prompt template




def structure_text(ocr_text: str) -> list:
    # Create a system message with the format instructions properly escaped
    system_message = """You are a helpful assistant that extracts university schedule entries from text.
    
After analyzing the content, respond with a JSON object containing schedule entries following this format:
```json
[
  {
    "course_code": "CISC 101",
    "day": "Monday",
    "time_start": "9:30AM",
    "time_end": "10:30AM",
    "location": "BioSci 1103"
  },
  ...additional entries
]
```
Each entry should have the course_code, day, time_start, time_end, and location fields."""

    # Create the messages
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": ocr_text}
    ]
    
    # Call the model
    response = llm.invoke(messages)
    
    # Extract and parse the JSON from the response
    try:
        import re
        # Find JSON array in the response
        json_match = re.search(r'\[\s*\{.*\}\s*\]', response.content, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            return json.loads(json_str)
        else:
            # If no JSON array is found, try to parse the entire content
            return json.loads(response.content)
    except json.JSONDecodeError:
        # If JSON parsing fails, apply more aggressive extraction
        try:
            # Look for content between ```json and ``` markers
            json_block_match = re.search(r'```json\s*([\s\S]*?)\s*```', response.content)
            if json_block_match:
                json_str = json_block_match.group(1)
                return json.loads(json_str)
        except:
            pass
        
        # If all parsing attempts fail, return an empty list
        print("Failed to parse JSON from the LLM response")
        print("Response:", response.content)
        return []

def validate_courses(courses: list) -> dict:
    for course in courses:
        code = course.get("course_code", "")
        prefix = code[:8]  # e.g. "CISC 101"
        subject = code[:4]
        if subject not in ["CISC", "COGS", "COCA"]:
            continue
        if prefix not in CISC_courses:
            correct_code = fix_ocr_course_code_typo(code, courses)
            course["course_code"] = correct_code

    return courses
def fix_ocr_course_code_typo(incorrect_code, courses):
    valid_course_codes = get_valid_course_codes(courses)

    # Create a system message with direct instructions
    system_message = f"""
    You are an OCR error corrector. The user will send a typo of a course code.
    Compare it against this list of valid course codes:
    {valid_course_codes}
    Return the one that is closest in format and spelling.
    
    Respond with ONLY the corrected course code, nothing else.
    """

    # Create messages
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": incorrect_code}
    ]
    
    # Call the model
    response = llm.invoke(messages)
    
    # Extract the correct code from the response
    correct_code = response.content.strip()
    
    return correct_code

def get_valid_course_codes(courses):
    valid_courses = []
    for course in courses:
        course_code = course["course_code"][:8]
        if course_code in CISC_courses:
            valid_courses.append(course_code)
    return valid_courses

def get_course_list(ocr_text: str) -> list:
    course_dicts = structure_text(ocr_text)
    validate_courses(course_dicts) # modifies the dict
    return course_dicts


def get_courses_from_ocr(ocr_text: str) -> list:
    course_dicts = structure_text(ocr_text)
    validate_courses(course_dicts) # modifies the dict
    for course in course_dicts:
        course["course_code"] = course["course_code"][:8]
    return course_dicts



text = "Schedule\nTi\n8.00AM\n9:00AM\n10:00AM\n11:00AM\n12:00PM\n1:00PM\n2:00PM\n3:00PM\n4:00PM\n5:00PM\nMonday\nMar 24\nCISC 474-001\nLecture\n10:30AM-\n11:30AM\nDunning Hall 11\nCISC 455-001\nLecture\n12:30PM -\n1:30PM\nKingston Hall\n101\nSTAT 362-001\nLecture\n1:30PM.\n2:30PM\nBiosciences\nComplex 1102\nMar 25\nCISC 332-001\nLecture\n8:30AM -\n9:30AM\nBiosciences\nComplex 1101\nWednesday\nCISC 474-001\nLecture\n9:30AM-\n10:30AM\nDunning Hall 11\nCISC 332-001\nLecture\n10:30AM-\n11:30AM\nBiosciences\nComplex 1101\nCISC 455-001\nLecture\n11:30AM-\n12:30PM\nKingston Hall\n101\nSTAT 362-001\nLecture\n12:30PM -\n1:30PM\nBiosciences\nComplex 1102\nThursday\nMar 27\nCISC 497-001\nLecture\n1:00PM.\n2:30PM\nJeffery Hall 126\nCISC 497-001\nLecture\n1:00PM-\n2:30PM\nJeffery Hall 126\nCISC 456-001\nLecture\n1:30PM.\n2:30PM\nKingston Hall\n101\nCISC 407-004\nSeminar\n4:00PM-\n5:30PM\nEllis Hall 333\nFriday\nMar 29\nCISC 474-001\nLecture\n8:30AM -\n9:30AM\nDunning Hall 11\nCISC 332-001\nLecture\n9:30AM-\n10:30AM\nBiosciences\nComplex 1101\nSTAT 362-001\nLecture\n11:30AM-\n12:30PM\nBiosciences\nComplex 1102\nSaturday\nMar 29\nSunday\nMar 30\n"
r = get_courses_from_ocr(text)