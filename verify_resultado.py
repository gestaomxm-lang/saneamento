import pandas as pd
import sys

# Redirect stdout to a file
sys.stdout = open('resultado_verification.txt', 'w', encoding='utf-8')

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def verify_resultado():
    print(f"\n{'='*20} Verifying resultado_de_para.xlsx {'='*20}")
    try:
        df = pd.read_excel('resultado_de_para.xlsx')
        print(f"Shape: {df.shape}")
        print("\nColumns:")
        for col in df.columns:
            print(f"  - {col}")
            
        print("\nNon-null counts:")
        print(df.count())
        
        print("\n" + "="*60)
        print("SAMPLE OF MATCHED ROWS (where HCM data exists)")
        print("="*60)
        matched = df[df['CÓDIGO HCM'].notna()]
        if not matched.empty:
            print(f"\nTotal matches: {len(matched)}")
            print("\nFirst 5 matches:")
            print(matched[['PRODUTO RHC', 'CÓDIGO RHC', 'PRODUTO HCM', 'CÓDIGO HCM']].head(5).to_string(index=False))
        else:
            print("No matches found.")
            
        print("\n" + "="*60)
        print("SAMPLE OF NON-MATCHED ROWS (where HCM data is missing)")
        print("="*60)
        non_matched = df[df['CÓDIGO HCM'].isna()]
        if not non_matched.empty:
            print(f"\nTotal non-matches: {len(non_matched)}")
            print("\nFirst 3 non-matches:")
            print(non_matched[['PRODUTO RHC', 'CÓDIGO RHC']].head(3).to_string(index=False))
        else:
            print("All rows have matches.")
            
    except Exception as e:
        print(f"Error reading file: {e}")

verify_resultado()

sys.stdout.close()
