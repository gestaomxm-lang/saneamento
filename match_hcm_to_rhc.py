import pandas as pd
import unicodedata


def normalize_text(text):
    """Normalize text: remove accents, uppercase and strip whitespace."""
    if pd.isna(text):
        return ""
    s = str(text)
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    return s.strip().upper()


def match_hcm_to_rhc(base_hcm_path='base_hcm.xlsx', base_rhc_path='base_rhc.xlsx', output_path='base_hcm_matched.xlsx'):
    """
    Match products from `base_hcm.xlsx` to `base_rhc.xlsx` using only
    the `CÓDIGO` and `PRODUTO` columns. Produces a new file (does not
    overwrite the original) with `CÓDIGO RHC` and `PRODUTO RHC` appended
    where matches are found (exact normalized name match).
    """
    try:
        print("Loading files...")
        df_hcm = pd.read_excel(base_hcm_path)
        df_rhc = pd.read_excel(base_rhc_path)
    except Exception as e:
        print(f"Error reading input files: {e}")
        raise

    required = {'CÓDIGO', 'PRODUTO'}
    if not required.issubset(df_hcm.columns):
        missing = required - set(df_hcm.columns)
        raise KeyError(f"Missing columns in {base_hcm_path}: {missing}")
    if not required.issubset(df_rhc.columns):
        missing = required - set(df_rhc.columns)
        raise KeyError(f"Missing columns in {base_rhc_path}: {missing}")

    print(f"Loaded base_hcm: {df_hcm.shape}")
    print(f"Loaded base_rhc: {df_rhc.shape}")

    df_hcm = df_hcm.copy()
    df_rhc = df_rhc.copy()
    df_hcm['_KEY'] = df_hcm['PRODUTO'].fillna('').map(normalize_text)
    df_rhc['_KEY'] = df_rhc['PRODUTO'].fillna('').map(normalize_text)

    df_rhc_small = df_rhc[['_KEY', 'CÓDIGO', 'PRODUTO']].rename(columns={
        'CÓDIGO': 'CÓDIGO RHC',
        'PRODUTO': 'PRODUTO RHC'
    })

    df_merged = df_hcm.merge(df_rhc_small, on='_KEY', how='left')

    total = len(df_merged)
    matches = df_merged['CÓDIGO RHC'].notna().sum() if total > 0 else 0
    match_rate = (matches / total * 100) if total > 0 else 0.0

    print("Matching completed.")
    print(f"Found {matches} matches out of {total} rows.")
    if total > 0:
        print(f"Match rate: {match_rate:.2f}%")

    if '_KEY' in df_merged.columns:
        df_merged = df_merged.drop(columns=['_KEY'])

    try:
        print(f"Saving to {output_path}...")
        df_merged.to_excel(output_path, index=False)
        print("Done!")
    except Exception as e:
        print(f"Error saving output file: {e}")
        raise


if __name__ == "__main__":
    match_hcm_to_rhc()
