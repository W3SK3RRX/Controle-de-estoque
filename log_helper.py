from datetime import datetime
import db


def registrar(usuario, acao, detalhes=""):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (data_hora, usuario, acao, detalhes) 
        VALUES (?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), usuario, acao, detalhes))
    conn.commit()
    conn.close()
