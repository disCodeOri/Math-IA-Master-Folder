import pandas as pd
from scipy.stats import pearsonr

def calculate_pcc(file_path):
    # Read data with duplicate headers
    df = pd.read_csv(file_path, header=0)
    df = df.dropna(how='all')  # Remove empty rows
    
    results = []
    
    # Process columns in sequential pairs (0&1, 2&3, 4&5, etc.)
    for pair_num in range(len(df.columns)//2):
        col1_idx = 2*pair_num
        col2_idx = 2*pair_num + 1
        
        # Get actual column names from CSV
        col1_name = df.columns[col1_idx]
        col2_name = df.columns[col2_idx]
        
        # Extract data pairs and clean
        pair_data = df.iloc[:,[col1_idx, col2_idx]].dropna()
        
        if len(pair_data) >= 2:
            r, p = pearsonr(pair_data.iloc[:,0], pair_data.iloc[:,1])
            results.append({
                'Comparison': f"Pair {pair_num+1} ({col1_name} vs {col2_name})",
                'PCC': round(r, 4),
                'p-value': f"{p:.2e}" if p < 0.001 else round(p, 4)
            })
    
    return pd.DataFrame(results)

# Usage:
results = calculate_pcc('pcc.csv')
print(results.to_string(index=False))
