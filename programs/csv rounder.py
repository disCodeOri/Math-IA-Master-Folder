import csv
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

def round_to_two_decimals(value):
    try:
        return round(float(value), 2)
    except ValueError:
        return value

def process_csv_file(input_file, output_file):
    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            rounded_row = [round_to_two_decimals(cell) for cell in row]
            writer.writerow(rounded_row)

def process_multiple_files(file_paths):
    for input_file in file_paths:
        output_file = os.path.splitext(input_file)[0] + '_rounded.csv'
        process_csv_file(input_file, output_file)
        print(f"Processed {input_file} -> {output_file}")

def select_files():
    # Hide the root Tkinter window
    Tk().withdraw()
    # Open a file dialog to select CSV files
    file_paths = askopenfilenames(
        title="Select CSV Files",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    return file_paths

# Example usage
if __name__ == "__main__":
    # Let the user select the files
    selected_files = select_files()
    
    if selected_files:
        # Process the selected files
        process_multiple_files(selected_files)
        print("Processing complete!")
    else:
        print("No files selected.")