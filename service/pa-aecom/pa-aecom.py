import os
import csv
from tqdm import tqdm

def search_aecom_files(root_dir):
    aecom_files = []
    case_dirs = [d for d in os.listdir(root_dir) if d.isdigit()]

    for case_dir in tqdm(case_dirs, desc="Searching case files"):
        pleadings_dir = os.path.join(root_dir, case_dir, 'Pleadings')
        if os.path.exists(pleadings_dir):
            for filename in os.listdir(pleadings_dir):
                if 'aecom' in filename.lower():
                    aecom_files.append(os.path.join(pleadings_dir, filename))

    return aecom_files

def main():
    root_dir = r"\\twappsrv\TrialWorks\CaseFiles"
    aecom_files = search_aecom_files(root_dir)
    
    if aecom_files:
        print("Files containing 'aecom' in their names:")
        for file in aecom_files:
            print(file)
        
        # Append to CSV file
        with open('aecom_files.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            for file in aecom_files:
                csvwriter.writerow([file])
    else:
        print("No files containing 'aecom' found.")

if __name__ == "__main__":
    main()