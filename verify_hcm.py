import pandas as pd
import sys

# Redirect stdout to a file
sys.stdout = open('hcm_verification.txt', 'w', encoding='utf-8')

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def verify_hcm():
    print(f"\n{'='*20} Verifying base_hcm.xlsx {'='*20}")
    try:
        df = pd.read_excel('base_hcm.xlsx')
        print(f"Shape: {df.shape}")
        print("\nColumns:")
        for col in df.columns:
            print(f"  - {col}")
            
        print("\nNon-null counts:")
        print(df.count())
        
        print("\n" + "="*60)
        print("SAMPLE OF MATCHED ROWS")
        print("="*60)
        matched = df[df['CÓDIGO RHC'].notna()]
        if not matched.empty:
            print(f"\nTotal matches: {len(matched)}")
            print("\nFirst 5 matches:")
            print(matched[['PRODUTO', 'CÓDIGO RHC', 'PRODUTO.1']].head(5).to_string(index=False))
        else:
            print("No matches found.")
            
    except Exception as e:
        print(f"Error reading file: {e}")

verify_hcm()

sys.stdout.close()
