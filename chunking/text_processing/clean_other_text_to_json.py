import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import json
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

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
    },
      {
        "url": "https://www.cs.queensu.ca/undergraduate/courses/",
        "name": "courses2"
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


# define your expected schema
response_schemas = [
    ResponseSchema(name="chunk", description="A self-contained paragraph containing a rule or policy."),
    ResponseSchema(name="category", description=""),
]
parser = StructuredOutputParser.from_response_schemas(response_schemas)


system_prompt="""
You are a parsing assistant trained to extract and structure academic policy and curriculum text from university documentation.

Your task is to split the given text into **self-contained policy chunks** that represent academic rules, requirements, explanations, or guidelines relevant to students or advisors.

These documents may vary in structure. They are **not required** to follow a specific university plan format. You must use your judgment to:
- Group related sentences into coherent policy chunks
- Assign an appropriate `category` to each chunk

Each chunk should capture **one clear idea or policy**, and **no chunk should exceed 100 words**. Break longer sections into smaller logical units.

add a category or section title that describes the content in the chunk in a few words

⚠️ Return the **original text exactly as written** — do not reword or paraphrase.

🚫 Do **not** include extra formatting like ```json or triple backticks.

✅ Your response must be a JSON array, where each item includes:
- `chunk`: The raw academic text
- `category`: summary of the chunk (less than 10 words)

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
   
    return chunks



def get_chunks_from_file_list(file_list: list[str]):
    all_chunks = []
    for file in file_list:
        print(f"\n📄 Processing {file}...")
        
        url = get_url_from_name(file.split('/')[-1].split('.')[0])
        file_chunks = get_chunks_from_file(file)
        
        # Transform chunks into final format
        transformed_chunks = [{
            "content": chunk["chunk"],
            'section': chunk['category'],
            'option': False,
            'url': url,
            'major': False,
            'specialization': False,
        } for chunk in file_chunks]
        
        all_chunks.extend(transformed_chunks)
    return all_chunks
# Get list of all files in cleaned_text directory
files = [f'./cleaned_text/{file}' for file in [
    # 'ai_option.txt',
    # 'biomedical_computation_option.txt', 
    # 'biomedical_computing.txt',
    # 'cognitive_science.txt',
    # 'computing_creative_arts.txt',
    # 'computing_major.txt',
    # 'computing_math_analytics.txt',
    'courses.txt',
    'courses2.txt',
    # 'fundamental_computation_option.txt',
    'programs.txt',
    # 'security_option.txt',
    # 'software_design.txt',
    'specializations.txt'
]]

chunks = get_chunks_from_file_list(files)
# Save chunks to JSON file
output_path = Path(__file__).resolve().parents[1] / "data" / "chunks_other.json"
output_path.parent.mkdir(exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(chunks, f, indent=4, ensure_ascii=False)

print(f"✅ Saved {len(chunks)} chunks to {output_path}")

