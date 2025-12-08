import pandas as pd
import sys

# Redirect stdout to a file
sys.stdout = open('inspect_simplified.txt', 'w', encoding='utf-8')

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def inspect_file(filename):
    print(f"\n{'='*20} Inspecting {filename} {'='*20}")
    try:
        df = pd.read_excel(filename)
        print(f"Shape: {df.shape}")
        print("Columns:")
        for col in df.columns:
            print(f"  - {col}")
        print("\nFirst 10 rows:")
        print(df.head(10))
    except Exception as e:
        print(f"Error reading {filename}: {e}")

inspect_file('base_rhc.xlsx')
inspect_file('base_hcm.xlsx')

sys.stdout.close()
