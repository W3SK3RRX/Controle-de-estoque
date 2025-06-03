import sqlite3
from datetime import datetime, timedelta
import os

# Caminho para o banco de dados
db_path = os.path.join("estoque.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 🔧 Criação da tabela de categorias (se não existir)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL
    )
""")

# 🔧 Criação da tabela de produtos (se não existir)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        unidade TEXT NOT NULL,
        validade DATE,
        estoque_minimo INTEGER NOT NULL,
        FOREIGN KEY (categoria) REFERENCES categorias(nome)
    )
""")

# 🚀 Categorias de teste
categorias = ["Açaí", "Complemento", "Embalagem"]

for categoria in categorias:
    cursor.execute("""
        INSERT OR IGNORE INTO categorias (nome) VALUES (?)
    """, (categoria,))

# 📦 Produtos de teste
produtos = [
    # nome, categoria, quantidade, unidade, validade, estoque_minimo
    ("Açaí Tradicional 500ml", "Açaí", 10, "unidade", (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'), 5),
    ("Açaí com Leite Condensado", "Açaí", 3, "unidade", (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'), 5),
    ("Granola", "Complemento", 2, "unidade", (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'), 5),
    ("Leite em Pó", "Complemento", 8, "unidade", (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'), 5),
    ("Copo 500ml", "Embalagem", 50, "unidade", (datetime.now() + timedelta(days=300)).strftime('%Y-%m-%d'), 10),
    ("Açaí Premium 1L", "Açaí", 1, "unidade", (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'), 5),  # Vencido
]

for produto in produtos:
    cursor.execute("""
        INSERT INTO produtos (nome, categoria, quantidade, unidade, validade, estoque_minimo)
        VALUES (?, ?, ?, ?, ?, ?)
    """, produto)

conn.commit()
conn.close()

print("✅ Categorias e produtos de teste inseridos com sucesso!")
