import csv

def carregar_produtos(nome_arquivo='produtos.csv'):
    """Lê o arquivo CSV de produtos e retorna uma lista de dicionários."""
    try:
        with open(nome_arquivo, mode='r', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            produtos = [linha for linha in leitor_csv]
            return produtos
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        return []

# --- Programa Principal ---
if __name__ == "__main__":
    print("Iniciando o sistema do Ateliê...")
    
    lista_de_produtos = carregar_produtos()
    
    if lista_de_produtos:
        print("Produtos carregados com sucesso!")
        for produto in lista_de_produtos:
            # Formatando uma string bonita para mostrar cada produto
            print(f"  - ID: {produto['id_produto']}, "
                  f"Nome: {produto['nome']} "
                  f"({produto['tamanho']}), "
                  f"Meta: {produto['tempo_estimado_min']} min")
    else:
        print("Nenhum produto encontrado. Verifique o arquivo produtos.csv")