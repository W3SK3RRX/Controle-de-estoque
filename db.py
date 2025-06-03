import sqlite3
from pathlib import Path

# Pasta do banco
Path("database").mkdir(exist_ok=True)

DB_PATH = "estoque.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        senha TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        unidade TEXT NOT NULL,
        validade DATE,
        estoque_minimo INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_hora TEXT NOT NULL,
        usuario TEXT NOT NULL,
        acao TEXT NOT NULL,
        detalhes TEXT
    )
    """)

    conn.commit()
    conn.close()

def criar_usuario_padrao():
    conn = conectar()
    cursor = conn.cursor()

    # Verifica se já existe usuário
    cursor.execute("SELECT * FROM usuarios")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", ('admin', '123'))
        conn.commit()

    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    criar_usuario_padrao()
    print("Banco de dados criado com sucesso.")
