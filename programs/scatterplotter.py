import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

def select_csv_file():
    """Open a file dialog to select CSV file"""
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    root.destroy()
    return file_path

def create_scatter_plot(file_path):
    """Create scatter plot from CSV data"""
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Check if there are exactly two columns
        if len(df.columns) != 2:
            raise ValueError("CSV must contain exactly two columns")
            
        # Extract X and Y data
        x = df.iloc[:, 0]  # First column
        y = df.iloc[:, 1]  # Second column
        
        # Create plot
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, color='blue', alpha=0.7)
        
        # Add labels and title
        plt.xlabel(df.columns[0])
        plt.ylabel(df.columns[1])
        plt.title(f"Scatter Plot: {df.columns[0]} vs {df.columns[1]}")
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Please select your CSV file:")
    csv_file = select_csv_file()
    
    if csv_file:
        print(f"Selected file: {csv_file}")
        create_scatter_plot(csv_file)
    else:
        print("No file selected. Exiting...")