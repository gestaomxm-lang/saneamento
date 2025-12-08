import pandas as pd
import unicodedata


def normalize_text(text):
    """Normalize text for matching: remove accents, uppercase and strip whitespace."""
    if pd.isna(text):
        return ""
    s = str(text)
    # Remove accents
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    return s.strip().upper()


def create_combined_depara(base_hcm_path='base_hcm.xlsx', base_rhc_path='base_rhc.xlsx', output_path='resultado_de_para.xlsx'):
    """
    Create a new file mapping HCM products to RHC products using only the
    `CÓDIGO` and `PRODUTO` columns in each file. The function validates the
    presence of the two columns, normalizes `PRODUTO` and performs a
    vectorized merge (left join).
    """
    try:
        print("Loading files...")
        df_hcm = pd.read_excel(base_hcm_path)
        df_rhc = pd.read_excel(base_rhc_path)
    except Exception as e:
        print(f"Error reading input files: {e}")
        raise

    # Validate required columns
    required = {'CÓDIGO', 'PRODUTO'}
    if not required.issubset(set(df_hcm.columns)):
        missing = required - set(df_hcm.columns)
        raise KeyError(f"Missing columns in {base_hcm_path}: {missing}")
    if not required.issubset(set(df_rhc.columns)):
        missing = required - set(df_rhc.columns)
        raise KeyError(f"Missing columns in {base_rhc_path}: {missing}")

    print(f"Loaded base_hcm: {df_hcm.shape}")
    print(f"Loaded base_rhc: {df_rhc.shape}")

    # Build normalized key columns
    df_hcm = df_hcm.copy()
    df_rhc = df_rhc.copy()
    df_hcm['_KEY'] = df_hcm['PRODUTO'].fillna('').map(normalize_text)
    df_rhc['_KEY'] = df_rhc['PRODUTO'].fillna('').map(normalize_text)

    # Merge (left join): keep all HCM rows, bring RHC code/product where match exists
    df_rhc_small = df_rhc[['_KEY', 'CÓDIGO', 'PRODUTO']].rename(columns={
        'CÓDIGO': 'CÓDIGO RHC',
        'PRODUTO': 'PRODUTO RHC'
    })

    df_result = df_hcm.merge(df_rhc_small, on='_KEY', how='left')

    # Compute match stats
    total = len(df_hcm)
    if total == 0:
        match_rate = 0.0
    else:
        matches_found = df_result['CÓDIGO RHC'].notna().sum()
        match_rate = matches_found / total * 100

    print("\nMatching completed!")
    print(f"Total HCM products: {total}")
    if total > 0:
        print(f"Matches found: {matches_found}")
        print(f"Match rate: {match_rate:.2f}%")

    # Drop helper key before saving
    if '_KEY' in df_result.columns:
        df_result = df_result.drop(columns=['_KEY'])

    # Save result
    try:
        print(f"\nSaving to {output_path}...")
        df_result.to_excel(output_path, index=False)
        print("Done!")
        print(f"Output file: {output_path}")
    except Exception as e:
        print(f"Error saving output file: {e}")
        raise


if __name__ == "__main__":
    create_combined_depara()
