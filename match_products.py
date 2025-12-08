import pandas as pd
import unicodedata


def normalize_text(text):
    if pd.isna(text):
        return ""
    s = str(text)
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    return s.strip().upper()


def run_matching(base_de_para_path='base_de_para.xlsx', base_rhc_path='base_rhc.xlsx', output_path='base_de_para_matched.xlsx'):
    """
    Match products from `base_de_para.xlsx` to `base_rhc.xlsx` using only
    the `CÓDIGO` and `PRODUTO` columns. Produces a new file with
    `CÓDIGO RHC` and `PRODUTO RHC` appended where matches exist.
    """
    try:
        print("Loading files...")
        df_de_para = pd.read_excel(base_de_para_path)
        df_rhc = pd.read_excel(base_rhc_path)
    except Exception as e:
        print(f"Error reading input files: {e}")
        raise

    required = {'CÓDIGO', 'PRODUTO'}
    if not required.issubset(df_de_para.columns):
        missing = required - set(df_de_para.columns)
        raise KeyError(f"Missing columns in {base_de_para_path}: {missing}")
    if not required.issubset(df_rhc.columns):
        missing = required - set(df_rhc.columns)
        raise KeyError(f"Missing columns in {base_rhc_path}: {missing}")

    print(f"Loaded base_de_para: {df_de_para.shape}")
    print(f"Loaded base_rhc: {df_rhc.shape}")

    df_left = df_de_para.copy()
    df_right = df_rhc.copy()
    df_left['_KEY'] = df_left['PRODUTO'].fillna('').map(normalize_text)
    df_right['_KEY'] = df_right['PRODUTO'].fillna('').map(normalize_text)

    df_right_small = df_right[['_KEY', 'CÓDIGO', 'PRODUTO']].rename(columns={
        'CÓDIGO': 'CÓDIGO RHC',
        'PRODUTO': 'PRODUTO RHC'
    })

    df_merged = df_left.merge(df_right_small, on='_KEY', how='left')

    total = len(df_merged)
    matches = int(df_merged['CÓDIGO RHC'].notna().sum()) if total > 0 else 0
    match_rate = (matches / total * 100) if total > 0 else 0.0

    print(f"Matching completed. Found {matches} matches out of {total} rows.")
    if total > 0:
        print(f"Match rate: {match_rate:.2f}%")

    if '_KEY' in df_merged.columns:
        df_merged = df_merged.drop(columns=['_KEY'])

    try:
        print(f"Saving to {output_path}...")
        df_merged.to_excel(output_path, index=False)
        print("Done.")
    except Exception as e:
        print(f"Error saving output file: {e}")
        raise


if __name__ == "__main__":
    run_matching()
