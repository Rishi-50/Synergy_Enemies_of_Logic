from pdfminer.high_level import extract_text

def read_pdf(file_path):
    text = extract_text(file_path)
    return text

# Example usage
pdf_text = read_pdf('300-Hydraulic-Services-Plans.pdf')

# def read_text_file(file_path):
#     with open(file_path, 'r') as file:
#         text = file.read()
#     return text

# # Example usage
# text = read_text_file('path_to_your_document.txt')


import re

def extract_info(text, pattern):
    matches = re.findall(pattern, text)
    return matches

# Example usage for drawing numbers
drawing_numbers = extract_info(pdf_text, r'\bDrawing\s+(\d+)\b')


def extract_info(text):
    # Example patterns for drawing numbers and titles
    drawing_number_pattern = r'\bDrawing\s+(\d+)\b'
    drawing_title_pattern = r'\bDrawing Title:\s+(.+)'
    
    drawing_numbers = re.findall(drawing_number_pattern, text)
    drawing_titles = re.findall(drawing_title_pattern, text)
    
    return drawing_numbers, drawing_titles

def label_and_store(drawing_numbers, drawing_titles):
    extracted_info = {}
    for i, number in enumerate(drawing_numbers):
        extracted_info[number] = {
            'Title': drawing_titles[i],
            'Number': number
        }
    return extracted_info

import fitz  # PyMuPDF

def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_info = {}
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        
        drawing_numbers, drawing_titles = extract_info(text)
        extracted_info.update(label_and_store(drawing_numbers, drawing_titles))
    
    return extracted_info

