"""
Sistema de Matching Farmacêutico
Interface gráfica para realizar matching entre base_rhc e outra base (padrão)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import re
from difflib import SequenceMatcher
import threading
import os

class SistemaMatchingFarmaceutico:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Matching Farmacêutico")
        self.root.geometry("800x600")
        
        # Variables
        self.arquivo_base_padrao = tk.StringVar()
        self.arquivo_rhc = tk.StringVar(value="base_rhc.xlsx")
        self.threshold = tk.DoubleVar(value=0.75)
        self.output_file = tk.StringVar(value="equivalencias_resultado.xlsx")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="🔬 Sistema de Matching Farmacêutico", 
                              font=("Arial", 16, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(pady=15)
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection section
        file_frame = tk.LabelFrame(main_frame, text="📁 Seleção de Arquivos", 
                                  font=("Arial", 10, "bold"), padx=10, pady=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Base padrão (HCM ou outra)
        tk.Label(file_frame, text="Base Padrão (ex: base_hcm.xlsx):").grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Entry(file_frame, textvariable=self.arquivo_base_padrao, width=50).grid(row=0, column=1, padx=5)
        tk.Button(file_frame, text="Procurar...", command=self.selecionar_base_padrao).grid(row=0, column=2)
        
        # Base RHC
        tk.Label(file_frame, text="Base RHC:").grid(row=1, column=0, sticky=tk.W, pady=5)
        tk.Entry(file_frame, textvariable=self.arquivo_rhc, width=50).grid(row=1, column=1, padx=5)
        tk.Button(file_frame, text="Procurar...", command=self.selecionar_rhc).grid(row=1, column=2)
        
        # Settings section
        settings_frame = tk.LabelFrame(main_frame, text="⚙️ Configurações", 
                                      font=("Arial", 10, "bold"), padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(settings_frame, text="Limiar de Similaridade (0.0 - 1.0):").grid(row=0, column=0, sticky=tk.W, pady=5)
        threshold_spinbox = tk.Spinbox(settings_frame, from_=0.0, to=1.0, increment=0.05, 
                                      textvariable=self.threshold, width=10)
        threshold_spinbox.grid(row=0, column=1, sticky=tk.W, padx=5)
        tk.Label(settings_frame, text="(Recomendado: 0.75)").grid(row=0, column=2, sticky=tk.W)
        
        tk.Label(settings_frame, text="Nome do arquivo de saída:").grid(row=1, column=0, sticky=tk.W, pady=5)
        tk.Entry(settings_frame, textvariable=self.output_file, width=40).grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=5)
        
        # Action buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.btn_executar = tk.Button(button_frame, text="▶️ Executar Matching", 
                                      command=self.executar_matching, 
                                      bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
                                      padx=20, pady=10)
        self.btn_executar.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="📂 Abrir Resultado", 
                 command=self.abrir_resultado,
                 bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                 padx=20, pady=10).pack(side=tk.LEFT, padx=5)
        
        # Log section
        log_frame = tk.LabelFrame(main_frame, text="📋 Log de Execução", 
                                 font=("Arial", 10, "bold"), padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(10, 0))
        
    def selecionar_base_padrao(self):
        filename = filedialog.askopenfilename(
            title="Selecionar Base Padrão",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if filename:
            self.arquivo_base_padrao.set(filename)
            
    def selecionar_rhc(self):
        filename = filedialog.askopenfilename(
            title="Selecionar Base RHC",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if filename:
            self.arquivo_rhc.set(filename)
            
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def executar_matching(self):
        # Validate inputs
        if not self.arquivo_base_padrao.get():
            messagebox.showerror("Erro", "Por favor, selecione a Base Padrão!")
            return
            
        if not self.arquivo_rhc.get():
            messagebox.showerror("Erro", "Por favor, selecione a Base RHC!")
            return
            
        # Run in thread to avoid freezing UI
        thread = threading.Thread(target=self._executar_matching_thread)
        thread.daemon = True
        thread.start()
        
    def _executar_matching_thread(self):
        try:
            self.btn_executar.config(state=tk.DISABLED)
            self.progress.start()
            self.log_text.delete(1.0, tk.END)
            
            self.log("="*60)
            self.log("INICIANDO MATCHING FARMACÊUTICO")
            self.log("="*60)
            self.log(f"Base Padrão: {os.path.basename(self.arquivo_base_padrao.get())}")
            self.log(f"Base RHC: {os.path.basename(self.arquivo_rhc.get())}")
            self.log(f"Limiar: {self.threshold.get()}")
            self.log("")
            
            # Load files
            self.log("Carregando arquivos...")
            df_base = pd.read_excel(self.arquivo_base_padrao.get())
            df_rhc = pd.read_excel(self.arquivo_rhc.get())
            
            self.log(f"✓ Base Padrão: {df_base.shape[0]} produtos")
            self.log(f"✓ Base RHC: {df_rhc.shape[0]} produtos")
            self.log("")
            
            # Build index
            self.log("Construindo índice invertido...")
            rhc_index = self.build_inverted_index(df_rhc)
            self.log(f"✓ Índice criado com {len(rhc_index)} tokens")
            self.log("")
            
            # Perform matching
            self.log("Iniciando processo de matching...")
            results = []
            matches_found = 0
            total = len(df_base)
            
            for idx, row in df_base.iterrows():
                # Get column names dynamically
                codigo_col = df_base.columns[0]  # First column is code
                produto_col = df_base.columns[1]  # Second column is product
                
                codigo = row[codigo_col]
                produto = row[produto_col]
                
                # Find match
                best_match, similarity = self.find_best_match_optimized(
                    produto, df_rhc, rhc_index, self.threshold.get()
                )
                
                if best_match is not None:
                    results.append({
                        'CÓDIGO BASE': codigo,
                        'PRODUTO BASE': produto,
                        'CÓDIGO RHC': best_match['CÓDIGO DO PRODUTO'],
                        'PRODUTO RHC': best_match['PRODUTO'],
                        'SIMILARIDADE': f"{similarity:.2%}"
                    })
                    matches_found += 1
                else:
                    results.append({
                        'CÓDIGO BASE': codigo,
                        'PRODUTO BASE': produto,
                        'CÓDIGO RHC': None,
                        'PRODUTO RHC': None,
                        'SIMILARIDADE': None
                    })
                
                # Progress update
                if (idx + 1) % 500 == 0:
                    self.log(f"Processado {idx + 1}/{total} produtos ({matches_found} matches)...")
            
            # Save results
            df_results = pd.DataFrame(results)
            output_path = self.output_file.get()
            df_results.to_excel(output_path, index=False)
            
            # Summary
            self.log("")
            self.log("="*60)
            self.log("RESUMO DO MATCHING")
            self.log("="*60)
            self.log(f"Total de produtos processados: {total}")
            self.log(f"Matches encontrados: {matches_found}")
            self.log(f"Taxa de match: {matches_found/total*100:.2f}%")
            self.log(f"Sem correspondência: {total - matches_found}")
            self.log("")
            self.log(f"✓ Arquivo salvo: {output_path}")
            self.log("="*60)
            
            messagebox.showinfo("Sucesso!", 
                              f"Matching concluído!\n\n"
                              f"Matches: {matches_found}/{total} ({matches_found/total*100:.1f}%)\n"
                              f"Arquivo: {output_path}")
            
        except Exception as e:
            self.log(f"\n❌ ERRO: {str(e)}")
            messagebox.showerror("Erro", f"Erro durante o matching:\n{str(e)}")
        finally:
            self.progress.stop()
            self.btn_executar.config(state=tk.NORMAL)
    
    def normalize_pharmaceutical_text(self, text):
        if pd.isna(text):
            return ""
        
        text = str(text).upper().strip()
        
        # Dicionário EXPANDIDO de sinônimos farmacêuticos (conhecimento de farmacêutico)
        pharmaceutical_synonyms = {
            # === PRINCÍPIOS ATIVOS - Abreviações e Variações ===
            'CLAV': 'CLAVULANATO',
            'CLAVUL': 'CLAVULANATO',
            'AMOX': 'AMOXICILINA',
            'AMOXILINA': 'AMOXICILINA',
            'AMOXI': 'AMOXICILINA',
            'AC.': 'ACIDO',
            'AC ': 'ACIDO ',
            'ACETILSAL': 'ACETILSALICILICO',
            'ASS': 'ACETILSALICILICO',
            'AAS': 'ACETILSALICILICO',
            'DIPIR': 'DIPIRONA',
            'PARACET': 'PARACETAMOL',
            'IBUPRO': 'IBUPROFENO',
            'CEFALEX': 'CEFALEXINA',
            'AZITRO': 'AZITROMICINA',
            'CLARITRO': 'CLARITROMICINA',
            'METFORM': 'METFORMINA',
            'ATENOL': 'ATENOLOL',
            'CAPTOP': 'CAPTOPRIL',
            'ENALAPRIL': 'ENALAPRIL',
            'LOSART': 'LOSARTANA',
            'SINVAST': 'SINVASTATINA',
            'ATORVAST': 'ATORVASTATINA',
            'OMEPRAZ': 'OMEPRAZOL',
            'PANTOPRAZ': 'PANTOPRAZOL',
            'RANITID': 'RANITIDINA',
            
            # === SAIS E COMPOSTOS ===
            'SODICO': 'SODIO',
            'POTASSICO': 'POTASSIO',
            'CALCICO': 'CALCIO',
            'CLORIDRATO': 'HCL',
            'SULFATO': 'SO4',
            'FOSFATO': 'PO4',
            
            # === FORMAS FARMACÊUTICAS ===
            'COMP.': 'COMPRIMIDO',
            'COMP ': 'COMPRIMIDO ',
            'COMPR': 'COMPRIMIDO',
            'CPR': 'COMPRIMIDO',
            'CAPS': 'CAPSULA',
            'CAP': 'CAPSULA',
            'AMP.': 'AMPOLA',
            'AMP ': 'AMPOLA ',
            'AMPOLA': 'AMPOLA',
            'FA.': 'FRASCO',
            'FA ': 'FRASCO ',
            'FR.': 'FRASCO',
            'FR ': 'FRASCO ',
            'FRASCO': 'FRASCO',
            'ENV.': 'ENVELOPE',
            'ENV ': 'ENVELOPE ',
            'SOL.': 'SOLUCAO',
            'SOL ': 'SOLUCAO ',
            'SUSP.': 'SUSPENSAO',
            'SUSP ': 'SUSPENSAO ',
            'XPE': 'XAROPE',
            'XAROPE': 'XAROPE',
            'POM': 'POMADA',
            'CREME': 'CREME',
            'GEL': 'GEL',
            'SPRAY': 'SPRAY',
            'AEROSOL': 'AEROSOL',
            'GOTAS': 'GOTAS',
            'COLIR': 'COLIRIO',
            
            # === UNIDADES DE MEDIDA - Normalizar ===
            'GR ': 'G ',
            'GR)': 'G)',
            'GRS': 'G',
            'GRAMA': 'G',
            'GRAMAS': 'G',
            'ML.': 'ML',
            'MG.': 'MG',
            'G.': 'G',
            'MCG': 'MCG',
            'MICROG': 'MCG',
            'UI': 'UI',
            'UNIDADES': 'UI',
            '%': 'PORCENTO',
            
            # === VIAS DE ADMINISTRAÇÃO ===
            'VO': 'ORAL',
            'IV': 'INTRAVENOSO',
            'IM': 'INTRAMUSCULAR',
            'SC': 'SUBCUTANEO',
            'TOP': 'TOPICO',
            
            # === PREPOSIÇÕES E CONECTORES (remover) ===
            'C/': 'COM',
            'S/': 'SEM',
            ' DE ': ' ',
            ' DA ': ' ',
            ' DO ': ' ',
            ' PARA ': ' ',
            
            # === CARACTERES ESPECIAIS ===
            '(*.*)': '',
            '*': '',
            '+': ' ',
            '-': ' ',
            '/': ' ',
            '(': '',
            ')': '',
            '[': '',
            ']': '',
        }
        
        # Aplicar substituições em ordem (importantes primeiro)
        for old, new in pharmaceutical_synonyms.items():
            text = text.replace(old, new)
        
        # Remover espaços extras
        text = ' '.join(text.split())
        
        return text
    
    def extract_concentration(self, text):
        patterns = [
            r'\d+\.?\d*\s*MG', r'\d+\.?\d*\s*ML', r'\d+\.?\d*\s*G',
            r'\d+\.?\d*\s*%', r'\d+\.?\d*\s*MG/\s*\d+\.?\d*\s*ML',
            r'\d+\.?\d*\s*MCG', r'\d+\.?\d*\s*UI',
        ]
        
        concentrations = []
        for pattern in patterns:
            matches = re.findall(pattern, text.upper())
            concentrations.extend(matches)
        
        return set(concentrations)
    
    def calculate_similarity(self, text1, text2):
        """Calcula similaridade com lógica farmacêutica avançada"""
        norm1 = self.normalize_pharmaceutical_text(text1)
        norm2 = self.normalize_pharmaceutical_text(text2)
        
        # 1. Similaridade básica de sequência
        basic_score = SequenceMatcher(None, norm1, norm2).ratio()
        
        # 2. Verificar concentrações (CRÍTICO para farmacêuticos)
        conc1 = self.extract_concentration(text1)  # Usar texto original
        conc2 = self.extract_concentration(text2)
        
        concentration_penalty = 0
        concentration_bonus = 0
        
        if conc1 and conc2:
            # Normalizar concentrações para comparação
            conc1_normalized = self.normalize_concentrations(conc1)
            conc2_normalized = self.normalize_concentrations(conc2)
            
            if conc1_normalized == conc2_normalized:
                # BÔNUS se concentrações são iguais (forte indicador de equivalência)
                concentration_bonus = 0.15  # Aumentado de 0.1 para 0.15
            else:
                # PENALIDADE REDUZIDA se concentrações são diferentes
                concentration_penalty = 0.15  # Reduzido de 0.35 para 0.15
        
        # 3. Análise de princípio ativo (primeiras 3-5 palavras)
        words1 = norm1.split()[:5]
        words2 = norm2.split()[:5]
        
        # Overlap de palavras do princípio ativo
        ingredient_overlap = len(set(words1) & set(words2)) / max(len(set(words1)), len(set(words2)), 1)
        
        # 4. Verificar se há nome comercial comum (entre parênteses)
        brand1 = self.extract_brand_name(text1)
        brand2 = self.extract_brand_name(text2)
        brand_bonus = 0
        
        if brand1 and brand2 and brand1 == brand2:
            # BÔNUS se mesmo nome comercial (ex: CLAVULIN)
            brand_bonus = 0.2  # Aumentado de 0.15 para 0.2
        
        # 5. CÁLCULO FINAL com pesos farmacêuticos AJUSTADOS
        # - Ingrediente ativo é MAIS importante (65%)
        # - Sequência exata é menos importante (35%)
        # - Bônus/penalidades de concentração e marca
        final_score = (
            (basic_score * 0.35) + 
            (ingredient_overlap * 0.65) + 
            concentration_bonus + 
            brand_bonus - 
            concentration_penalty
        )
        
        return max(0, min(1, final_score))
    
    def extract_brand_name(self, text):
        """Extrai nome comercial entre parênteses"""
        import re
        match = re.search(r'\(([A-Z]+)\)', text.upper())
        if match:
            return match.group(1)
        return None
    
    def normalize_concentrations(self, concentrations):
        """Normaliza concentrações para comparação (ex: 1GR = 1G)"""
        normalized = set()
        for conc in concentrations:
            # Remover espaços e normalizar variações
            conc_norm = (
                conc.replace(' ', '')
                .replace('GR', 'G')
                .replace('GRAMA', 'G')
                .replace('GRAMAS', 'G')
            )
            normalized.add(conc_norm)
        return normalized
    
    def build_inverted_index(self, df):
        index = {}
        for idx, row in df.iterrows():
            name = self.normalize_pharmaceutical_text(row['PRODUTO'])
            tokens = set(name.split())
            for token in tokens:
                if len(token) < 3:
                    continue
                if token not in index:
                    index[token] = []
                index[token].append(idx)
        return index
    
    def find_best_match_optimized(self, product_name, candidate_df, inverted_index, threshold):
        norm_name = self.normalize_pharmaceutical_text(product_name)
        tokens = set(norm_name.split())
        
        candidate_indices = set()
        for token in tokens:
            if len(token) < 3:
                continue
            if token in inverted_index:
                candidate_indices.update(inverted_index[token])
        
        if not candidate_indices:
            return None, 0
        
        best_score = 0
        best_match = None
        
        for idx in candidate_indices:
            candidate_row = candidate_df.iloc[idx]
            candidate_name = candidate_row['PRODUTO']
            score = self.calculate_similarity(product_name, candidate_name)
            
            if score > best_score:
                best_score = score
                best_match = candidate_row
        
        if best_score >= threshold:
            return best_match, best_score
        else:
            return None, 0
    
    def abrir_resultado(self):
        output_path = self.output_file.get()
        if os.path.exists(output_path):
            os.startfile(output_path)
        else:
            messagebox.showwarning("Aviso", "Arquivo de resultado não encontrado!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaMatchingFarmaceutico(root)
    root.mainloop()
