import sqlite3
import os

class AtelieDB:
    def __init__(self, db_name='atelie.db'):
        self.db_name = db_name
        self.create_table()

    def get_db_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def create_table(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()

    # Tabela de itens produzidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS itens_produzidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                item TEXT NOT NULL,
                quantidade INTEGER NOT NULL
            )
        ''')

        # Tabela de horas trabalhadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS horas_trabalhadas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                horas REAL NOT NULL
        )
    ''')
        
        # Tabela de produtos   
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_produto TEXT NOT NULL,
                variante_produto TEXT,
                descricao TEXT,
                materiais_principais TEXT,
                custo_producao_estimado REAL,
                tempo_producao_estimado REAL,
                preco_venda REAL,
                margem_lucro REAL
            )
        ''')
        conn.commit()
        conn.close()

    def insert_product(self, tipo, variante, descricao, materiais, custo_prod, tempo_prod, preco_venda, margem_lucro):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (tipo_produto, variante_produto, descricao, materiais_principais,
                                  custo_producao_estimado, tempo_producao_estimado, preco_venda, margem_lucro)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (tipo, variante, descricao, materiais, custo_prod, tempo_prod, preco_venda, margem_lucro))
        conn.commit()
        conn.close()

    def delete_product(self, product_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM produtos WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()

    def get_products(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos ORDER BY id DESC')
        products = cursor.fetchall()
        conn.close()
        return products
