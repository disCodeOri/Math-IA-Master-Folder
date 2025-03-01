import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# Known parameter
BOLT_REAL_HEIGHT_CM = 195  # Usain Bolt's official height

class BoltScalingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bolt Data Scaler")
        
        # File path
        self.bolt_path = None
        
        # Video measurement
        self.measured_height = None
        
        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # CSV selection
        tk.Button(self.root, text="Select Bolt CSV", 
                 command=self.load_bolt).grid(row=0, column=0, padx=5, pady=5)
        self.bolt_label = tk.Label(self.root, text="No file selected")
        self.bolt_label.grid(row=0, column=1, padx=5, pady=5)
        
        # Video height input
        tk.Label(self.root, text="Measured video height (cm):").grid(row=1, column=0)
        self.video_height = tk.Entry(self.root)
        self.video_height.grid(row=1, column=1)
        
        # Process button
        tk.Button(self.root, text="Scale Data", 
                 command=self.process_data).grid(row=2, column=0, columnspan=2, pady=10)

    def load_bolt(self):
        self.bolt_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.bolt_label.config(text=self.bolt_path.split("/")[-1])

    def process_data(self):
        try:
            # Get measured video height (241.17 in your case)
            measured = float(self.video_height.get())
            
            # Calculate scaling factor
            scale_factor = BOLT_REAL_HEIGHT_CM / measured
            
            # Load data
            df = pd.read_csv(self.bolt_path)
            
            # Scale coordinates (preserve time column)
            for col in ['Cleaned Ankle 1', 'Cleaned zAnkle 2']:
                df[col] = (df[col] * scale_factor).round(2)
            
            # Save scaled data
            save_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialfile="scaled_bolt.csv"
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
    app = BoltScalingApp(root)
    root.mainloop()