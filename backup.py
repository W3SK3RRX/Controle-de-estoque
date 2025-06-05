import os
import shutil
from datetime import datetime

# 🔗 Caminho do arquivo do banco de dados (ajuste conforme seu projeto)
caminho_banco = os.path.join(os.getcwd(), "estoque.db")  # Exemplo, se estiver na mesma pasta

# 📂 Pasta onde os backups serão armazenados
pasta_backup = os.path.join(os.getcwd(), "backups")

# 🏗️ Cria a pasta de backup se não existir
os.makedirs(pasta_backup, exist_ok=True)

# 📅 Nome do backup com data e hora
nome_backup = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.db"

# 🔗 Caminho completo do arquivo de backup
caminho_backup = os.path.join(pasta_backup, nome_backup)

# 🗄️ Copia o banco para a pasta de backup
try:
    shutil.copy2(caminho_banco, caminho_backup)
    print(f"✅ Backup realizado com sucesso: {caminho_backup}")
except Exception as e:
    print(f"❌ Erro ao realizar backup: {e}")
