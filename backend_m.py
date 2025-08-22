import sqlite3

# Conecta (ou cria) o banco de dados local
conn = sqlite3.connect("atelie.db")
cursor = conn.cursor()

# Cria a tabela de itens
cursor.execute("""
CREATE TABLE IF NOT EXISTS itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tempo_estimado REAL,
    observacoes TEXT
)
""")

# Cria a tabela de sessões
cursor.execute("""
CREATE TABLE IF NOT EXISTS sessoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    item_id INTEGER NOT NULL,
    horas_trabalhadas REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    observacoes TEXT,
    FOREIGN KEY (item_id) REFERENCES itens(id)
)
""")

# Salva e fecha a conexão
conn.commit()
conn.close()
