import pandas as pd
import sys

# Redirect stdout to a file
sys.stdout = open('verify_fuzzy.txt', 'w', encoding='utf-8')

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 50)

def verify_fuzzy_results():
    print(f"\n{'='*20} Verifying equivalencias_farmaceuticas.xlsx {'='*20}")
    try:
        df = pd.read_excel('equivalencias_farmaceuticas.xlsx')
        print(f"Shape: {df.shape}")
        
        print("\nColumns:")
        for col in df.columns:
            print(f"  - {col}")
            
        print("\nNon-null counts:")
        print(df.count())
        
        print("\n" + "="*60)
        print("SAMPLE OF MATCHES (High Similarity)")
        print("="*60)
        # Convert similarity to float for sorting if it's string percentage
        # But let's just show head where HCM is not null
        matched = df[df['CÓDIGO HCM'].notna()]
        if not matched.empty:
            print(f"\nTotal matches: {len(matched)}")
            print("\nFirst 10 matches:")
            print(matched[['PRODUTO RHC', 'PRODUTO HCM', 'SIMILARIDADE']].head(10).to_string(index=False))
        else:
            print("No matches found.")
            
        print("\n" + "="*60)
        print("SAMPLE OF NON-MATCHES")
        print("="*60)
        non_matched = df[df['CÓDIGO HCM'].isna()]
        if not non_matched.empty:
            print(f"\nTotal non-matches: {len(non_matched)}")
            print("\nFirst 5 non-matches:")
            print(non_matched[['PRODUTO RHC']].head(5).to_string(index=False))
            
    except Exception as e:
        print(f"Error reading file: {e}")

verify_fuzzy_results()

sys.stdout.close()
