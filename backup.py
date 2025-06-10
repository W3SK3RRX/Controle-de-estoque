# backup.py
import shutil
import os
from datetime import datetime
from tkinter import filedialog, messagebox

def fazer_backup():
    try:
        # Caminho original do banco
        origem = "estoque.db"

        if not os.path.exists(origem):
            messagebox.showerror("Erro", "Banco de dados não encontrado.")
            return

        # Solicita a pasta de destino
        pasta_destino = filedialog.askdirectory(title="Selecione a pasta de destino para o backup")
        if not pasta_destino:
            return  # Usuário cancelou

        # Nome do arquivo com data e hora
        nome_arquivo = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.db"
        destino = os.path.join(pasta_destino, nome_arquivo)

        shutil.copy2(origem, destino)
        messagebox.showinfo("Backup Realizado", f"Backup salvo com sucesso em:\n{destino}")
    except Exception as e:
        messagebox.showerror("Erro ao fazer backup", str(e))
