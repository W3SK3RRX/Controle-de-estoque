# backup.py
import os
import shutil
from datetime import datetime

def realizar_backup():
    origem = "estoque.db"
    destino_dir = "backups"
    if not os.path.exists(destino_dir):
        os.makedirs(destino_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    destino = os.path.join(destino_dir, f"estoque_backup_{timestamp}.db")

    shutil.copy2(origem, destino)
    print(f"Backup criado: {destino}")

if __name__ == "__main__":
    realizar_backup()
