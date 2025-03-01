import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# Known parameters (heights in centimeters)
GATLIN_REAL_HEIGHT_CM = 185  # Justin Gatlin's real height

class ScalingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gatlin Data Scaler")
        
        # File path
        self.gatlin_path = None
        
        # Video measurement
        self.gatlin_video_height = None
        
        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Gatlin CSV selection
        tk.Button(self.root, text="Select Gatlin CSV", 
                 command=self.load_gatlin).grid(row=0, column=0, padx=5, pady=5)
        self.gatlin_label = tk.Label(self.root, text="No file selected")
        self.gatlin_label.grid(row=0, column=1, padx=5, pady=5)
        
        # Video height input
        tk.Label(self.root, text="Gatlin's measured video height (cm):").grid(row=1, column=0)
        self.gatlin_video = tk.Entry(self.root)
        self.gatlin_video.grid(row=1, column=1)
        
        # Process button
        tk.Button(self.root, text="Scale Data", 
                 command=self.process_data).grid(row=2, column=0, columnspan=2, pady=10)

    def load_gatlin(self):
        self.gatlin_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.gatlin_label.config(text=self.gatlin_path.split("/")[-1])

    def process_data(self):
        try:
            # Get measured video height
            measured_height = float(self.gatlin_video.get())
            
            # Calculate scaling factor
            scale_factor = GATLIN_REAL_HEIGHT_CM / measured_height
            
            # Load data
            df = pd.read_csv(self.gatlin_path)
            
            # Scale and round coordinates (preserve time column)
            for col in ['Ankle 1', 'Ankle 2']:
                df[col] = (df[col] * scale_factor).round(2)
            
            # Save scaled data
            save_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialfile="scaled_gatlin.csv"
            )
            df.to_csv(save_path, index=False)
            
            messagebox.showinfo(
                "Success", 
                f"Data scaled by {scale_factor:.3f}x and saved to:\n{save_path}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ScalingApp(root)
    root.mainloop()