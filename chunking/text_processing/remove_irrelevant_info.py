from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
deepseek_key = os.getenv('deepseek_key')


client = OpenAI(
    base_url="https://api.deepseek.com/v1",  # 🔁 Use DeepSeek endpoint
    api_key=deepseek_key
)

prompt = (
    "You are a content filter for a university schedule advisor. The user will provide scraped website text. "
    "Remove any content not related to academic rules, enrollment requirements, courses, course prerequisites, or graduation policies. Include the course title."
    "Only keep relevant academic content. Do NOT summarize. Return the text exactly as written. If no text is relevant return an empty string."
)

def clean_text(input_path, output_path, prompt):
    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Break into 2000-line chunks
    chunk_size = 2000
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

    cleaned_sections = []

    for i, chunk in enumerate(chunks):
        chunk_text = "".join(chunk)

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": chunk_text}
        ]

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )

        cleaned = response.choices[0].message.content
        cleaned_sections.append(cleaned)
        print(f"✅ Cleaned chunk {i + 1}/{len(chunks)}")

    # Save output
    with open(output_path, 'w', encoding='utf-8') as out_file:
        out_file.write("\n\n".join(cleaned_sections))

    print(f"🧼 Done! Cleaned text saved to {output_path}")
    
# Get all files from raw_text directory
raw_text_dir = 'raw_text_from_websites'
output_dir = 'cleaned_text'


def clean_raw_text(input_dir, output_dir):
# Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process each file in raw_text directory
    for filename in os.listdir(raw_text_dir):
        if filename.endswith('.txt'):
            input_path = os.path.join(raw_text_dir, filename)
            output_path = os.path.join(output_dir, filename)
            print(f"\n📄 Processing {filename}...")
            clean_text(input_path, output_path, prompt)
                

