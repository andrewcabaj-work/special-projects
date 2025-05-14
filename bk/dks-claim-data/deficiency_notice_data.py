import pdfplumber
import pandas as pd
import re
import os

def process_deficiency_pdfs(folder_path):
    parent_folder = os.path.basename(folder_path)
    output_filename = f"Deficiency Notifications [{parent_folder}].xlsx"
    data = []

    # Regex to match a claim entry line
    claim_entry_pattern = re.compile(r'^(\d{7,8})\s+(.+?)\s+(\*{5}\d{4})$')
    deficiency_line_pattern = re.compile(r'^([A-Z]{0,2}\d{2,4}[A-Z]{0,3})\s+-')
    noise_patterns = [
        r'^Total:\s+\d+\s+Claim\(s\)',
        r'^List of Deficiencies for',
        r'^Firm:\s+SWMW LAW, LLC',
        r'^Attorney:\s+[A-Z .]+$',
        r'As of:\s*\d{1,2}/\d{1,2}/\d{4}',
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}'
        r'Claim\s*#',
        r'Name',
        r'SSN',
    ]
    compiled_noise = [re.compile(p) for p in noise_patterns]

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            raw_trust = os.path.basename(filename).split(' ')[0]
            trust = re.sub(r'\d+$', '', raw_trust)
            with pdfplumber.open(pdf_path) as pdf:
                # Start reading from page 2 onward
                lines = []
                for page in pdf.pages[1:]:
                    text = page.extract_text()
                    if text:
                        lines.extend(text.split('\n'))

            current_claim_number = None
            current_name = None
            current_deficiencies = []
            continued_once = False

            for line in lines:
                line = line.strip()
                claim_match = claim_entry_pattern.match(line)

                if claim_match:
                    # Save any existing claim's deficiencies first
                    if current_claim_number and current_deficiencies:
                        for deficiency in current_deficiencies:
                            data.append([
                                trust,
                                current_claim_number,
                                current_name,
                                deficiency
                            ])
                    # Start new claim
                    current_claim_number, current_name, _ = claim_match.groups()
                    current_deficiencies = []
                    continued_once = False
                
                else:
                    # See if the line is a deficiency code
                    deficiency_match = deficiency_line_pattern.match(line)
                    if deficiency_match:
                        current_deficiencies.append(line)
                        continued_once = False
                    else:
                        # continuation of last deficiency
                        if current_deficiencies and not continued_once:
                            if not any(p.search(line) for p in compiled_noise):
                                current_deficiencies[-1] += ' ' + line
                                continued_once = True

            # Save last claim after loop ends
            if current_claim_number and current_deficiencies:
                for deficiency in current_deficiencies:
                    data.append([
                        trust,
                        current_claim_number,
                        current_name,
                        deficiency
                    ])
    
    if not data:
        return None
    
    # Create DataFrame and Export
    df = pd.DataFrame(data, columns=[
        'Trust', 'Claim Name', 'Claim Number', 'Deficiency Codes'
    ])
    output_path = os.path.join(folder_path, output_filename)
    df.to_excel(output_path, index=False)
    return output_path
