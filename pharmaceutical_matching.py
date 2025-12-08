"""
Pharmaceutical Fuzzy Matching Script
Matches products from base_rhc.xlsx to base_hcm.xlsx using:
- Fuzzy string matching with pharmaceutical knowledge
- Similarity thresholds
- Concentration and dosage form awareness
"""

import pandas as pd
import re
from difflib import SequenceMatcher

def normalize_pharmaceutical_text(text):
    """
    Normalize pharmaceutical product names for better matching
    """
    if pd.isna(text):
        return ""
    
    text = str(text).upper().strip()
    
    # Remove common pharmaceutical abbreviations variations
    replacements = {
        'COMP.': 'COMPRIMIDO',
        'COMP': 'COMPRIMIDO',
        'CPR': 'COMPRIMIDO',
        'AMP.': 'AMPOLA',
        'AMP': 'AMPOLA',
        'FA.': 'FRASCO',
        'FA': 'FRASCO',
        'FR.': 'FRASCO',
        'FR': 'FRASCO',
        'ENV.': 'ENVELOPE',
        'ENV': 'ENVELOPE',
        'ML.': 'ML',
        'MG.': 'MG',
        'G.': 'G',
        'C/': 'COM',
        'S/': 'SEM',
        '(*.*)': '',
        '  ': ' ',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Remove extra spaces
    text = ' '.join(text.split())
    
    return text

def extract_concentration(text):
    """
    Extract concentration/dosage from product name
    Examples: 500MG, 10ML, 2.5%, 100MG/5ML
    """
    # Pattern for concentrations like 500MG, 10ML, 2.5%, etc.
    patterns = [
        r'\d+\.?\d*\s*MG',
        r'\d+\.?\d*\s*ML',
        r'\d+\.?\d*\s*G',
        r'\d+\.?\d*\s*%',
        r'\d+\.?\d*\s*MG/\s*\d+\.?\d*\s*ML',
        r'\d+\.?\d*\s*MCG',
        r'\d+\.?\d*\s*UI',
    ]
    
    concentrations = []
    for pattern in patterns:
        matches = re.findall(pattern, text.upper())
        concentrations.extend(matches)
    
    return set(concentrations)

def calculate_similarity(text1, text2):
    """
    Calculate similarity between two pharmaceutical product names
    Returns a score between 0 and 1
    """
    # Normalize both texts
    norm1 = normalize_pharmaceutical_text(text1)
    norm2 = normalize_pharmaceutical_text(text2)
    
    # Basic sequence matching
    basic_score = SequenceMatcher(None, norm1, norm2).ratio()
    
    # Check if concentrations match
    conc1 = extract_concentration(norm1)
    conc2 = extract_concentration(norm2)
    
    concentration_penalty = 0
    if conc1 and conc2:
        # If both have concentrations, they must match
        if conc1 != conc2:
            concentration_penalty = 0.3  # Heavy penalty for different concentrations
    
    # Extract main active ingredient (usually first words before numbers)
    words1 = norm1.split()[:3]  # First 3 words
    words2 = norm2.split()[:3]
    
    # Check if main ingredient words overlap
    ingredient_overlap = len(set(words1) & set(words2)) / max(len(set(words1)), len(set(words2)), 1)
    
    # Final score combines basic similarity, concentration match, and ingredient overlap
    final_score = (basic_score * 0.5 + ingredient_overlap * 0.5) - concentration_penalty
    
    return max(0, min(1, final_score))  # Clamp between 0 and 1

def build_inverted_index(df):
    """
    Build an inverted index for faster lookup
    Token -> List of Row Indices
    """
    index = {}
    for idx, row in df.iterrows():
        name = normalize_pharmaceutical_text(row['PRODUTO'])
        tokens = set(name.split())
        for token in tokens:
            if len(token) < 3: continue # Skip short tokens
            if token not in index:
                index[token] = []
            index[token].append(idx)
    return index

def find_best_match_optimized(product_name, candidate_df, inverted_index, threshold=0.75):
    """
    Find best match using inverted index to filter candidates
    """
    norm_name = normalize_pharmaceutical_text(product_name)
    tokens = set(norm_name.split())
    
    # Get candidates that share at least one significant token
    candidate_indices = set()
    for token in tokens:
        if len(token) < 3: continue
        if token in inverted_index:
            candidate_indices.update(inverted_index[token])
    
    if not candidate_indices:
        return None, 0
        
    best_score = 0
    best_match = None
    
    # Only compare with candidates
    for idx in candidate_indices:
        candidate_row = candidate_df.iloc[idx]
        candidate_name = candidate_row['PRODUTO']
        
        # Quick length check optimization
        if abs(len(norm_name) - len(normalize_pharmaceutical_text(candidate_name))) > 10:
             # If length difference is huge, skip detailed calculation (unless it's a substring case)
             pass

        score = calculate_similarity(product_name, candidate_name)
        
        if score > best_score:
            best_score = score
            best_match = candidate_row
    
    if best_score >= threshold:
        return best_match, best_score
    else:
        return None, 0

def pharmaceutical_fuzzy_matching(threshold=0.75):
    """
    Main function to perform pharmaceutical fuzzy matching
    Base: HCM
    Lookup: RHC
    """
    print("="*60)
    print("PHARMACEUTICAL FUZZY MATCHING (HCM BASE -> RHC LOOKUP)")
    print("="*60)
    print(f"Similarity threshold: {threshold}")
    print()
    
    # Load files
    print("Loading files...")
    df_rhc = pd.read_excel('base_rhc.xlsx')
    df_hcm = pd.read_excel('base_hcm.xlsx')
    
    print(f"Loaded base_hcm: {df_hcm.shape[0]} products (BASE)")
    print(f"Loaded base_rhc: {df_rhc.shape[0]} products (LOOKUP)")
    
    # Build index for RHC (since we are looking up IN RHC)
    print("Building inverted index for RHC...")
    rhc_index = build_inverted_index(df_rhc)
    print(f"Index built with {len(rhc_index)} tokens.")
    print()
    
    # Results storage
    results = []
    matches_found = 0
    
    print("Starting matching process...")
    print()
    
    # For each HCM product, find best match in RHC
    total = len(df_hcm)
    for idx, hcm_row in df_hcm.iterrows():
        hcm_code = hcm_row['CÓDIGO']
        hcm_product = hcm_row['PRODUTO']
        
        # Find best match in RHC
        best_match, similarity = find_best_match_optimized(hcm_product, df_rhc, rhc_index, threshold)
        
        if best_match is not None:
            results.append({
                'CÓDIGO HCM': hcm_code,
                'PRODUTO HCM': hcm_product,
                'CÓDIGO RHC': best_match['CÓDIGO DO PRODUTO'],
                'PRODUTO RHC': best_match['PRODUTO'],
                'SIMILARIDADE': f"{similarity:.2%}"
            })
            matches_found += 1
            
            if matches_found <= 10:  # Show first 10 matches
                print(f"✓ Match {matches_found}:")
                print(f"  HCM: {hcm_product[:60]}")
                print(f"  RHC: {best_match['PRODUTO'][:60]}")
                print(f"  Similarity: {similarity:.2%}")
                print()
        else:
            # No match found
            results.append({
                'CÓDIGO HCM': hcm_code,
                'PRODUTO HCM': hcm_product,
                'CÓDIGO RHC': None,
                'PRODUTO RHC': None,
                'SIMILARIDADE': None
            })
        
        # Progress indicator
        if (idx + 1) % 500 == 0:
            print(f"Processed {idx + 1}/{total} products ({matches_found} matches so far)...")
    
    # Create results dataframe
    df_results = pd.DataFrame(results)
    
    # Save to Excel
    output_file = 'equivalencias_farmaceuticas_hcm_base.xlsx'
    df_results.to_excel(output_file, index=False)
    
    # Summary
    print()
    print("="*60)
    print("MATCHING SUMMARY")
    print("="*60)
    print(f"Total HCM products: {len(df_hcm)}")
    print(f"Matches found: {matches_found}")
    print(f"Match rate: {matches_found/len(df_hcm)*100:.2f}%")
    print(f"No match: {len(df_hcm) - matches_found}")
    print()
    print(f"Output file: {output_file}")
    print("="*60)

if __name__ == "__main__":
    # You can adjust the threshold here (0.0 to 1.0)
    # 0.75 = 75% similarity required
    pharmaceutical_fuzzy_matching(threshold=0.75)
