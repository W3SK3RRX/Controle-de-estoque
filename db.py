import sqlite3
import os
import sys
from pathlib import Path

def resource_path(relative_path):
    # Quando rodando via PyInstaller, _MEIPASS aponta para os arquivos extraídos
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Caminho real do banco (fora do .exe, ao lado dele)
def get_db_path():
    if getattr(sys, 'frozen', False):  # se rodando como .exe
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(__file__)
    return os.path.join(base, "estoque.db")

DB_PATH = get_db_path()

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

    cursor.execute("SELECT * FROM usuarios")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", ('admin', '123'))
        conn.commit()

    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    criar_usuario_padrao()
    print("Banco de dados criado com sucesso.")
