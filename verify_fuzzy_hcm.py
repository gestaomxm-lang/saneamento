import pandas as pd
import sys

# Redirect stdout to a file
sys.stdout = open('verify_fuzzy_hcm.txt', 'w', encoding='utf-8')

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 50)

def verify_fuzzy_results():
    print(f"\n{'='*20} Verifying equivalencias_farmaceuticas_hcm_base.xlsx {'='*20}")
    try:
        df = pd.read_excel('equivalencias_farmaceuticas_hcm_base.xlsx')
        print(f"Shape: {df.shape}")
        
        print("\nColumns:")
        for col in df.columns:
            print(f"  - {col}")
            
        print("\nNon-null counts:")
        print(df.count())
        
        print("\n" + "="*60)
        print("SAMPLE OF MATCHES (High Similarity)")
        print("="*60)
        matched = df[df['CÓDIGO RHC'].notna()]
        if not matched.empty:
            print(f"\nTotal matches: {len(matched)}")
            print("\nFirst 10 matches:")
            print(matched[['PRODUTO HCM', 'PRODUTO RHC', 'SIMILARIDADE']].head(10).to_string(index=False))
        else:
            print("No matches found.")
            
        print("\n" + "="*60)
        print("SAMPLE OF NON-MATCHES")
        print("="*60)
        non_matched = df[df['CÓDIGO RHC'].isna()]
        if not non_matched.empty:
            print(f"\nTotal non-matches: {len(non_matched)}")
            print("\nFirst 5 non-matches:")
            print(non_matched[['PRODUTO HCM']].head(5).to_string(index=False))
            
    except Exception as e:
        print(f"Error reading file: {e}")

verify_fuzzy_results()

sys.stdout.close()
