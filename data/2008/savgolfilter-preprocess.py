import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from matplotlib.widgets import RadioButtons, Button
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d
from tkinter import filedialog
import tkinter as tk
import os

def load_data():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Open file dialog for selecting the input CSV
    file_path = filedialog.askopenfilename(
        title="Select Data CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        initialdir=os.getcwd()
    )
    
    if file_path:
        # Load data and drop rows with missing values
        df = pd.read_csv(file_path).dropna()
        
        # Print available columns to help with debugging
        print("Available columns in the CSV file:")
        print(df.columns.tolist())
        
        # Try different possible column names
        time_col = next((col for col in df.columns if 'time' in col.lower()), None)
        ankle1_col = next((col for col in df.columns if 'ankle 1' in col.lower() or 'ankle1' in col.lower()), None)
        ankle2_col = next((col for col in df.columns if 'ankle 2' in col.lower() or 'ankle2' in col.lower()), None)
        hip_col = next((col for col in df.columns if 'hip' in col.lower()), None)
        
        if not all([time_col, ankle1_col, ankle2_col, hip_col]):
            print("\nMissing required columns!")
            print(f"Looking for columns similar to: 'Time (ms)', 'Ankle 1', 'Ankle 2', 'hip'")
            print(f"Found: Time={time_col}, Ankle1={ankle1_col}, Ankle2={ankle2_col}, Hip={hip_col}")
            raise ValueError("Could not find all required columns in the CSV file")
        
        return (
            df[time_col].values / 1000,  # Convert ms to seconds
            df[ankle1_col].values,
            df[ankle2_col].values,
            df[hip_col].values
        )
    else:
        raise ValueError("No file selected")

def remove_camera_shake(ankle_signal, hip_signal):
    # The hip should ideally have minimal vertical movement
    # So we can treat hip motion as camera shake
    # Simply subtract the hip motion to stabilize the view
    stabilized_motion = ankle_signal - hip_signal

    # Optional: Smooth out any high-frequency noise
    window = 11  # Smaller window to preserve more detail
    stabilized_smooth = savgol_filter(stabilized_motion, window, 3)

    return stabilized_smooth

# Replace the data loading code with this
try:
    time, ankle1, ankle2, hip = load_data()
    
    # Process the loaded data
    ankle1_cleaned = remove_camera_shake(ankle1, hip)
    ankle2_cleaned = remove_camera_shake(ankle2, hip)
    
except ValueError as e:
    print(f"Error: {e}")
    exit()

# Create a DataFrame with the cleaned data
cleaned_data = pd.DataFrame({
    'Time (s)': time,
    'Cleaned Ankle 1': ankle1_cleaned,
    'Cleaned Ankle 2': ankle2_cleaned,
    'Original Ankle 1': ankle1,
    'Original Ankle 2': ankle2,
    'Hip Position': hip
})

# Export to a new CSV file
output_filepath = "cleaned_ankle_data.csv"
cleaned_data.to_csv(output_filepath, index=False)
print(f"Cleaned data saved to: {output_filepath}")

# Adjust the figure and subplot layout first
fig, ax = plt.subplots(figsize=(12, 8))  # Increased figure height
plt.subplots_adjust(left=0.3, bottom=0.2, top=0.9)  # Adjust margins

# Calculate frequency domain data for both ankles
freq = np.fft.fftfreq(len(time), d=(time[1]-time[0]))
ankle1_fft_clean = fft(ankle1_cleaned)
ankle2_fft_clean = fft(ankle2_cleaned)
power_clean1 = np.abs(ankle1_fft_clean)**2
power_clean2 = np.abs(ankle2_fft_clean)**2

# Modify radio button positions with proper spacing
rax1 = plt.axes([0.05, 0.75, 0.2, 0.15])  # Domain selection
radio_domain = RadioButtons(rax1, ('Time Domain', 'Frequency Domain'))

rax2 = plt.axes([0.05, 0.55, 0.2, 0.15])  # Ankle selection
radio_ankle = RadioButtons(rax2, ('Ankle 1', 'Ankle 2', 'Both Ankles'))

rax3 = plt.axes([0.05, 0.35, 0.2, 0.15])  # Data type selection
radio_data = RadioButtons(rax3, ('Both', 'Raw Only', 'Cleaned Only'))

rax4 = plt.axes([0.05, 0.15, 0.2, 0.15])  # Hip visibility (now visible)
radio_hip = RadioButtons(rax4, ('Hide Hip', 'Show Hip'))

# Add after the radio button definitions
rax5 = plt.axes([0.05, 0.02, 0.2, 0.1])  # CSV export button position
csv_button = Button(rax5, 'Export CSV')

# Add these imports if not already present
from matplotlib.widgets import Button
import matplotlib.pyplot as plt

# After creating all radio buttons and before the update_plot function, add:
rax_hide = plt.axes([0.05, 0.9, 0.2, 0.05])  # Position at top
hide_button = Button(rax_hide, 'Hide Controls')

# Create a list of all control axes
control_axes = [rax1, rax2, rax3, rax4, rax5, rax_hide]

def toggle_controls(event):
    for ax in control_axes:
        ax.set_visible(False)
    fig.canvas.draw_idle()

def show_controls(event):
    if event.dblclick:  # Only respond to double clicks
        for ax in control_axes:
            ax.set_visible(True)
        fig.canvas.draw_idle()

# Connect the button and double-click events
hide_button.on_clicked(toggle_controls)
fig.canvas.mpl_connect('button_press_event', show_controls)

def smooth_data(x, y):
    # Create interpolation function
    f = interp1d(x, y, kind='cubic', bounds_error=False, fill_value="extrapolate")
    
    # Create a denser x array for smoother plotting
    x_smooth = np.linspace(x.min(), x.max(), len(x) * 10)
    y_smooth = f(x_smooth)
    
    return x_smooth, y_smooth

def export_plot():
    # Create a new figure for export
    export_fig, export_ax = plt.subplots(figsize=(12, 8))
    
    # Get current selections
    domain = radio_domain.value_selected
    ankle = radio_ankle.value_selected
    data_type = radio_data.value_selected
    hip_visibility = radio_hip.value_selected

    if domain == 'Time Domain':
        if hip_visibility == 'Show Hip':
            time_smooth, hip_smooth = smooth_data(time, hip)
            export_ax.plot(time_smooth, hip_smooth, 'k--', alpha=0.5, label="Hip Position")

        if ankle == 'Ankle 1':
            time_smooth, ankle1_smooth = smooth_data(time, ankle1)
            time_smooth, ankle1_cleaned_smooth = smooth_data(time, ankle1_cleaned)
            
            if data_type in ['Both', 'Raw Only']:
                export_ax.plot(time_smooth, ankle1_smooth, 'b', alpha=0.5, label="Raw Ankle 1")
            if data_type in ['Both', 'Cleaned Only']:
                export_ax.plot(time_smooth, ankle1_cleaned_smooth, 'r', label="Cleaned Ankle 1")
        
        elif ankle == 'Ankle 2':
            time_smooth, ankle2_smooth = smooth_data(time, ankle2)
            time_smooth, ankle2_cleaned_smooth = smooth_data(time, ankle2_cleaned)
            
            if data_type in ['Both', 'Raw Only']:
                export_ax.plot(time_smooth, ankle2_smooth, 'b', alpha=0.5, label="Raw Ankle 2")
            if data_type in ['Both', 'Cleaned Only']:
                export_ax.plot(time_smooth, ankle2_cleaned_smooth, 'r', label="Cleaned Ankle 2")
        
        else:  # Both Ankles
            time_smooth, ankle1_smooth = smooth_data(time, ankle1)
            time_smooth, ankle1_cleaned_smooth = smooth_data(time, ankle1_cleaned)
            _, ankle2_smooth = smooth_data(time, ankle2)
            _, ankle2_cleaned_smooth = smooth_data(time, ankle2_cleaned)
            
            if data_type in ['Both', 'Raw Only']:
                export_ax.plot(time_smooth, ankle1_smooth, 'b', alpha=0.5, label="Raw Ankle 1")
                export_ax.plot(time_smooth, ankle2_smooth, 'g', alpha=0.5, label="Raw Ankle 2")
            if data_type in ['Both', 'Cleaned Only']:
                export_ax.plot(time_smooth, ankle1_cleaned_smooth, 'r', label="Cleaned Ankle 1")
                export_ax.plot(time_smooth, ankle2_cleaned_smooth, 'y', label="Cleaned Ankle 2")
        
        export_ax.set_xlabel("Time (s)")
        export_ax.set_ylabel("Position")
        export_ax.set_title(f"{ankle}: {data_type}")
        
    else:  # Frequency Domain
        if ankle == 'Ankle 1':
            export_ax.plot(freq[:len(freq)//2], power_clean1[:len(freq)//2], 'g', label="Ankle 1")
        elif ankle == 'Ankle 2':
            export_ax.plot(freq[:len(freq)//2], power_clean2[:len(freq)//2], 'g', label="Ankle 2")
        else:  # Both Ankles
            export_ax.plot(freq[:len(freq)//2], power_clean1[:len(freq)//2], 'r', label="Ankle 1")
            export_ax.plot(freq[:len(freq)//2], power_clean2[:len(freq)//2], 'b', label="Ankle 2")
        export_ax.set_xlabel("Frequency (Hz)")
        export_ax.set_ylabel("Power")
        export_ax.set_title(f"{ankle} Power Spectrum")

    # Add grid
    export_ax.grid(True, linestyle='--', alpha=0.7)
    export_ax.legend()
    
    # Save the plot
    plt.savefig('ankle_analysis.png', dpi=300, bbox_inches='tight')
    plt.close(export_fig)

def export_csv(event):
    root = tk.Tk()
    root.withdraw()
    
    # Open file dialog for saving the CSV
    save_path = filedialog.asksaveasfilename(
        title="Save Cleaned Data As",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        initialdir=os.getcwd()
    )
    
    if save_path:
        # Create a DataFrame with the cleaned data
        cleaned_data = pd.DataFrame({
            'Time (s)': time,
            'Cleaned Ankle 1': ankle1_cleaned,
            'Cleaned Ankle 2': ankle2_cleaned,
            'Original Ankle 1': ankle1,
            'Original Ankle 2': ankle2,
            'Hip Position': hip
        })
        
        # Export to the selected file
        cleaned_data.to_csv(save_path, index=False)
        print(f"Cleaned data saved to: {save_path}")

def update_plot():
    ax.clear()
    domain = radio_domain.value_selected
    ankle = radio_ankle.value_selected
    data_type = radio_data.value_selected
    hip_visibility = radio_hip.value_selected

    if domain == 'Time Domain':
        # Plot hip data if enabled
        if hip_visibility == 'Show Hip':
            time_smooth, hip_smooth = smooth_data(time, hip)
            ax.plot(time_smooth, hip_smooth, 'k--', alpha=0.5, label="Hip Position")

        if ankle == 'Ankle 1':
            # Generate smooth curves
            time_smooth, ankle1_smooth = smooth_data(time, ankle1)
            time_smooth, ankle1_cleaned_smooth = smooth_data(time, ankle1_cleaned)
            
            if data_type in ['Both', 'Raw Only']:
                ax.plot(time_smooth, ankle1_smooth, 'b', alpha=0.5, label="Raw Ankle 1")
            if data_type in ['Both', 'Cleaned Only']:
                ax.plot(time_smooth, ankle1_cleaned_smooth, 'r', label="Cleaned Ankle 1")
        
        elif ankle == 'Ankle 2':
            time_smooth, ankle2_smooth = smooth_data(time, ankle2)
            time_smooth, ankle2_cleaned_smooth = smooth_data(time, ankle2_cleaned)
            
            if data_type in ['Both', 'Raw Only']:
                ax.plot(time_smooth, ankle2_smooth, 'b', alpha=0.5, label="Raw Ankle 2")
            if data_type in ['Both', 'Cleaned Only']:
                ax.plot(time_smooth, ankle2_cleaned_smooth, 'r', label="Cleaned Ankle 2")
        
        else:  # Both Ankles
            time_smooth, ankle1_smooth = smooth_data(time, ankle1)
            time_smooth, ankle1_cleaned_smooth = smooth_data(time, ankle1_cleaned)
            _, ankle2_smooth = smooth_data(time, ankle2)
            _, ankle2_cleaned_smooth = smooth_data(time, ankle2_cleaned)
            
            if data_type in ['Both', 'Raw Only']:
                ax.plot(time_smooth, ankle1_smooth, 'b', alpha=0.5, label="Raw Ankle 1")
                ax.plot(time_smooth, ankle2_smooth, 'g', alpha=0.5, label="Raw Ankle 2")
            if data_type in ['Both', 'Cleaned Only']:
                ax.plot(time_smooth, ankle1_cleaned_smooth, 'r', label="Cleaned Ankle 1")
                ax.plot(time_smooth, ankle2_cleaned_smooth, 'y', label="Cleaned Ankle 2")
        
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Position")
        ax.set_title(f"{ankle}: {data_type}")
        ax.legend()
    
    else:  # Frequency Domain
        # Keep the frequency domain plotting as is
        if ankle == 'Ankle 1':
            ax.plot(freq[:len(freq)//2], power_clean1[:len(freq)//2], 'g', label="Ankle 1")
        elif ankle == 'Ankle 2':
            ax.plot(freq[:len(freq)//2], power_clean2[:len(freq)//2], 'g', label="Ankle 2")
        else:  # Both Ankles
            ax.plot(freq[:len(freq)//2], power_clean1[:len(freq)//2], 'r', label="Ankle 1")
            ax.plot(freq[:len(freq)//2], power_clean2[:len(freq)//2], 'b', label="Ankle 2")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Power")
        ax.set_title(f"{ankle} Power Spectrum")
        ax.legend()
    
    # Add grid to the interactive plot
    ax.grid(True, linestyle='--', alpha=0.7)
    
    fig.canvas.draw_idle()

# Initial plot
update_plot()

# Connect radio button events
radio_domain.on_clicked(lambda x: update_plot())
radio_ankle.on_clicked(lambda x: update_plot())
radio_data.on_clicked(lambda x: update_plot())
radio_hip.on_clicked(lambda x: update_plot())

# Connect the CSV export button
csv_button.on_clicked(export_csv)

# Add a keyboard shortcut for export (press 'e' to export)
def on_key(event):
    if event.key == 'e':
        export_plot()

# Connect the keyboard event
fig.canvas.mpl_connect('key_press_event', on_key)

plt.show()