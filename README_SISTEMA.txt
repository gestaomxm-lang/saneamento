========================================
SISTEMA DE MATCHING FARMACÊUTICO
========================================

COMO USAR:

1. Dê duplo clique no arquivo "EXECUTAR_SISTEMA.bat"
   
2. Uma janela será aberta com a interface do sistema

3. Selecione os arquivos:
   - Base Padrão: Escolha o arquivo que será a base (ex: base_hcm.xlsx)
   - Base RHC: Escolha o arquivo base_rhc.xlsx

4. Configure o limiar de similaridade (recomendado: 0.75)
   - 0.75 = 75% de similaridade mínima
   - Valores maiores = matching mais rigoroso
   - Valores menores = matching mais flexível

5. Clique em "Executar Matching"

6. Aguarde o processamento (acompanhe o log)

7. Quando concluir, clique em "Abrir Resultado" para ver o arquivo Excel gerado

========================================
REQUISITOS:

- Python instalado
- Bibliotecas: pandas, openpyxl, tkinter (já vem com Python)

Se der erro de biblioteca faltando, execute:
pip install pandas openpyxl

========================================
ESTRUTURA DOS ARQUIVOS:

Os arquivos Excel devem ter 2 colunas:
- Coluna 1: CÓDIGO (ou CÓDIGO DO PRODUTO)
- Coluna 2: PRODUTO

========================================
RESULTADO:

O arquivo gerado terá 5 colunas:
- CÓDIGO BASE: Código do produto da base padrão
- PRODUTO BASE: Nome do produto da base padrão
- CÓDIGO RHC: Código do produto equivalente na RHC
- PRODUTO RHC: Nome do produto equivalente na RHC
- SIMILARIDADE: Percentual de similaridade (ex: 95.50%)

========================================
