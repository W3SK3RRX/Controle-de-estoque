import shutil
import os
from tkinter import filedialog, messagebox

def restaurar_backup():
    try:
        # Solicita ao usuário o arquivo de backup
        caminho_backup = filedialog.askopenfilename(
            title="Selecione o arquivo de backup",
            filetypes=[("SQLite Database", "*.db")]
        )

        if not caminho_backup:
            return  # Cancelado

        destino = "estoque.db"  # Como o banco está na raiz

        # Faz um backup do banco atual, se existir
        if os.path.exists(destino):
            shutil.copy2(destino, destino + ".bak")

        # Restaura o backup selecionado
        shutil.copy2(caminho_backup, destino)

        messagebox.showinfo("Restaurado com Sucesso", "Backup restaurado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro ao restaurar", str(e))
