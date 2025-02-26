import os
import sys
import zipfile
from math import ceil
import tkinter as tk
from tkinter import simpledialog, messagebox

# Allow user to provide the maximum number of files per split zip file
def get_user_input():
    root = tk.Tk()
    root.withdraw()
    user_input = simpledialog.askinteger("Input", "Enter the maximum number of items per zip (default 800):", initialvalue=800)
    root.destroy()
    return user_input

# Function to show error message
def show_error_message(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", message)
    root.destroy()

try:
    max_files_per_zip = get_user_input()

    if max_files_per_zip is None:
        sys.exit()

    current_directory = os.path.dirname(os.path.abspath(__file__))

    primary_zip_dir = os.path.join(current_directory, 'primary_zip')
    split_zips_dir = os.path.join(current_directory, 'split_zips')

    os.makedirs(split_zips_dir, exist_ok=True)

    zip_files = [f for f in os.listdir(primary_zip_dir) if f.endswith('.zip')]
    if not zip_files:
        raise FileNotFoundError(f"No zip files found in {primary_zip_dir}")
        sys.exit()

    first_zip_file = zip_files[0]

    with zipfile.ZipFile(os.path.join(primary_zip_dir, first_zip_file), 'r') as zip_ref:
        zip_ref.extractall('temp_extracted')

    extracted_files = os.listdir('temp_extracted')

    num_splits = ceil(len(extracted_files) / max_files_per_zip)

    for i in range(num_splits):
        part_files = extracted_files[i*max_files_per_zip:(i+1)*max_files_per_zip]
        part_number = i + 1
        new_zip_filename = f"part-{part_number}.zip"
        
        with zipfile.ZipFile(os.path.join(split_zips_dir, new_zip_filename), 'w') as zip_ref:
            for file in part_files:
                zip_ref.write(os.path.join('temp_extracted', file), file)

    for file in extracted_files:
        os.remove(os.path.join('temp_extracted', file))
    os.rmdir('temp_extracted')

except Exception as e:
    show_error_message(str(e))
