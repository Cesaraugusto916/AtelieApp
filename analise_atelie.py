import customtkinter as ctk
import pandas as pd
import numpy as np
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
import calendar
import locale
import re
import os

# Define o local para português para formatar nomes de meses e dias
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    print("Local 'pt_BR.UTF-8' não encontrado. Usando o padrão do sistema.")

# --- Configurações Iniciais ---
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

class AtelieAnalysisApp(ctk.CTk):
    """
    Aplicativo para análise de dados de produção do ateliê.
    """
    def __init__(self):
        super().__init__()

        # --- Configuração da Janela ---
        self.title("Análise de Dados do Ateliê")
        self.attributes('-zoomed', True)
        self.minsize(800, 600)

        # --- CORREÇÃO: Caminhos de arquivo robustos ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.registros_csv_path = os.path.join(script_dir, "registros.csv")
        self.produtos_csv_path = os.path.join(script_dir, "produtos.csv")

        # --- Atributos de Estado ---
        self.visao_atual = "Semanal"
        self.data_referencia = datetime.now().date()
        self.df_registros = pd.DataFrame()

        # --- Carregamento de Dados ---
        self._carregar_e_preparar_dados()

        # --- Criação da Interface ---
        self.tabview = ctk.CTkTabview(self, width=780, height=580)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        self.tab_dashboard = self.tabview.add("Dashboard de Horas")
        self.tab_analise_produtos = self.tabview.add("Análise de Produtos")
        
        self.criar_aba_dashboard()
        self.criar_aba_analise()
        
        # --- Atualização Inicial ---
        self._atualizar_visao()

    def _estilizar_grafico(self, ax, fig):
        """Aplica um estilo visual escuro e limpo ao gráfico Matplotlib."""
        fig.set_facecolor("#2B2B2B")
        ax.set_facecolor("#2B2B2B")
        
        ax.tick_params(colors='white', which='both')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')

        for spine in ax.spines.values():
            spine.set_edgecolor('white')
        
        ax.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.3)

    def criar_aba_dashboard(self):
        self.tab_dashboard.grid_columnconfigure(0, weight=1)
        self.tab_dashboard.grid_rowconfigure(2, weight=1)

        frame_kpis = ctk.CTkFrame(self.tab_dashboard)
        frame_kpis.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")
        frame_kpis.grid_columnconfigure([0, 1, 2], weight=1)

        kpi_font = ctk.CTkFont(size=14)
        kpi_value_font = ctk.CTkFont(size=20, weight="bold")

        ctk.CTkLabel(frame_kpis, text="TOTAL DE HORAS", font=kpi_font).grid(row=0, column=0, pady=(5,0))
        self.label_total_horas = ctk.CTkLabel(frame_kpis, text="---", font=kpi_value_font)
        self.label_total_horas.grid(row=1, column=0, pady=(0,10))

        ctk.CTkLabel(frame_kpis, text="MÉDIA DIÁRIA", font=kpi_font).grid(row=0, column=1, pady=(5,0))
        self.label_media_diaria = ctk.CTkLabel(frame_kpis, text="---", font=kpi_value_font)
        self.label_media_diaria.grid(row=1, column=1, pady=(0,10))

        ctk.CTkLabel(frame_kpis, text="DIAS TRABALHADOS", font=kpi_font).grid(row=0, column=2, pady=(5,0))
        self.label_dias_trabalhados = ctk.CTkLabel(frame_kpis, text="---", font=kpi_value_font)
        self.label_dias_trabalhados.grid(row=1, column=2, pady=(0,10))

        frame_controles = ctk.CTkFrame(self.tab_dashboard)
        frame_controles.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        frame_controles.grid_columnconfigure(1, weight=1)

        self.btn_anterior = ctk.CTkButton(frame_controles, text="< Anterior", command=self._navegar_anterior)
        self.btn_anterior.grid(row=0, column=0, padx=10, pady=10)

        self.label_periodo = ctk.CTkLabel(frame_controles, text="Período", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_periodo.grid(row=0, column=1, padx=10, pady=10)

        self.btn_proximo = ctk.CTkButton(frame_controles, text="Próximo >", command=self._navegar_proximo)
        self.btn_proximo.grid(row=0, column=2, padx=10, pady=10)

        self.segmented_button_visao = ctk.CTkSegmentedButton(frame_controles, 
                                                             values=["Semanal", "Mensal", "Anual"],
                                                             command=self._atualizar_visao)
        self.segmented_button_visao.set("Semanal")
        self.segmented_button_visao.grid(row=0, column=3, padx=10, pady=10)

        self.frame_grafico = ctk.CTkFrame(self.tab_dashboard)
        self.frame_grafico.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="nsew")
        self.frame_grafico.grid_columnconfigure(0, weight=1)
        self.frame_grafico.grid_rowconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots()
        self._estilizar_grafico(self.ax, self.fig)
        plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def criar_aba_analise(self):
        """Cria a interface da aba de Análise de Produtos."""
        self.tab_analise_produtos.grid_columnconfigure(0, weight=1)
        self.tab_analise_produtos.grid_rowconfigure(1, weight=1)

        frame_principal = ctk.CTkFrame(self.tab_analise_produtos)
        frame_principal.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        btn_analise = ctk.CTkButton(frame_principal, text="Calcular Análise de Produção", command=self._executar_analise_produtos)
        btn_analise.pack(pady=10)

        frame_tabela = ctk.CTkFrame(self.tab_analise_produtos)
        frame_tabela.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        frame_tabela.grid_columnconfigure(0, weight=1)
        frame_tabela.grid_rowconfigure(0, weight=1)

        cabecalho = ["Produto", "Tempo Meta (min)", "Tempo Calculado (min)", "Diferença (%)", "Total Produzido"]
        self.tabela_analise = ttk.Treeview(frame_tabela, columns=cabecalho, show='headings')
        for col in cabecalho:
            self.tabela_analise.heading(col, text=col)
            self.tabela_analise.column(col, anchor="center")
        self.tabela_analise.grid(row=0, column=0, sticky="nsew")

    def _carregar_e_preparar_dados(self):
        """Lê e prepara os CSVs, garantindo os tipos de dados corretos e tratando erros."""
        try:
            self.df_registros = pd.read_csv(self.registros_csv_path)
            if self.df_registros.empty:
                return

            self.df_registros['data'] = pd.to_datetime(self.df_registros['data'], errors='coerce')
            self.df_registros.dropna(subset=['data'], inplace=True)
            self.df_registros['data'] = self.df_registros['data'].dt.normalize()

            for col in ['pausa_min', 'duracao_total_min']:
                self.df_registros[col] = pd.to_numeric(self.df_registros[col], errors='coerce').fillna(0)

        except FileNotFoundError:
            messagebox.showwarning("Aviso", f"Arquivo {os.path.basename(self.registros_csv_path)} não encontrado.")
            self.df_registros = pd.DataFrame(columns=['id_registro', 'data', 'inicio', 'fim', 'pausa_min', 'duracao_total_min', 'itens_produzidos'])
        except Exception as e:
            messagebox.showerror("Erro ao Carregar Dados", f"Ocorreu um erro inesperado ao ler {os.path.basename(self.registros_csv_path)}:\n{e}")

    def _executar_analise_produtos(self):
        """Executa a análise de regressão linear para calcular o tempo de produção."""
        try:
            df_produtos = pd.read_csv(self.produtos_csv_path)
            if self.df_registros.empty:
                 messagebox.showerror("Dados Insuficientes", "Não há registros de trabalho para analisar.")
                 return
        except FileNotFoundError:
            messagebox.showerror("Arquivo Não Encontrado", f"Não foi possível encontrar o arquivo: {os.path.basename(self.produtos_csv_path)}")
            return
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao carregar os dados: {e}")
            return

        df_registros_com_producao = self.df_registros[self.df_registros['itens_produzidos'] != 'Nenhuma produção'].copy()

        if len(df_registros_com_producao) < len(df_produtos) + 1: 
            messagebox.showerror("Dados Insuficientes", f"São necessários mais registros com produção (pelo menos {len(df_produtos)+1}) para realizar uma análise confiável.")
            return

        product_ids = df_produtos['id_produto'].unique()
        for pid in product_ids:
            df_registros_com_producao[pid] = 0

        name_to_id = {f"{row['nome']} ({row['tamanho']})": row['id_produto'] for _, row in df_produtos.iterrows()}

        for index, row in df_registros_com_producao.iterrows():
            itens = row['itens_produzidos'].split(' | ')
            for item in itens:
                match = re.search(r'"(.*?)\s\(Qtd:\s*(\d+)\)"', item)
                if match:
                    nome_produto, quantidade = match.groups()
                    pid = name_to_id.get(nome_produto)
                    if pid:
                        df_registros_com_producao.loc[index, pid] += int(quantidade)

        X = df_registros_com_producao[product_ids]
        y = df_registros_com_producao['duracao_total_min']

        if X.sum().sum() == 0:
            messagebox.showerror("Análise Inconclusiva", "Não foi possível extrair dados de produção dos registros. Verifique o formato no arquivo CSV.")
            return

        model = LinearRegression()
        model.fit(X, y)

        if np.all(model.coef_ == 0) or np.isnan(model.coef_).any():
            messagebox.showerror("Análise Inconclusiva", "Não foi possível calcular os tempos. Verifique se há variedade suficiente nos dados de produção registrados.")
            return

        for item in self.tabela_analise.get_children():
            self.tabela_analise.delete(item)

        coef_dict = dict(zip(product_ids, model.coef_))

        for _, row in df_produtos.iterrows():
            pid = row['id_produto']
            nome_completo = f"{row['nome']} ({row['tamanho']})"
            tempo_meta = pd.to_numeric(row['tempo_estimado_min'], errors='coerce')
            tempo_calculado = coef_dict.get(pid, 0)
            total_produzido = X[pid].sum()

            if pd.isna(tempo_meta) or tempo_meta == 0:
                diferenca_pct = 0
            else:
                diferenca_pct = ((tempo_calculado - tempo_meta) / tempo_meta) * 100

            self.tabela_analise.insert("", "end", values=[
                nome_completo,
                f"{tempo_meta:.1f}" if not pd.isna(tempo_meta) else "N/A",
                f"{tempo_calculado:.1f}",
                f"{diferenca_pct:+.1f}%",
                int(total_produzido)
            ])
        
        messagebox.showinfo("Sucesso", "Análise de produção concluída com sucesso!")
        
    def _navegar_anterior(self):
        if self.visao_atual == "Semanal":
            self.data_referencia -= timedelta(days=7)
        elif self.visao_atual == "Mensal":
            primeiro_dia_mes = self.data_referencia.replace(day=1)
            self.data_referencia = primeiro_dia_mes - timedelta(days=1)
        elif self.visao_atual == "Anual":
            self.data_referencia = self.data_referencia.replace(year=self.data_referencia.year - 1)
        self._atualizar_visao()

    def _navegar_proximo(self):
        if self.visao_atual == "Semanal":
            self.data_referencia += timedelta(days=7)
        elif self.visao_atual == "Mensal":
            dias_no_mes = calendar.monthrange(self.data_referencia.year, self.data_referencia.month)[1]
            self.data_referencia += timedelta(days=dias_no_mes)
        elif self.visao_atual == "Anual":
            self.data_referencia = self.data_referencia.replace(year=self.data_referencia.year + 1)
        self._atualizar_visao()

    def _atualizar_visao(self, visao_selecionada: str = None):
        if visao_selecionada:
            self.visao_atual = visao_selecionada
        
        if self.df_registros.empty:
            self.ax.clear()
            self.ax.text(0.5, 0.5, "Nenhum dado para exibir", ha='center', va='center', color='white', fontsize=16)
            self._estilizar_grafico(self.ax, self.fig)
            self.canvas.draw()
            return

        df_filtrado = pd.DataFrame()
        
        if self.visao_atual == "Semanal":
            inicio_semana = self.data_referencia - timedelta(days=self.data_referencia.weekday())
            fim_semana = inicio_semana + timedelta(days=6)
            inicio_semana_ts = pd.to_datetime(inicio_semana)
            fim_semana_ts = pd.to_datetime(fim_semana)
            df_filtrado = self.df_registros[(self.df_registros['data'] >= inicio_semana_ts) & (self.df_registros['data'] <= fim_semana_ts)]
            self._plotar_grafico_semanal(df_filtrado, inicio_semana, fim_semana)
            self.label_periodo.configure(text=f"{inicio_semana.strftime('%d/%m/%Y')} - {fim_semana.strftime('%d/%m/%Y')}")

        elif self.visao_atual == "Mensal":
            df_filtrado = self.df_registros[(self.df_registros['data'].dt.year == self.data_referencia.year) & 
                                          (self.df_registros['data'].dt.month == self.data_referencia.month)]
            self._plotar_grafico_mensal_anual(df_filtrado, "Mensal")
            self.label_periodo.configure(text=f"{self.data_referencia.strftime('%B de %Y').capitalize()}")

        elif self.visao_atual == "Anual":
            df_filtrado = self.df_registros[self.df_registros['data'].dt.year == self.data_referencia.year]
            self._plotar_grafico_mensal_anual(df_filtrado, "Anual")
            self.label_periodo.configure(text=f"Ano de {self.data_referencia.year}")

        if not df_filtrado.empty:
            total_horas = df_filtrado['duracao_total_min'].sum() / 60
            dias_trabalhados = df_filtrado['data'].nunique()
            media_diaria = (total_horas / dias_trabalhados) if dias_trabalhados > 0 else 0
            self.label_total_horas.configure(text=f"{total_horas:.1f}h")
            self.label_media_diaria.configure(text=f"{media_diaria:.1f}h")
            self.label_dias_trabalhados.configure(text=f"{dias_trabalhados} dias")
        else:
            self.label_total_horas.configure(text="0.0h")
            self.label_media_diaria.configure(text="0.0h")
            self.label_dias_trabalhados.configure(text="0 dias")

    def _plotar_grafico_semanal(self, df_semana, inicio_semana, fim_semana):
        print(df_semana) # Para debugging
        self.ax.clear()
        if df_semana.empty:
            self.ax.text(0.5, 0.5, "Sem dados para o período", ha='center', va='center', color='white')
        else:
            df_semana['horas_trabalhadas'] = pd.to_numeric(df_semana['duracao_total_min'], errors='coerce').fillna(0) / 60
            df_semana['dia_da_semana_num'] = df_semana['data'].dt.weekday
            dados_por_dia = df_semana.groupby('dia_da_semana_num')['horas_trabalhadas'].sum()
            dados_por_dia = dados_por_dia.reindex(range(7), fill_value=0)
            dias_em_portugues = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
            barras = self.ax.barh(dias_em_portugues, dados_por_dia.values, color='#009688')
            self.ax.bar_label(barras, fmt='%.1f h', padding=3, color='white', fontsize=10)
            self.ax.set_xlabel("Horas Trabalhadas")
            self.ax.set_title(f"Horas por Dia na Semana de {inicio_semana.strftime('%d/%m')} a {fim_semana.strftime('%d/%m')}")
            self.ax.invert_yaxis()
        self._estilizar_grafico(self.ax, self.fig)
        self.fig.tight_layout()
        self.canvas.draw()

    def _plotar_grafico_mensal_anual(self, df_periodo, tipo):
        self.ax.clear()
        if df_periodo.empty:
            self.ax.text(0.5, 0.5, f"Sem dados para este {tipo.lower()}", ha='center', va='center', color='white')
        else:
            df_periodo['horas_trabalhadas'] = df_periodo['duracao_total_min'] / 60
            if tipo == "Mensal":
                dados_agregados = df_periodo.groupby(df_periodo['data'].dt.day)['horas_trabalhadas'].sum()
                barras = self.ax.bar(dados_agregados.index, dados_agregados.values, color='#20726A')
                self.ax.set_xlabel("Dia do Mês")
                self.ax.set_title(f"Horas Trabalhadas em: {self.data_referencia.strftime('%B de %Y').capitalize()}")
            else: # Anual
                dados_agregados = df_periodo.groupby(df_periodo['data'].dt.month)['horas_trabalhadas'].sum()
                dados_agregados = dados_agregados.reindex(range(1, 13), fill_value=0)
                barras = self.ax.bar(dados_agregados.index, dados_agregados.values, color='#20726A')
                self.ax.set_xticks(range(1, 13))
                self.ax.set_xticklabels([calendar.month_abbr[i].capitalize() for i in range(1, 13)], rotation=0)
                self.ax.set_xlabel("Mês")
                self.ax.set_title(f"Horas Trabalhadas em: {self.data_referencia.year}")
            self.ax.bar_label(barras, fmt='%.1fh', padding=3, color='white', fontsize=10)
            self.ax.set_ylabel("Total de Horas Trabalhadas")
        self._estilizar_grafico(self.ax, self.fig)
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    app = AtelieAnalysisApp()
    app.mainloop()