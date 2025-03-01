import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

def select_csv_file():
    """Open a file dialog to select CSV file"""
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    root.destroy()
    return file_path

def create_scatter_plot(file_path, title, xlabel, ylabel):
    """Create scatter plot from CSV data with custom labels"""
    try:
        df = pd.read_csv(file_path)
        
        if len(df.columns) != 2:
            raise ValueError("CSV must contain exactly two columns")
            
        x = df.iloc[:, 0]
        y = df.iloc[:, 1]

        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, color='blue', alpha=0.7)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Please select your CSV file:")
    csv_file = select_csv_file()
    
    if csv_file:
        # Get custom labels from user
        graph_title = input("Enter graph title: ")
        x_label = input("Enter X-axis label: ")
        y_label = input("Enter Y-axis label: ")
        
        print(f"Selected file: {csv_file}")
        create_scatter_plot(csv_file, graph_title, x_label, y_label)
    else:
        print("No file selected. Exiting...")