"""
Sistema de Matching Farmacêutico
Interface gráfica para realizar matching entre base_rhc e outra base (padrão)
Streamlit Version - Otimizado & UI Modernizada
"""

import streamlit as st
import pandas as pd
import re
from difflib import SequenceMatcher
import io
import time

# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================

# Dicionário de sinônimos movido para escopo global para evitar recriação
PHARMACEUTICAL_SYNONYMS = {
    # === PRINCÍPIOS ATIVOS ===
    'CLAV': 'CLAVULANATO', 'CLAVUL': 'CLAVULANATO',
    'AMOX': 'AMOXICILINA', 'AMOXILINA': 'AMOXICILINA', 'AMOXI': 'AMOXICILINA',
    'AC.': 'ACIDO', 'AC ': 'ACIDO ',
    'ACETILSAL': 'ACETILSALICILICO', 'ASS': 'ACETILSALICILICO', 'AAS': 'ACETILSALICILICO',
    'DIPIR': 'DIPIRONA', 'PARACET': 'PARACETAMOL', 'IBUPRO': 'IBUPROFENO',
    'CEFALEX': 'CEFALEXINA', 'AZITRO': 'AZITROMICINA', 'CLARITRO': 'CLARITROMICINA',
    'METFORM': 'METFORMINA', 'ATENOL': 'ATENOLOL', 'CAPTOP': 'CAPTOPRIL',
    'ENALAPRIL': 'ENALAPRIL', 'LOSART': 'LOSARTANA', 'SINVAST': 'SINVASTATINA',
    'ATORVAST': 'ATORVASTATINA', 'OMEPRAZ': 'OMEPRAZOL', 'PANTOPRAZ': 'PANTOPRAZOL',
    'RANITID': 'RANITIDINA',
    
    # === SAIS E COMPOSTOS ===
    'SODICO': 'SODIO', 'POTASSICO': 'POTASSIO', 'CALCICO': 'CALCIO',
    'CLORIDRATO': 'HCL', 'SULFATO': 'SO4', 'FOSFATO': 'PO4',
    
    # === FORMAS FARMACÊUTICAS ===
    'COMP.': 'COMPRIMIDO', 'COMP ': 'COMPRIMIDO ', 'COMPR': 'COMPRIMIDO', 'CPR': 'COMPRIMIDO',
    'CAPS': 'CAPSULA', 'CAP': 'CAPSULA',
    'AMP.': 'AMPOLA', 'AMP ': 'AMPOLA ', 'AMPOLA': 'AMPOLA',
    'FA.': 'FRASCO', 'FA ': 'FRASCO ', 'FR.': 'FRASCO', 'FR ': 'FRASCO ', 'FRASCO': 'FRASCO',
    'ENV.': 'ENVELOPE', 'ENV ': 'ENVELOPE ',
    'SOL.': 'SOLUCAO', 'SOL ': 'SOLUCAO ',
    'SUSP.': 'SUSPENSAO', 'SUSP ': 'SUSPENSAO ',
    'XPE': 'XAROPE', 'XAROPE': 'XAROPE',
    'POM': 'POMADA', 'CREME': 'CREME', 'GEL': 'GEL',
    'SPRAY': 'SPRAY', 'AEROSOL': 'AEROSOL', 'GOTAS': 'GOTAS', 'COLIR': 'COLIRIO',
    
    # === UNIDADES DE MEDIDA ===
    'GR ': 'G ', 'GR)': 'G)', 'GRS': 'G', 'GRAMA': 'G', 'GRAMAS': 'G',
    'ML.': 'ML', 'MG.': 'MG', 'G.': 'G', 'MCG': 'MCG', 'MICROG': 'MCG',
    'UI': 'UI', 'UNIDADES': 'UI', '%': 'PORCENTO',
    
    # === OUTROS MAPPINGS ===
    'VO': 'ORAL', 'IV': 'INTRAVENOSO', 'IM': 'INTRAMUSCULAR',
    'SC': 'SUBCUTANEO', 'TOP': 'TOPICO',
    'C/': 'COM', 'S/': 'SEM',
    ' DE ': ' ', ' DA ': ' ', ' DO ': ' ', ' PARA ': ' ',
    '(*.*)': '', '*': '', '+': ' ', '-': ' ', '/': ' ', '(': '', ')': '', '[': '', ']': '',
}

CONCENTRATION_PATTERNS = [
    r'\d+\.?\d*\s*MG', r'\d+\.?\d*\s*ML', r'\d+\.?\d*\s*G',
    r'\d+\.?\d*\s*%', r'\d+\.?\d*\s*MG/\s*\d+\.?\d*\s*ML',
    r'\d+\.?\d*\s*MCG', r'\d+\.?\d*\s*UI',
]

# =============================================================================
# CORE LOGIC FUNCTIONS
# =============================================================================

def normalize_pharmaceutical_text(text):
    if pd.isna(text):
        return ""
    
    text = str(text).upper().strip()
    
    for old, new in PHARMACEUTICAL_SYNONYMS.items():
        text = text.replace(old, new)
    text = ' '.join(text.split())
    return text

def extract_concentration(text):
    concentrations = []
    text_upper = text.upper()
    for pattern in CONCENTRATION_PATTERNS:
        matches = re.findall(pattern, text_upper)
        concentrations.extend(matches)
    return set(concentrations)

def extract_brand_name(text):
    match = re.search(r'\(([A-Z]+)\)', text.upper())
    if match:
        return match.group(1)
    return None

def normalize_concentrations(concentrations):
    normalized = set()
    for conc in concentrations:
        conc_norm = (
            conc.replace(' ', '')
            .replace('GR', 'G')
            .replace('GRAMA', 'G')
            .replace('GRAMAS', 'G')
        )
        normalized.add(conc_norm)
    return normalized

def preprocess_item(idx, text, row_data):
    """
    Pre-computes all features needed for matching for a single item.
    Returns a dictionary of features.
    """
    norm_text = normalize_pharmaceutical_text(text)
    
    # Concentrations
    raw_concs = extract_concentration(text)
    norm_concs = normalize_concentrations(raw_concs) if raw_concs else set()
    
    # Brand
    brand = extract_brand_name(text)
    
    # Tokens (for indexing) and First 5 words (for active ingredient check)
    tokens = set(norm_text.split())
    words_5 = norm_text.split()[:5]
    
    return {
        'id': idx,
        'original': text,
        'norm': norm_text,
        'concs': norm_concs,
        'brand': brand,
        'tokens': tokens,
        'words_5': set(words_5), # Use set for faster intersection O(1) vs O(N)
        'words_5_len': max(len(set(words_5)), 1),
        'row': row_data # Store the full row data for result retrieval
    }

# Cache the heavy lifting of processing the RHC base
@st.cache_data(show_spinner=False)
def preprocess_rhc_base(df):
    
    if 'PRODUTO' in df.columns:
        product_col = 'PRODUTO'
        code_col = df.columns[0]
    else:
        product_col = df.columns[1]
        code_col = df.columns[0]
        
    processed_items = []
    inverted_index = {}
    
    for idx, row in df.iterrows():
        item = preprocess_item(idx, row[product_col], row)
        # Store essential result fields cleanly
        item['result_code'] = row[code_col]
        item['result_prod'] = row[product_col]
        
        processed_items.append(item)
        
        # Build Index
        for token in item['tokens']:
            if len(token) < 3: continue
            if token not in inverted_index:
                inverted_index[token] = []
            inverted_index[token].append(idx) # Store index in the list
            
    return processed_items, inverted_index

def calculate_similarity_fast(input_item, candidate_item):
    """
    Calculates similarity using pre-computed features. 
    Much faster than the original function.
    """
    # 1. Basic Sequence Matcher (still needed, but on cached normalized strings)
    # Using quick_ratio() first can be an optimization, but .ratio() is robust
    basic_score = SequenceMatcher(None, input_item['norm'], candidate_item['norm']).ratio()
    
    # 2. Concentrations
    concentration_penalty = 0
    concentration_bonus = 0
    
    if input_item['concs'] and candidate_item['concs']:
        if input_item['concs'] == candidate_item['concs']:
            concentration_bonus = 0.15
        else:
            concentration_penalty = 0.15
            
    # 3. Active Ingredient (Word Overlap)
    # Using pre-computed sets
    intersection = len(input_item['words_5'] & candidate_item['words_5'])
    # Denom needs max length, we stored input's length, check candidate
    max_len = max(input_item['words_5_len'], candidate_item['words_5_len'])
    ingredient_overlap = intersection / max_len
    
    # 4. Brand
    brand_bonus = 0
    if input_item['brand'] and candidate_item['brand'] and input_item['brand'] == candidate_item['brand']:
        brand_bonus = 0.2
        
    final_score = (
        (basic_score * 0.35) + 
        (ingredient_overlap * 0.65) + 
        concentration_bonus + 
        brand_bonus - 
        concentration_penalty
    )
    
    return max(0, min(1, final_score))

def validate_columns(df):
    """
    Validates if the DataFrame has exactly 2 columns and normalizes headers.
    Renames 'CÓDIGO DO PRODUTO' -> 'CÓDIGO', etc.
    """
    # Check column count
    if len(df.columns) != 2:
        raise ValueError(f"O arquivo deve ter exatamente 2 colunas. Encontrado: {len(df.columns)} colunas.")
        
    # Check column names (Flexible)
    cols = [str(c).upper().strip() for c in df.columns]
    
    # Map common variations to standard
    replacements = {
        'CÓDIGO DO PRODUTO': 'CÓDIGO',
        'CODIGO DO PRODUTO': 'CÓDIGO',
        'CODIGO': 'CÓDIGO',
        'COD': 'CÓDIGO',
        'DESCRIÇÃO': 'PRODUTO',
        'DESCRICAO': 'PRODUTO',
        'NOME': 'PRODUTO'
    }
    
    new_cols = []
    for c in cols:
        new_cols.append(replacements.get(c, c))
        
    df.columns = new_cols
    
    # Final check - warn but don't crash if different, allowing user to proceed if 2 cols exist
    # (User asked to remove restriction, so we'll trust the 2-column structure is enough for logic)
    
    return True

# =============================================================================
# STREAMLIT APP
# =============================================================================

def main():
    st.set_page_config(page_title="Sistema de Matching", page_icon="favicon.png", layout="centered")

    # Session State Initialization (Must be first)
    if 'results' not in st.session_state:
        st.session_state['results'] = None
    if 'processing_complete' not in st.session_state:
        st.session_state['processing_complete'] = False
    if 'uploader_key' not in st.session_state:
        st.session_state['uploader_key'] = 0

    # Custom CSS
    st.markdown("""
        <style>
        .stApp { background-color: #ECEFF4; }
        .main-header { color: #001A72; text-align: center; }
        .stButton>button {
            background-color: #E87722; color: white; border: none;
        }
        .stButton>button:hover {
            background-color: #d66a1a; color: white;
        }
        h1, h2, h3 { color: #001A72 !important; }
        
        /* File Uploader Clean Style */
        [data-testid="stFileUploader"] { padding-top: 5px; padding-bottom: 5px; }
        button[kind="secondary"] {
            background-color: #E87722 !important; color: white !important; border: none !important; width: 100%;
        }
        [data-testid="stFileUploader"] small { color: transparent; display: none; }
        </style>
    """, unsafe_allow_html=True)

    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try: st.image("logo.png", use_container_width=True)
        except: pass

    st.markdown("<h1 style='text-align: center; color: #001A72;'>Sistema de Auxílio para Saneamento da Base de Dados RHC</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555;'>Identificação automática de equivalência de produtos</p>", unsafe_allow_html=True)
    st.divider()

    # Uploads
    st.markdown("### 1. Upload dos Arquivos")
    
    # Instructions
    st.info("""
        **Padrão Obrigatório:** As planilhas devem conter **exatamente duas colunas** nesta ordem:
        1. **CÓDIGO**
        2. **PRODUTO**
        
        Arquivos fora deste padrão não serão processados.
    """, icon="ℹ️")

    upload_container = st.container(border=True)
    with upload_container:
        col1, col2 = st.columns(2)
        with col1:
            uploaded_base = st.file_uploader(
                "Base Atual Unidade (.xlsx)", 
                type=["xlsx"],
                key=f"base_{st.session_state.uploader_key}"
            )
            if uploaded_base: st.markdown(f"<small>✅ {uploaded_base.name}</small>", unsafe_allow_html=True)
        with col2:
            uploaded_rhc = st.file_uploader(
                "Base RHC (.xlsx)", 
                type=["xlsx"],
                key=f"rhc_{st.session_state.uploader_key}"
            )
            if uploaded_rhc: st.markdown(f"<small>✅ {uploaded_rhc.name}</small>", unsafe_allow_html=True)



    # Execution
    st.markdown("### 2. Processamento")
    
    if uploaded_base and uploaded_rhc:
        # Check if we need to process (Button click)
        if st.button("▶️ Executar Matching", type="primary", use_container_width=True):
            
            status = st.container(border=True)
            status.markdown("**Status do Processamento**")
            log = status.empty()
            pbar = status.progress(0)
            
            try:
                # 1. Load Data
                log.text("📂 Lendo arquivos Excel...")
                df_base = pd.read_excel(uploaded_base)
                
                # Validation Base
                validate_columns(df_base)
                
                df_rhc = pd.read_excel(uploaded_rhc)
                
                # Validation RHC
                validate_columns(df_rhc)
                
                # 2. Pre-process RHC (Heavy lifting, optimized & cached)
                log.text("⚙️ Otimizando Base RHC (Indexação)...")
                rhc_items, rhc_index = preprocess_rhc_base(df_rhc)
                
                results = []
                matches_found = 0
                total = len(df_base)
                THRESHOLD = 0.75
                
                # Identifica colunas da Base Input
                col_code = df_base.columns[0]
                col_prod = df_base.columns[1]

                # 3. Matching Loop
                start_time = time.time()
                log.text("🔍 Iniciando busca de similaridade...")
                
                for idx, row in df_base.iterrows():
                    
                    # Preprocess Single Input Item
                    input_text = row[col_prod]
                    input_item = preprocess_item(idx, input_text, row)
                    
                    # Find candidates via index
                    candidate_indices = set()
                    for token in input_item['tokens']:
                        if len(token) < 3: continue
                        if token in rhc_index:
                            candidate_indices.update(rhc_index[token])
                    
                    best_match = None
                    best_score = 0
                    
                    if candidate_indices:
                        # Scan only candidates
                        for cand_idx in candidate_indices:
                            cand_item = rhc_items[cand_idx] # Direct access via list index
                            
                            score = calculate_similarity_fast(input_item, cand_item)
                            
                            if score > best_score:
                                best_score = score
                                best_match = cand_item
                    
                    # Result Decision
                    res_entry = {
                        'CÓDIGO BASE': row[col_code],
                        'PRODUTO BASE': input_text,
                        'CÓDIGO RHC': None,
                        'PRODUTO RHC': None,
                        'SIMILARIDADE': None
                    }
                    
                    if best_score >= THRESHOLD and best_match:
                        res_entry['CÓDIGO RHC'] = best_match['result_code']
                        res_entry['PRODUTO RHC'] = best_match['result_prod']
                        res_entry['SIMILARIDADE'] = f"{best_score:.2%}"
                        matches_found += 1
                        
                    results.append(res_entry)
                    
                    # UI Update (Throttled for performance)
                    if idx % 50 == 0 or idx == total - 1:
                        prog = (idx + 1) / total
                        pbar.progress(prog)
                        rate = (idx + 1) / (time.time() - start_time)
                        log.markdown(f"⚡ Processando: **{idx+1}/{total}** | Velocidade: {rate:.1f} itens/seg")

                # 4. Finalize
                df_results = pd.DataFrame(results)
                # Ensure column order
                cols_order = ['CÓDIGO BASE', 'PRODUTO BASE', 'CÓDIGO RHC', 'PRODUTO RHC', 'SIMILARIDADE']
                df_results = df_results[cols_order]
                
                log.markdown(f"✅ **Concluído!** {matches_found} matches em {time.time() - start_time:.1f}s")
                pbar.progress(1.0)
                
                # Store in session state
                st.session_state['results'] = df_results
                st.session_state['processing_complete'] = True
                st.session_state['total'] = total
                st.session_state['matches'] = matches_found
                st.rerun()

            except Exception as e:
                st.error(f"Erro durante o processamento: {e}")

    else:
        st.info("👆 Anexe as planilhas para começar.")

    # 3. Results Display (Persistent)
    if st.session_state.get('processing_complete') and st.session_state.get('results') is not None:
        
        st.divider()
        st.markdown("### 3. Resultados")
        
        df_results = st.session_state['results']
        total = st.session_state['total']
        matches_found = st.session_state['matches']
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total de Itens", total)
        m2.metric("Matches Encontrados", matches_found)
        m3.metric("Eficiência", f"{matches_found/total*100:.1f}%")
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_results.to_excel(writer, index=False, sheet_name='Resultado')
        
        st.download_button(
            "📥 BAIXAR RESULTADO (XLSX)",
            data=output.getvalue(),
            file_name="resultado_matching_otimizado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )
        
        if st.button("🔄 Nova Análise"):
            # Clear state
            st.session_state['results'] = None
            st.session_state['processing_complete'] = False
            # Increment key to reset file uploaders
            st.session_state['uploader_key'] += 1
            st.rerun()

if __name__ == "__main__":
    main()
