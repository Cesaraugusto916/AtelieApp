import customtkinter as ctk
from tkinter import ttk # Precisamos do ttk para a nossa tabela (Treeview)
from datetime import datetime
from tkinter import messagebox
import csv
import os

# --- Configurações Iniciais ---
ctk.set_appearance_mode("system")  # Pode ser "system", "dark" ou "light"
ctk.set_default_color_theme("green") # Temas: "blue", "green", "dark-blue"

# --- Dados Fake (por enquanto) ---
dados_registros_fake = [
    ['2025-09-15', '09:00', '17:00', 'Necessaire M, Ecobag'],
    ['2025-09-14', '13:00', '18:00', 'Bolsa de Praia'],
]
cabecalho_registros = ['Data', 'Início', 'Fim', 'Itens Produzidos']

# --- Classe Principal do Aplicativo ---
class AtelieApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configuração da Janela Principal ---
        self.title("AteliêApp da Mamãe")
        self.geometry("800x600")

        # --- Caminho para o arquivo de dados ---
        self.produtos_csv_path = "produtos.csv"

        # --- Fontes Padronizadas ---
        self.default_font = ctk.CTkFont(size=15, weight="bold")
        self.title_font = ctk.CTkFont(size=20, weight="bold")

        # --- Criação das Abas ---
        self.tabview = ctk.CTkTabview(self, width=780)
        self.tabview.pack(padx=10, pady=10)

        self.tab_registros = self.tabview.add("Registrar Trabalho")
        self.tab_produtos = self.tabview.add("Gerenciar Produtos")
        
        # --- Populando cada Aba ---
        self.criar_aba_registros()
        self.criar_aba_produtos()
        self._popular_tabela_produtos()

    def criar_aba_registros(self):
        # --- Frame para os inputs da sessão ---
        frame_sessao = ctk.CTkFrame(self.tab_registros)
        frame_sessao.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_sessao, text="Registrar Nova Sessão de Trabalho", font=self.title_font).grid(row=0, column=0, columnspan=5, pady=10, padx=10)

        # --- Inputs de Data ---
        hoje = datetime.now()
        ctk.CTkLabel(frame_sessao, text="Data:", font=self.default_font).grid(row=1, column=0, padx=(10,5), pady=10, sticky="w")
        entry_dia = ctk.CTkEntry(frame_sessao, width=50, font=self.default_font)
        entry_dia.insert(0, hoje.strftime('%d'))
        entry_dia.grid(row=1, column=1, pady=10)
        entry_mes = ctk.CTkEntry(frame_sessao, width=50, font=self.default_font)
        entry_mes.insert(0, hoje.strftime('%m'))
        entry_mes.grid(row=1, column=2, padx=5, pady=10)
        entry_ano = ctk.CTkEntry(frame_sessao, width=70, font=self.default_font)
        entry_ano.insert(0, hoje.strftime('%Y'))
        entry_ano.grid(row=1, column=3, pady=10)

        # --- Inputs de Horário de Início ---
        ctk.CTkLabel(frame_sessao, text="Início:", font=self.default_font).grid(row=2, column=0, padx=(10,5), pady=10, sticky="w")
        entry_inicio_h = ctk.CTkEntry(frame_sessao, width=50, placeholder_text="HH", font=self.default_font)
        entry_inicio_h.grid(row=2, column=1, pady=10)
        entry_inicio_m = ctk.CTkEntry(frame_sessao, width=50, placeholder_text="MM", font=self.default_font)
        entry_inicio_m.grid(row=2, column=2, padx=5, pady=10)

        # --- Inputs de Horário de Fim ---
        ctk.CTkLabel(frame_sessao, text="Fim:", font=self.default_font).grid(row=3, column=0, padx=(10,5), pady=10, sticky="w")
        entry_fim_h = ctk.CTkEntry(frame_sessao, width=50, placeholder_text="HH", font=self.default_font)
        entry_fim_h.grid(row=3, column=1, pady=10)
        entry_fim_m = ctk.CTkEntry(frame_sessao, width=50, placeholder_text="MM", font=self.default_font)
        entry_fim_m.grid(row=3, column=2, padx=5, pady=10)

        btn_salvar_sessao = ctk.CTkButton(frame_sessao, text="Salvar Sessão", font=self.default_font)
        btn_salvar_sessao.grid(row=4, column=0, columnspan=5, pady=20)

        # --- Frame para a tabela de registros ---
        frame_tabela_registros = ctk.CTkFrame(self.tab_registros)
        frame_tabela_registros.pack(pady=10, padx=10, fill="both", expand=True)

        ctk.CTkLabel(frame_tabela_registros, text="Últimos Registros", font=self.title_font).pack(pady=5)
        
        # Criando a tabela (Treeview)
        tabela_registros = ttk.Treeview(frame_tabela_registros, columns=cabecalho_registros, show='headings')
        for col in cabecalho_registros:
            tabela_registros.heading(col, text=col)
        for dado in dados_registros_fake:
            tabela_registros.insert('', 'end', values=dado)
        tabela_registros.pack(pady=10, padx=10, fill="both", expand=True)
        
        btn_excluir_sessao = ctk.CTkButton(frame_tabela_registros, text="Excluir Selecionado", font=self.default_font)
        btn_excluir_sessao.pack(pady=10)

    def criar_aba_produtos(self):
        # Frame para o cadastro de produtos
        frame_cadastro = ctk.CTkFrame(self.tab_produtos)
        frame_cadastro.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_cadastro, text="Cadastrar Novo Produto", font=self.title_font).grid(row=0, column=0, columnspan=4, pady=10)
        
        ctk.CTkLabel(frame_cadastro, text="Nome:", font=self.default_font).grid(row=1, column=0, padx=5, sticky="w")
        self.entry_nome = ctk.CTkEntry(frame_cadastro, width=200, font=self.default_font)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=10)

        ctk.CTkLabel(frame_cadastro, text="Tamanho:", font=self.default_font).grid(row=1, column=2, padx=5, sticky="w")
        self.entry_tamanho = ctk.CTkEntry(frame_cadastro, font=self.default_font)
        self.entry_tamanho.grid(row=1, column=3, padx=5, pady=10)
        
        ctk.CTkLabel(frame_cadastro, text="Meta (min):", font=self.default_font).grid(row=2, column=0, padx=5, sticky="w")
        self.entry_meta = ctk.CTkEntry(frame_cadastro, width=100, font=self.default_font)
        self.entry_meta.grid(row=2, column=1, padx=5, pady=10)

        btn_salvar_produto = ctk.CTkButton(frame_cadastro, text="Salvar Novo Produto", font=self.default_font, command=self._salvar_novo_produto)
        btn_salvar_produto.grid(row=3, column=0, columnspan=4, pady=10)

        # Frame para a tabela de produtos
        frame_tabela_produtos = ctk.CTkFrame(self.tab_produtos)
        frame_tabela_produtos.pack(pady=10, padx=10, fill="both", expand=True)

        ctk.CTkLabel(frame_tabela_produtos, text="Produtos Cadastrados", font=self.title_font).pack(pady=5)
        
        cabecalho_produtos = ['ID', 'Nome', 'Tamanho', 'Meta (min)']
        self.tabela_produtos = ttk.Treeview(frame_tabela_produtos, columns=cabecalho_produtos, show='headings')
        for col in cabecalho_produtos:
            self.tabela_produtos.heading(col, text=col)
        self.tabela_produtos.pack(pady=10, padx=10, fill="both", expand=True)

        btn_excluir_produto = ctk.CTkButton(frame_tabela_produtos, text="Excluir Produto Selecionado", font=self.default_font)
        btn_excluir_produto.pack(pady=10)

    def _carregar_produtos_csv(self):
        """Lê os dados do arquivo CSV de produtos."""
        if not os.path.exists(self.produtos_csv_path):
            return []
        
        with open(self.produtos_csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                next(reader) # Pula o cabeçalho
                return list(reader)
            except StopIteration: # Arquivo está vazio
                return []

    def _popular_tabela_produtos(self):
        """Limpa a tabela de produtos e a preenche com dados do CSV."""
        # Limpa a tabela antes de inserir novos dados
        for item in self.tabela_produtos.get_children():
            self.tabela_produtos.delete(item)

        # Carrega os dados do CSV
        produtos = self._carregar_produtos_csv()

        # Insere os dados na tabela
        for produto in produtos:
            self.tabela_produtos.insert('', 'end', values=produto)

    def _salvar_novo_produto(self):
        """Salva um novo produto no arquivo CSV e atualiza a tabela."""
        # a. Obter o texto dos campos de entrada
        nome = self.entry_nome.get()
        tamanho = self.entry_tamanho.get()
        meta = self.entry_meta.get()

        # b. Validar se o nome não está vazio
        if not nome:
            messagebox.showerror("Erro", "O nome do produto não pode estar vazio.")
            return

        # c. Gerar um novo ID
        produtos = self._carregar_produtos_csv()
        if not produtos:
            novo_id_num = 1
        else:
            max_id = 0
            for produto in produtos:
                try:
                    id_num = int(produto[0].split('_')[-1])
                    if id_num > max_id:
                        max_id = id_num
                except (ValueError, IndexError):
                    continue # Ignora IDs mal formatados
            novo_id_num = max_id + 1
        
        novo_id = f"prod_{novo_id_num:03d}"

        # d. Criar a lista com os novos dados
        novo_produto = [novo_id, nome, tamanho, meta]

        # e. Adicionar ao arquivo CSV
        with open(self.produtos_csv_path, mode='a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(novo_produto)

        # f. Atualizar a tabela, g. Limpar campos e h. Mostrar sucesso
        self._popular_tabela_produtos()
        self.entry_nome.delete(0, 'end')
        self.entry_tamanho.delete(0, 'end')
        self.entry_meta.delete(0, 'end')
        messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")

# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    app = AtelieApp()
    app.mainloop()