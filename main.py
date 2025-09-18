import customtkinter as ctk
from tkinter import ttk # Precisamos do ttk para a nossa tabela (Treeview)
from datetime import datetime
from tkinter import messagebox
import csv
import os

# --- Configurações Iniciais ---
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

# --- Classe Principal do Aplicativo ---
class AtelieApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configuração da Janela Principal ---
        self.title("AteliêApp da Mamãe")
        self.geometry("800x600")
        self.attributes('-zoomed', True)
        self.minsize(600, 500) # Define um tamanho mínimo para a janela

        # --- Caminhos para os arquivos de dados ---
        self.produtos_csv_path = "produtos.csv"
        self.registros_csv_path = "registros.csv"

        # --- Fontes Padronizadas ---
        self.default_font = ctk.CTkFont(size=15, weight="bold")
        self.title_font = ctk.CTkFont(size=20, weight="bold")

        # --- Criação das Abas ---
        self.tabview = ctk.CTkTabview(self, width=780, height=580)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)

        self.tab_registros = self.tabview.add("Registrar Trabalho")
        self.tab_produtos = self.tabview.add("Gerenciar Produtos")
        
        # --- Populando cada Aba ---
        self.criar_aba_registros()
        self.criar_aba_produtos()
        
        # --- Carregamento Inicial dos Dados ---
        self._popular_tabela_produtos() # Isso também vai popular o dropdown
        self._popular_tabela_registros()

    def criar_aba_registros(self):
        # --- Frame principal da aba ---
        self.tab_registros.grid_rowconfigure(1, weight=1)
        self.tab_registros.grid_columnconfigure(0, weight=1)

        # --- Frame para os inputs da sessão ---
        frame_sessao = ctk.CTkFrame(self.tab_registros)
        frame_sessao.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        frame_sessao.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame_sessao, text="Registrar Nova Sessão de Trabalho", font=self.title_font).grid(row=0, column=0, columnspan=6, pady=10, padx=10)

        # --- Inputs de Data ---
        hoje = datetime.now()
        ctk.CTkLabel(frame_sessao, text="Data:", font=self.default_font).grid(row=1, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_dia = ctk.CTkEntry(frame_sessao, width=50, font=self.default_font)
        self.entry_dia.insert(0, hoje.strftime('%d'))
        self.entry_dia.grid(row=1, column=1, pady=5, sticky="w")
        self.entry_mes = ctk.CTkEntry(frame_sessao, width=50, font=self.default_font)
        self.entry_mes.insert(0, hoje.strftime('%m'))
        self.entry_mes.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_ano = ctk.CTkEntry(frame_sessao, width=70, font=self.default_font)
        self.entry_ano.insert(0, hoje.strftime('%Y'))
        self.entry_ano.grid(row=1, column=3, pady=5, sticky="w")

        # --- Inputs de Horário ---
        ctk.CTkLabel(frame_sessao, text="Início:", font=self.default_font).grid(row=2, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_inicio_h = ctk.CTkEntry(frame_sessao, width=50, placeholder_text="HH", font=self.default_font)
        self.entry_inicio_h.grid(row=2, column=1, pady=5, sticky="w")
        self.entry_inicio_m = ctk.CTkEntry(frame_sessao, width=50, placeholder_text="MM", font=self.default_font)
        self.entry_inicio_m.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(frame_sessao, text="Fim:", font=self.default_font).grid(row=3, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_fim_h = ctk.CTkEntry(frame_sessao, width=50, placeholder_text="HH", font=self.default_font)
        self.entry_fim_h.grid(row=3, column=1, pady=5, sticky="w")
        self.entry_fim_m = ctk.CTkEntry(frame_sessao, width=50, placeholder_text="MM", font=self.default_font)
        self.entry_fim_m.grid(row=3, column=2, padx=5, pady=5, sticky="w")

        # --- Itens Produzidos ---
        ctk.CTkLabel(frame_sessao, text="Itens Produzidos:", font=self.default_font).grid(row=4, column=0, padx=(10,5), pady=5, sticky="w")
        self.option_menu_produtos = ctk.CTkOptionMenu(frame_sessao, values=["Carregando..."], font=self.default_font)
        self.option_menu_produtos.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="we")
        
        ctk.CTkLabel(frame_sessao, text="Qtd:", font=self.default_font).grid(row=4, column=3, padx=(0,5), pady=5, sticky="e")
        self.entry_item_qtd = ctk.CTkEntry(frame_sessao, width=50, font=self.default_font)
        self.entry_item_qtd.grid(row=4, column=4, padx=(0,5), pady=5, sticky="w")
        
        btn_adicionar_item = ctk.CTkButton(frame_sessao, text="Adicionar", width=100, font=self.default_font, command=self._adicionar_item_sessao)
        btn_adicionar_item.grid(row=4, column=5, padx=(0,10), pady=5, sticky="w")

        self.textbox_itens_sessao = ctk.CTkTextbox(frame_sessao, height=80, font=self.default_font)
        self.textbox_itens_sessao.grid(row=5, column=0, columnspan=6, padx=10, pady=10, sticky="we")

        btn_salvar_sessao = ctk.CTkButton(frame_sessao, text="Salvar Sessão de Trabalho", font=self.default_font, command=self._salvar_sessao)
        btn_salvar_sessao.grid(row=6, column=0, columnspan=6, pady=20)

        # --- Frame para a tabela de registros ---
        frame_tabela_registros = ctk.CTkFrame(self.tab_registros)
        frame_tabela_registros.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        frame_tabela_registros.grid_rowconfigure(1, weight=1)
        frame_tabela_registros.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame_tabela_registros, text="Últimos Registros", font=self.title_font).grid(row=0, column=0, pady=5, padx=10)
        
        # --- Tabela ---
        cabecalho_registros = ['ID', 'Data', 'Início', 'Fim', 'Itens Produzidos']
        self.tabela_registros = ttk.Treeview(frame_tabela_registros, columns=cabecalho_registros, show='headings')
        for col in cabecalho_registros:
            self.tabela_registros.heading(col, text=col)
        self.tabela_registros.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        # --- Botão de Excluir ---
        btn_excluir_sessao = ctk.CTkButton(frame_tabela_registros, text="Excluir Selecionado", font=self.default_font, command=self._excluir_registro_selecionado)
        btn_excluir_sessao.grid(row=2, column=0, pady=10)

    def criar_aba_produtos(self):
        # --- Frame principal da aba ---
        self.tab_produtos.grid_rowconfigure(1, weight=1)
        self.tab_produtos.grid_columnconfigure(0, weight=1)

        # Frame para o cadastro de produtos
        frame_cadastro = ctk.CTkFrame(self.tab_produtos)
        frame_cadastro.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

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
        frame_tabela_produtos.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        frame_tabela_produtos.grid_rowconfigure(1, weight=1)
        frame_tabela_produtos.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame_tabela_produtos, text="Produtos Cadastrados", font=self.title_font).grid(row=0, column=0, pady=5, padx=10)
        
        # --- Botão de Excluir ---
        btn_excluir_produto = ctk.CTkButton(frame_tabela_produtos, text="Excluir Produto Selecionado", font=self.default_font, command=self._excluir_produto_selecionado)
        btn_excluir_produto.grid(row=2, column=0, pady=10)

        # --- Tabela ---
        cabecalho_produtos = ['ID', 'Nome', 'Tamanho', 'Meta (min)']
        self.tabela_produtos = ttk.Treeview(frame_tabela_produtos, columns=cabecalho_produtos, show='headings')
        for col in cabecalho_produtos:
            self.tabela_produtos.heading(col, text=col)
        self.tabela_produtos.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

    def _get_csv_data(self, file_path, header):
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            with open(file_path, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
            return []
        
        with open(file_path, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            try:
                file_header = next(reader)
                if file_header != header:
                    # Se o cabeçalho não bate, sobrescreve o arquivo
                    return self._get_csv_data(file_path, header)
                return list(reader)
            except StopIteration:
                return []

    def _carregar_produtos_csv(self):
        header = ['id_produto', 'nome', 'tamanho', 'tempo_estimado_min']
        return self._get_csv_data(self.produtos_csv_path, header)

    def _carregar_registros_csv(self):
        header = ['id_registro', 'data', 'inicio', 'fim', 'itens_produzidos']
        return self._get_csv_data(self.registros_csv_path, header)

    def _atualizar_dropdown_produtos(self):
        produtos = self._carregar_produtos_csv()
        nomes_produtos = [f"{p[1]} ({p[2]})" for p in produtos if len(p) > 2] if produtos else ["Nenhum produto cadastrado"]
        self.option_menu_produtos.configure(values=nomes_produtos)
        self.option_menu_produtos.set(nomes_produtos[0] if nomes_produtos else "")

    def _popular_tabela_produtos(self):
        for item in self.tabela_produtos.get_children():
            self.tabela_produtos.delete(item)
        produtos = self._carregar_produtos_csv()
        for produto in produtos:
            self.tabela_produtos.insert('', 'end', values=produto)
        self._atualizar_dropdown_produtos()

    def _popular_tabela_registros(self):
        for item in self.tabela_registros.get_children():
            self.tabela_registros.delete(item)
        registros = self._carregar_registros_csv()
        for registro in registros:
            self.tabela_registros.insert('', 'end', values=registro)

    def _salvar_novo_produto(self):
        nome = self.entry_nome.get()
        tamanho = self.entry_tamanho.get()
        meta = self.entry_meta.get()

        if not nome:
            messagebox.showerror("Erro", "O nome do produto não pode estar vazio.")
            return

        produtos = self._carregar_produtos_csv()
        novo_id_num = 1
        if produtos:
            try:
                ultimo_id = produtos[-1][0]
                novo_id_num = int(ultimo_id.split('_')[-1]) + 1
            except (ValueError, IndexError):
                max_id = 0
                for p in produtos:
                    try:
                        id_num = int(p[0].split('_')[-1])
                        if id_num > max_id: max_id = id_num
                    except (ValueError, IndexError): continue
                novo_id_num = max_id + 1

        novo_id = f"prod_{novo_id_num:03d}"
        novo_produto = [novo_id, nome, tamanho, meta]

        with open(self.produtos_csv_path, mode='a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(novo_produto)

        self._popular_tabela_produtos()
        self.entry_nome.delete(0, 'end')
        self.entry_tamanho.delete(0, 'end')
        self.entry_meta.delete(0, 'end')
        messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")

    def _excluir_produto_selecionado(self):
        selected_item = self.tabela_produtos.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um produto para excluir.")
            return

        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir o produto?"):
            return

        produto_id = self.tabela_produtos.item(selected_item)['values'][0]
        produtos = self._carregar_produtos_csv()
        produtos_mantidos = [p for p in produtos if p[0] != produto_id]

        header = ['id_produto', 'nome', 'tamanho', 'tempo_estimado_min']
        with open(self.produtos_csv_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(produtos_mantidos)

        self._popular_tabela_produtos()
        messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")

    def _adicionar_item_sessao(self):
        produto_selecionado = self.option_menu_produtos.get()
        quantidade = self.entry_item_qtd.get()

        if not produto_selecionado or "Nenhum produto" in produto_selecionado:
            messagebox.showerror("Erro", "Nenhum produto selecionado.")
            return
        if not quantidade.isdigit() or int(quantidade) <= 0:
            messagebox.showerror("Erro", "A quantidade deve ser um número positivo.")
            return
        
        item_str = f'"{produto_selecionado} (Qtd: {quantidade})\n'
        self.textbox_itens_sessao.insert("end", item_str)
        self.entry_item_qtd.delete(0, "end")

    def _salvar_sessao(self):
        data = f"{self.entry_ano.get()}-{self.entry_mes.get()}-{self.entry_dia.get()}"
        inicio = f"{self.entry_inicio_h.get()}:{self.entry_inicio_m.get()}"
        fim = f"{self.entry_fim_h.get()}:{self.entry_fim_m.get()}"
        itens_produzidos = self.textbox_itens_sessao.get("1.0", "end-1c").strip()

        if not itens_produzidos:
            messagebox.showerror("Erro", "Nenhum item produzido foi adicionado à sessão.")
            return

        registros = self._carregar_registros_csv()
        novo_id_num = 1
        if registros:
            try:
                ultimo_id = registros[-1][0]
                novo_id_num = int(ultimo_id.split('_')[-1]) + 1
            except (ValueError, IndexError):
                max_id = 0
                for r in registros:
                    try:
                        id_num = int(r[0].split('_')[-1])
                        if id_num > max_id: max_id = id_num
                    except (ValueError, IndexError): continue
                novo_id_num = max_id + 1
        
        novo_id = f"reg_{novo_id_num:03d}"
        novo_registro = [novo_id, data, inicio, fim, itens_produzidos.replace('\n', ' | ')]

        with open(self.registros_csv_path, mode='a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(novo_registro)

        self._popular_tabela_registros()
        
        # Limpar campos
        self.entry_inicio_h.delete(0, 'end')
        self.entry_inicio_m.delete(0, 'end')
        self.entry_fim_h.delete(0, 'end')
        self.entry_fim_m.delete(0, 'end')
        self.textbox_itens_sessao.delete("1.0", "end")
        messagebox.showinfo("Sucesso", "Sessão de trabalho salva com sucesso!")

    def _excluir_registro_selecionado(self):
        selected_item = self.tabela_registros.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um registro para excluir.")
            return

        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir o registro?"):
            return

        registro_id = self.tabela_registros.item(selected_item)['values'][0]
        registros = self._carregar_registros_csv()
        registros_mantidos = [r for r in registros if r[0] != registro_id]

        header = ['id_registro', 'data', 'inicio', 'fim', 'itens_produzidos']
        with open(self.registros_csv_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(registros_mantidos)

        self._popular_tabela_registros()
        messagebox.showinfo("Sucesso", "Registro excluído com sucesso!")

# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    app = AtelieApp()
    app.mainloop()
