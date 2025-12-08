import streamlit as st
import pandas as pd
import unicodedata
from io import BytesIO

st.set_page_config(page_title="Create Combined Depara", layout="wide")

def normalize_text(text):
    """Normalize text for matching: remove accents, uppercase and strip whitespace."""
    if pd.isna(text):
        return ""
    s = str(text)
    # Remove accents
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    return s.strip().upper()

st.title("📊 Create Combined Depara")
st.markdown("Baseado no script `create_combined_depara.py`. Faça upload de `base_hcm` e `base_rhc` para gerar `resultado_de_para.xlsx`")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Base HCM")
    uploaded_hcm = st.file_uploader("Escolha arquivo base_hcm", type=["xlsx", "xls", "csv"], key="hcm")

with col2:
    st.subheader("📁 Base RHC")
    uploaded_rhc = st.file_uploader("Escolha arquivo base_rhc", type=["xlsx", "xls", "csv"], key="rhc")

if uploaded_hcm and uploaded_rhc:
    try:
        # Load files
        df_hcm = pd.read_excel(uploaded_hcm) if uploaded_hcm.name.endswith(('.xlsx', '.xls')) else pd.read_csv(uploaded_hcm)
        df_rhc = pd.read_excel(uploaded_rhc) if uploaded_rhc.name.endswith(('.xlsx', '.xls')) else pd.read_csv(uploaded_rhc)
        
        # Validate required columns
        required = {'CÓDIGO', 'PRODUTO'}
        missing_hcm = required - set(df_hcm.columns)
        missing_rhc = required - set(df_rhc.columns)
        
        if missing_hcm:
            st.error(f"❌ Arquivo HCM faltando colunas: {missing_hcm}")
        elif missing_rhc:
            st.error(f"❌ Arquivo RHC faltando colunas: {missing_rhc}")
        else:
            st.success("✅ Arquivos carregados com sucesso!")
            
            # Display file info
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Base HCM:** {df_hcm.shape[0]} linhas, {df_hcm.shape[1]} colunas")
                st.dataframe(df_hcm.head(3), use_container_width=True)
            with col2:
                st.write(f"**Base RHC:** {df_rhc.shape[0]} linhas, {df_rhc.shape[1]} colunas")
                st.dataframe(df_rhc.head(3), use_container_width=True)
            
            if st.button("🚀 Processar e Gerar Resultado"):
                with st.spinner("Normalizando e fazendo merge..."):
                    # Build normalized key columns
                    df_hcm_copy = df_hcm.copy()
                    df_rhc_copy = df_rhc.copy()
                    df_hcm_copy['_KEY'] = df_hcm_copy['PRODUTO'].fillna('').map(normalize_text)
                    df_rhc_copy['_KEY'] = df_rhc_copy['PRODUTO'].fillna('').map(normalize_text)
                    
                    # Merge (left join): keep all HCM rows, bring RHC code/product where match exists
                    df_rhc_small = df_rhc_copy[['_KEY', 'CÓDIGO', 'PRODUTO']].rename(columns={
                        'CÓDIGO': 'CÓDIGO RHC',
                        'PRODUTO': 'PRODUTO RHC'
                    })
                    
                    df_result = df_hcm_copy.merge(df_rhc_small, on='_KEY', how='left')
                    
                    # Compute match stats
                    total = len(df_hcm_copy)
                    matches_found = df_result['CÓDIGO RHC'].notna().sum()
                    match_rate = (matches_found / total * 100) if total > 0 else 0.0
                    
                    # Drop helper key before saving
                    if '_KEY' in df_result.columns:
                        df_result = df_result.drop(columns=['_KEY'])
                    
                    # Display stats
                    st.success("✅ Processamento concluído!")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total HCM", total)
                    with col2:
                        st.metric("Matches", int(matches_found))
                    with col3:
                        st.metric("Taxa de Match", f"{match_rate:.2f}%")
                    
                    # Preview result
                    st.subheader("👀 Primeiras linhas do resultado:")
                    st.dataframe(df_result.head(10), use_container_width=True)
                    
                    # Generate download
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_result.to_excel(writer, index=False, sheet_name='Resultado')
                    output.seek(0)
                    
                    st.download_button(
                        label="📥 Baixar resultado_de_para.xlsx",
                        data=output,
                        file_name="resultado_de_para.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
    except Exception as e:
        st.error(f"❌ Erro ao processar: {str(e)}")
else:
    st.info("👆 Faça upload dos dois arquivos para começar")

st.markdown("---")
st.markdown("**Desenvolvido com Streamlit** | Mantém a funcionalidade exata do script `create_combined_depara.py`")
