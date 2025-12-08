# Deploy Streamlit Cloud

## Arquivos Criados

- `app.py` — App Streamlit completo (replicação fiel de `create_combined_depara.py`)
- `requirements.txt` — Dependências (streamlit, pandas, openpyxl)

## Como Fazer Deploy no Streamlit Cloud

### 1. Criar Conta no Streamlit Cloud
- Acesse https://share.streamlit.io/
- Clique em "Sign up" 
- Use sua conta GitHub para autenticar (mais fácil)

### 2. Conectar Repositório GitHub
- No Streamlit Cloud, clique em "New app"
- Selecione seu repositório GitHub: `gestaomxm-lang/saneamento`
- Selecione a branch: `main`
- Selecione o arquivo app: `app.py`
- Dê um nome ao app (ex: `create-combined-depara`)

### 3. Deploy
- Clique em "Deploy"
- Aguarde ~2-3 minutos
- Seu app estará online em um link tipo: `https://create-combined-depara-<seu-id>.streamlit.app`

### 4. Usar o App
- Acesse o link gerado
- Faça upload de `base_hcm.xlsx` e `base_rhc.xlsx`
- Clique em "Processar e Gerar Resultado"
- Baixe o arquivo `resultado_de_para.xlsx`

## Características do App

✅ Interface simples e intuitiva  
✅ Replicação exata da lógica de `create_combined_depara.py`  
✅ Normaliza produtos (remove acentos, uppercase, trim)  
✅ Faz left join entre os dois arquivos  
✅ Exibe estatísticas (total, matches, taxa)  
✅ Pré-visualiza primeiras linhas do resultado  
✅ Baixa arquivo Excel com resultado  

## Rodar Localmente

```bash
streamlit run app.py
```

Acesso: `http://localhost:8501`

## Troubleshooting

**"Arquivo RHC faltando colunas: {'CÓDIGO', 'PRODUTO'}"**
- Verifique se o arquivo Excel tem as colunas exatas: `CÓDIGO` e `PRODUTO`

**Erro ao processar**
- Verifique se os arquivos estão em formato Excel (.xlsx) ou CSV
- Certifique-se que não há linhas vazias no início

## Suporte

Para dúvidas sobre o deploy, consulte: https://docs.streamlit.io/
