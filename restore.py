# restore.py
import os
import shutil
from tkinter import messagebox

def restaurar_backup_mais_recente():
    pasta_backup = "backups"
    if not os.path.exists(pasta_backup):
        messagebox.showerror("Erro", "Nenhum diretório de backup encontrado.")
        return

    arquivos = [f for f in os.listdir(pasta_backup) if f.startswith("estoque_backup_") and f.endswith(".db")]
    if not arquivos:
        messagebox.showerror("Erro", "Nenhum arquivo de backup encontrado.")
        return

    arquivos = [f for f in os.listdir(pasta_backup) if f.endswith(".db")]
    print(f"Arquivos encontrados: {arquivos}")
    backup_mais_recente = os.path.join(pasta_backup, arquivos[0])

    try:
        shutil.copy2(backup_mais_recente, "estoque.db")
        messagebox.showinfo("Sucesso", f"Banco restaurado com backup de:\n{backup_mais_recente}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao restaurar backup:\n{e}")
