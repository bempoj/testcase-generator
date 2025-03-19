import pymupdf
import os
import json
from tkinter import Tk, filedialog
#from config import *
from openai import OpenAI

chunk_size = 3
client = OpenAI(api_key = "")

def load_json():
    Tk().withdraw()
    json_path = filedialog.askopenfilename(
        title="Select a Test Case Schema JSON file",
        filetypes=[("JSON files", "*.json")]
    )

    if not json_path:
        print("No JSON file selected!")
        return {}

    try:
        with open(json_path, "r", encoding="utf-8") as schema_file:
            schema_data = json.load(schema_file)
            print("\nSchema loaded successfully!")
            return schema_data.get("schema", {})
    except Exception as e:
        print(f"Error loading file: {e}")
        return {}

def pdf_reader(pdf_path):
    doc = pymupdf.open(pdf_path)
    text = []
    for page in doc:
        text.append(str(page.get_text().encode("utf8")))
       
    return text

def send_to_openai(prompt_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a helpful assistant."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content

pdf_path = filedialog.askopenfilename(
    title="Select a PDF file",
    filetypes=[("PDF files", "*.pdf")]
)

if pdf_path:
    extracted_text = pdf_reader(pdf_path)
    
    test_case_schema = load_json()
    
    if not test_case_schema:
        print("Schema failed to load.")
    
    temp_chunks = 0
    current_index = 0
    current_chunk = ''
    
    while current_index < len(extracted_text):
        current_chunk += extracted_text[current_index]
        
        if temp_chunks == chunk_size:
            print("\n Sending PDF content to OpenAI...")
            
            #print(current_chunk)
            
            response = send_to_openai(
                f"Here’s the current text chunk from my PDF:\n\n{current_chunk}"
                f"\n\nCan you write test cases based on this content, following this schema:\n{json.dumps(test_case_schema, indent=2)}"
                )
            print(response)
            
            current_chunk = ''
            temp_chunks = 0
            
        temp_chunks += 1
        current_index += 1
    
else:
    print("No PDF file selected!")

