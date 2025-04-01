from supabase import create_client
import json
import os
from tqdm import tqdm
import dotenv



# Load environment variables
dotenv.load_dotenv()
url = os.getenv("supabase_url")
key= os.getenv("supabase_service_key")

supabase = create_client(url, key)

import glob

# Get all .txt files in clean_text directory
cleaned_files = glob.glob("clean_text/*.txt")

for file in cleaned_files: 
    text = open(file, "r").read()
    file_suffix = file.split("\\")[1]
    course_id = file_suffix.split(".")[0]
    print(course_id)
    
    response = supabase.table("courses").insert({
        "course_id": course_id,
        "course_info": text
    }).execute()
    print(response)
    
