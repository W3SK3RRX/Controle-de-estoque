import logging
from pathlib import Path

# Pasta de logs
Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/estoque.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def registrar_log(acao, usuario="Sistema", detalhes=""):
    logging.info(f"{usuario} - {acao} - {detalhes}")
