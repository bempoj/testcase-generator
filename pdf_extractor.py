import pymupdf
import os
from tkinter import Tk, filedialog
from config import *
from openai import OpenAI

chunk_size = 3
client = OpenAI(api_key = "")

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
    
    temp_chunks = 0
    current_index = 0
    current_chunk = ''
    
    while current_index < len(extracted_text):
        current_chunk += extracted_text[current_index]
        
        if temp_chunks == chunk_size:
            print("\n Sending PDF content to OpenAI...")
            #print(current_chunk)
            response = send_to_openai(f"Here’s the current text chunk from my PDF:\n\n{current_chunk}\n\nCan you write test cases based on this content?")
            print(response)
            current_chunk = ''
            temp_chunks = 0
            
        temp_chunks += 1
        current_index += 1
    
else:
    print("No file selected!")

