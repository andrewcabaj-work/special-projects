import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from def_act_notice_data import process_deferred_pdfs
from deficiency_notice_data import process_deficiency_pdfs

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_var.set(folder_selected)

def generate_file():
    folder_path = path_var.get().strip()
    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showerror("Invalid Path", "Please enter a valid folder path.")
        return

    selected_mode = mode_var.get()

    if selected_mode == "Deferred Activity Notices":
        result = process_deferred_pdfs(folder_path)
    elif selected_mode == "List of Deficiencies":
        result = process_deficiency_pdfs(folder_path)
    else:
        messagebox.showerror("Invalid Selection", "Please select a valid processing mode.")
        return
    
    if result:
        messagebox.showinfo("Success", f"Excel file saved to:\n{result}")
    else:
        messagebox.showwarning("No Data Found", "No matching PDF entries were found.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Trust Claim Notices [DKS] - Spreadsheet Application")

    # --- Folder Path (Row 0) ---
    tk.Label(root, text="Folder Path:").grid(row=0, column=0, pady=2, padx=5, sticky='w')
    path_var = tk.StringVar()
    path_entry = tk.Entry(root, textvariable=path_var, width=50)
    path_entry.grid(row=0, column=1, padx=5, pady=0)
    tk.Button(root, text="Browse", command=browse_folder, height=1).grid(row=0, column=2, padx=(0,5), pady=(0,2), sticky='we', ipady=0)

    # --- Mode Selection and Generate (Row 1) ---
    tk.Label(root, text="Select Mode:").grid(row=1, column=0, pady=0, padx=5, sticky='w')
    mode_var = tk.StringVar()
    mode_combobox = ttk.Combobox(root, textvariable=mode_var, state="readonly", width=47)
    mode_combobox['values'] = ("Deferred Activity Notices", "List of Deficiencies")
    mode_combobox.current(0)
    mode_combobox.grid(row=1, column=1, padx=5, pady=0, sticky='w')

    tk.Button(root, text="Generate Files", command=generate_file, height=1).grid(row=1, column=2, padx=(0,5), pady=(0,2), sticky='we', ipady=0)


    root.mainloop()
