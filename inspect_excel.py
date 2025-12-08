import pandas as pd
import sys

# Redirect stdout to a file
sys.stdout = open('verification_result.txt', 'w', encoding='utf-8')

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def verify_file(filename):
    print(f"\n{'='*20} Verifying {filename} {'='*20}")
    try:
        df = pd.read_excel(filename)
        print(f"Shape: {df.shape}")
        print("Columns:")
        for col in df.columns:
            print(f"  - {col}")
            
        print("\nNon-null counts:")
        print(df.count())
        
        print("\nSample of matched rows (where 'CÓDIGO RHC' is not null):")
        matched = df[df['CÓDIGO RHC'].notna()]
        if not matched.empty:
            print(matched[['PRODUTO', 'CÓDIGO RHC', 'PRODUTO.1']].head(5))
        else:
            print("No matches found.")
            
    except Exception as e:
        print(f"Error reading {filename}: {e}")

verify_file('base_de_para.xlsx')

sys.stdout.close()
