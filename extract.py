import boto3
import os
import shutil
import re
import PyPDF2

def split_pdf(pdf_path, output_dir='pdf_pages'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)
    
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page_num, page in enumerate(reader.pages):
            writer = PyPDF2.PdfWriter()
            writer.add_page(page)
            output_path = os.path.join(output_dir, f'page_{page_num + 1}.pdf')
            with open(output_path, 'wb') as output_pdf:
                writer.write(output_pdf)
    
    return [os.path.join(output_dir, f'page_{page_num + 1}.pdf') for page_num in range(len(reader.pages))]

def extract_text_with_textract(pdf_path):
    client = boto3.client('textract')
    with open(pdf_path, 'rb') as document:
        response = client.analyze_document(
            Document={'Bytes': document.read()},
            FeatureTypes=['FORMS', 'TABLES']
        )
    return response

def parse_textract_response_with_merged_lines(response):
    # Here we define regex patterns for direct fields
    patterns = {
        'Payment to': r'Payment to:\s*(.+)',
        'Payment Date': r'Payment date:\s*(\w{3} \d{2}, \d{4})',
        'Payment Number': r'Payment number:\s*(\d+)',
        'Patient Name': r'PATIENT NAME:\s*(.+)',
        # Multiline regex patterns
        'Patient ID': r'PATIENT[\s\S]*?ID:\s*(\d+)',
        'Service Provider ID': r'HEALTH CARE PROFESSIONAL[\s\S]*?ID:\s*(\d+)',
    }

    # It initialize the output dictionary
    extracted_data = {
        "Payment to": None,
        "Payment Date": None,
        "Payment Number": None,
        "Total Amount Charged": None,
        "Total Contracted Amount": None,
        "Amount Eligible for Coverage": None,
        "Patient Name": None,
        "Patient ID": None,
        "Service Provider ID": None,
        "Service on":None
    }

    # Extract blocks of text
    blocks = response.get('Blocks', [])
    raw_text = "\n".join([block['Text'] for block in blocks if block['BlockType'] == 'LINE'])

    # Extract direct fields and multiline patterns
    for key, pattern in patterns.items():
        match = re.search(pattern, raw_text, re.IGNORECASE)
        if match:
            extracted_data[key] = match.group(1).strip()

    # Table extraction logic remains the same
    blocks_map = {block['Id']: block for block in blocks}
    for block in blocks:
        if block['BlockType'] == 'TABLE':
            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        cell = blocks_map[child_id]
                        if cell['BlockType'] == 'CELL':
                            row_index = cell.get('RowIndex', 1) - 1
                            col_index = cell.get('ColumnIndex', 1) - 1
                            cell_text = ''.join([
                                blocks_map[word_id]['Text'] for word_id in cell.get('Relationships', [{}])[0].get('Ids', [])
                                if blocks_map[word_id]['BlockType'] == 'WORD'
                            ]).strip()
                            # Map values based on known table structure
                            if row_index == 4 and col_index == 0:  # Total Amount Charged
                                extracted_data["Total Amount Charged"] = cell_text
                            elif row_index == 4 and col_index == 1:  # Total Contracted Amount
                                extracted_data["Total Contracted Amount"] = cell_text
                            elif row_index == 4 and col_index == 2:  # Amount Eligible for Coverage
                                extracted_data["Amount Eligible for Coverage"] = cell_text

    return extracted_data

def process_eob_pdf_with_multiline(file_path):
    pdf_pages = split_pdf(file_path)
    all_data = []
    for pdf_page in pdf_pages:
        response = extract_text_with_textract(pdf_page)
        data = parse_textract_response_with_merged_lines(response)
        all_data.append(data)

    # Merge results for a complete summary
    final_data = {key: None for key in all_data[0].keys()}
    for entry in all_data:
        for key, value in entry.items():
            if value:  # Prioritize non-null values
                final_data[key] = value

    return final_data

def extract(file_path):
    result = process_eob_pdf_with_multiline(file_path)
    return result
