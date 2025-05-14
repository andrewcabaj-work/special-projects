import pdfplumber
import pandas as pd
import re
import os

def process_deferred_pdfs(folder_path):
    parent_folder = os.path.basename(folder_path)
    output_filename = f"Deferred Activity Notices [{parent_folder}].xlsx"
    data = []

    pattern = re.compile(r'^([A-Z&]+)\s+(\d+)\s+(.+?)\s+SWMW LAW, LLC\s+(\d{1,2}/\d{1,2}/\d{4})$')
    capital_word_pattern = re.compile(r'^[A-Z\-]{2,}$')

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            with pdfplumber.open(pdf_path) as pdf:
                if len(pdf.pages) < 2:
                    continue
                page = pdf.pages[1]
                lines = page.extract_text().split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            match = pattern.match(line)

            if match:
                trust, claim_num, claimant_name, date = match.groups()
                name_parts = claimant_name.strip().split()
                if len(name_parts) == 1 and name_parts[0].isupper():
                    if (i + 1) < len(lines):
                        next_line = lines[i + 1].strip()
                        if capital_word_pattern.match(next_line):
                            claimant_name = f"{claimant_name} {next_line}"
                            i += 1

                data.append([claimant_name, trust, claim_num, date])
            i += 1

    df = pd.DataFrame(data, columns=[
        'Claimant Name', 'Trust', 'Claim Number', 'Deferral End Date'
    ])
    df.insert(0, 'Action Taken', '')
    df['Notes'] = ''

    output_path = os.path.join(folder_path, output_filename)
    df.to_excel(output_path, index=False)
    return output_path