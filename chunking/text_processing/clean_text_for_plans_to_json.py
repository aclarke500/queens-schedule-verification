import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import json
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
# from ..webscraping.websites import get_url_from_name



# this will be a dictionary of all the websites we want to scrape, and the site name we want the next to have
'''
https://www.cs.queensu.ca/undergraduate/programs/specializations/
https://www.cs.queensu.ca/undergraduate/programs/specializations/biomedical-computing.php
https://www.cs.queensu.ca/undergraduate/programs/specializations/cognitive-science.php
https://www.cs.queensu.ca/undergraduate/programs/specializations/computing-and-the-creative-arts.php
https://www.cs.queensu.ca/undergraduate/programs/specializations/computing-mathematics-and-analytics.php
https://www.cs.queensu.ca/undergraduate/programs/specializations/software-design.php
https://www.cs.queensu.ca/undergraduate/programs/options/artificial-intelligence.php
https://www.cs.queensu.ca/undergraduate/programs/options/biomedical-computation.php
https://www.cs.queensu.ca/undergraduate/programs/options/fundamental-computation.php
https://www.cs.queensu.ca/undergraduate/programs/options/security.php
https://www.cs.queensu.ca/undergraduate/courses/
'''
websites = [
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/",
        "name": "programs"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/major/",
        "name": "computing_major"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/",
        "name": "specializations"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/biomedical-computing.php",
        "name": "biomedical_computing"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/cognitive-science.php",
        "name": "cognitive_science"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/computing-and-the-creative-arts.php",
        "name": "computing_creative_arts"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/computing-mathematics-and-analytics.php",
        "name": "computing_math_analytics"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/specializations/software-design.php",
        "name": "software_design"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/options/artificial-intelligence.php",
        "name": "ai_option"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/options/biomedical-computation.php",
        "name": "biomedical_computation_option"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/options/fundamental-computation.php",
        "name": "fundamental_computation_option"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/programs/options/security.php",
        "name": "security_option"
    },
    {
        "url": "https://www.cs.queensu.ca/undergraduate/courses/",
        "name": "courses"
    }
]


def get_url_from_name(name: str) -> str:
    """
    Takes a program name and returns its corresponding URL from the websites list.
    
    Args:
        name: The name identifier of the program (e.g. 'ai_option', 'computing_major')
        
    Returns:
        The URL string for that program
        
    Raises:
        ValueError: If the name is not found in the websites list
    """
    for website in websites:
        if website["name"] == name:
            return website["url"]
    raise ValueError(f"No URL found for program name: {name}")


ALLOWED_CATEGORIES = {
    "program_description",
    "program_structure",
    "core_requirements",
    "option_requirements",
    "supporting_requirements",
    "elective_requirements",
    "substitution_policy",
    "note",
    "course_list",
    "unit_policy",
    "prerequisite_policy",
    "general_policy",
    "misc"
}


# Load .env from project root no matter where this script is run
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# Get OpenAI API key
open_ai_key = os.getenv("open_ai_key")
deepseek_key = os.getenv("deepseek_key")

if not open_ai_key:
    raise ValueError("❌ Missing 'open_ai_key' in your .env file!")

# Initialize OpenAI client
client = OpenAI(
    base_url="https://api.deepseek.com/v1",
    organization="org-deepseek",
    api_key=deepseek_key
)


def get_major_metadata(filename: str) -> dict:
    if filename.endswith("ai_option.txt"):
        return {"major": "ai", "specialization": False, "option": True}
    
    elif filename.endswith("biomedical_computation_option.txt"):
        return {"major": "biomedical", "specialization": False, "option": True}
    
    elif filename.endswith("biomedical_computing.txt"):
        return {"major": "biomedical", "specialization": True, "option": False}
    
    elif filename.endswith("cognitive_science.txt"):
        return {"major": "cognitive_science", "specialization": True, "option": False}
    
    elif filename.endswith("computing_creative_arts.txt"):
        return {"major": "creative_arts", "specialization": True, "option": False}
    
    elif filename.endswith("computing_major.txt"):
        return {"major": "computing", "specialization": False, "option": False}
    
    elif filename.endswith("computing_math_analytics.txt"):
        return {"major": "math_analytics", "specialization": True, "option": False}
    
    elif filename.endswith("courses.txt"):
        return {"major": None, "specialization": False, "option": False}
    
    elif filename.endswith("fundamental_computation_option.txt"):
        return {"major": "funco", "specialization": False, "option": True}
    
    elif filename.endswith("programs.txt"):
        return {"major": None, "specialization": False, "option": False}
    
    elif filename.endswith("security_option.txt"):
        return {"major": "security", "specialization": False, "option": True}
    
    elif filename.endswith("software_design.txt"):
        return {"major": "software_design", "specialization": True, "option": False}
    
    elif filename.endswith("specializations.txt"):
        return {"major": None, "specialization": False, "option": False}
    else:
        
        return {"major": None, "specialization": False, "option": False}





# define your expected schema
response_schemas = [
    ResponseSchema(name="chunk", description="A self-contained paragraph containing a rule or policy."),
    ResponseSchema(name="category", description=""),
]
parser = StructuredOutputParser.from_response_schemas(response_schemas)


system_prompt="""
You are a parsing assistant trained to extract and structure academic policy text from university program documents.

Your task is to split the given text into **self-contained policy chunks** that represent rules, requirements, or academic guidelines.

If the text follows a standard university degree plan format (e.g., with sections like Core, Option, Substitutions, Notes), break it up by those sections, and preserve the hierarchy using the `category` field.

If the document **does not** follow that format, break the text into logical units that still represent distinct academic policies, rules, or requirements. Use your judgment to assign a clear and concise `category` that reflects the purpose of the chunk (e.g., `admission`, `eligibility`, `general_policy`, `note`, etc.).
There should be somewhere between 4 and 5 chunks for each document. Use more or less chunks depending on the length of the document.
If some information is not relevant to the university and courses, skip that information and do not include it in the output.
Break the core requirements into multiple chunks at a logical level, no chunk should be more than 100 words.
For the `category` field, use one of the following allowed labels exactly:
program_description, program_structure, core_requirements, option_requirements, supporting_requirements, elective_requirements, substitution_policy, note, course_list, unit_policy, prerequisite_policy, general_policy
If the chunk does not fit clearly, use `misc`. 
⚠️ Return each chunk of text **exactly as it appears** in the input. Do not paraphrase or reword.
Return your output as a JSON array of objects. Do not wrap the objects individually. Do not include any markdown formatting like ```json or triple backticks."

Your response must be a JSON list where each item has:
- `chunk`: The raw text of the rule or policy, unchanged
- `category`: A short label describing the purpose of the chunk
"""

# your prompt structure
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "Here is the text to parse:\n\n{text}\n\nPlease format your response according to these instructions:\n{format_instructions}")
])

def get_chunks_from_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Format the prompt with the text and format instructions
    formatted_prompt = prompt_template.format_messages(
        text=text,
        format_instructions=parser.get_format_instructions()
    )
    
    response = client.chat.completions.create(
        model="deepseek-coder",  # or "gpt-4" if you prefer
        messages=[{"role": "user" if m.type == "human" else m.type, "content": m.content} for m in formatted_prompt],
        temperature=0
    )

    raw = response.choices[0].message.content
    print("🔍 Raw response from model:\n", raw)

    # Clean up the response by removing markdown code block formatting
    cleaned_response = raw.strip()
    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response[7:]  # Remove ```json
    if cleaned_response.startswith("```"):
        cleaned_response = cleaned_response[3:]  # Remove ```
    if cleaned_response.endswith("```"):
        cleaned_response = cleaned_response[:-3]  # Remove trailing ```
    
    chunks = json.loads(cleaned_response.strip())
    for chunk in chunks:
        if chunk["category"] not in ALLOWED_CATEGORIES:
            chunk["category"] = "misc"

    return chunks


def get_chunks_from_file_list(file_list: list[str]):
    all_chunks = []
    for file in file_list:
        print(f"\n📄 Processing {file}...")
        metadata = get_major_metadata(file)
        url = get_url_from_name(file.split('/')[-1].split('.')[0])
        file_chunks = get_chunks_from_file(file)
        
        # Transform chunks into final format
        transformed_chunks = [{
            "content": chunk["chunk"],
            'section': chunk['category'],
            'option': metadata['option'],
            'url': url,
            'major': metadata['major'],
            'specialization': metadata['specialization']
        } for chunk in file_chunks]
        
        all_chunks.extend(transformed_chunks)
    return all_chunks
# Get list of all files in cleaned_text directory
files = [f'./cleaned_text/{file}' for file in [
    'ai_option.txt',
    'biomedical_computation_option.txt', 
    'biomedical_computing.txt',
    'cognitive_science.txt',
    'computing_creative_arts.txt',
    'computing_major.txt',
    'computing_math_analytics.txt',
    # 'courses.txt',
    'fundamental_computation_option.txt',
    # 'programs.txt',
    'security_option.txt',
    'software_design.txt',
    # 'specializations.txt'
]]

chunks = get_chunks_from_file_list(files)
# Save chunks to JSON file
output_path = Path(__file__).resolve().parents[1] / "data" / "chunks.json"
output_path.parent.mkdir(exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(chunks, f, indent=4, ensure_ascii=False)

print(f"✅ Saved {len(chunks)} chunks to {output_path}")

for c in chunks:
    print(c)
    print('**********************')
