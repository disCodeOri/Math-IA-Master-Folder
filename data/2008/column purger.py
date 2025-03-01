import csv
import os
from tkinter import Tk, filedialog, messagebox, Listbox, Button, Label, StringVar, END, MULTIPLE

def remove_columns(input_file, columns_to_remove):
    # Read the input CSV file
    with open(input_file, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        headers = next(reader)  # Read the header row
        data = list(reader)     # Read the rest of the data

    # Determine the indices of the columns to remove
    columns_to_remove_indices = [headers.index(col) for col in columns_to_remove]

    # Remove the specified columns
    new_headers = [header for i, header in enumerate(headers) if i not in columns_to_remove_indices]
    new_data = [[row[i] for i in range(len(row)) if i not in columns_to_remove_indices] for row in data]

    # Write the new CSV file
    output_file = os.path.splitext(input_file)[0] + '_modified.csv'
    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(new_headers)
        writer.writerows(new_data)

    messagebox.showinfo("Success", f"Modified file saved as {output_file}")

def select_columns(input_file):
    # Read the headers from the CSV file
    with open(input_file, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        headers = next(reader)

    # Create a Tkinter window for column selection
    root = Tk()
    root.title("Select Columns to Remove")

    # Label for instructions
    Label(root, text="Use the arrow keys to navigate and Space to select/deselect columns:").pack()

    # Listbox to display columns
    listbox = Listbox(root, selectmode=MULTIPLE, height=len(headers))
    for header in headers:
        listbox.insert(END, header)
    listbox.pack()

    # Function to confirm selection
    def confirm_selection():
        selected_columns = [listbox.get(i) for i in listbox.curselection()]
        if not selected_columns:
            messagebox.showwarning("No Selection", "Please select at least one column to remove.")
            return
        root.destroy()
        remove_columns(input_file, selected_columns)

    # Confirm button
    Button(root, text="Confirm", command=confirm_selection).pack()

    # Run the Tkinter event loop
    root.mainloop()

def main():
    # Hide the root Tkinter window
    root = Tk()
    root.withdraw()

    # Open a file selector dialog to choose the CSV file
    input_file = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )

    # Check if a file was selected
    if not input_file:
        messagebox.showwarning("No File Selected", "No file selected. Exiting.")
        return

    # Open the column selection window
    select_columns(input_file)

if __name__ == "__main__":
    main()