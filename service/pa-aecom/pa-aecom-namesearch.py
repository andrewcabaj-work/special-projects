import csv
import re
from PyPDF2 import PdfReader

# Define the path to the CSV file
csv_filepath = r"C:\Users\andrew.cabaj\Project Code\audits\document-search\aecom_files.csv"
output_csv_filepath = r"C:\Users\andrew.cabaj\Project Code\audits\document-search\output.csv"

# Function to read the first page of a PDF file and extract lines between "Plaintiff(s)" and "Defendant(s)"
def read(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            if len(reader.pages) > 0:
                first_page = reader.pages[0]
                text = first_page.extract_text()
                # Regex to find text between "Plaintiff(s)" and "Defendant(s)" or similar keywords
                match = re.search(r'Plaintiff\(s\)(.*?)Defendant\(s\)|Plaintiff\(s\)(.*?)Defendant|Plaintiff(.*?)Defendant\(s\)|Plaintiff(.*?)Defendant', text, re.DOTALL)
                if match:
                    return len(match.group(0).strip())
                else:
                    return 0  # Return 0 if keywords not found
            else:
                return 0  # Return 0 if no pages found
    except Exception as e:
        return f"Error reading {file_path}: {e}"

# Read the CSV file and process all file paths
with open(csv_filepath, 'r', encoding='latin1') as csvfile:
    csv_reader = csv.reader(csvfile)
    rows = []
    for row in csv_reader:
        file_path = row[0].strip('"')
        if 'AECOM' in file_path:
            content_length = read(file_path)
            rows.append([content_length])

# Write the output to a new CSV file
with open(output_csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Content Length'])
    csv_writer.writerows(rows)

print(f"Output written to {output_csv_filepath}")