import logging
import os
from datetime import datetime

def configurar_log():
    """Cria e configura log com nome baseado na data/hora da execução"""
    os.makedirs("log", exist_ok=True)

    data_hora = datetime.now().strftime("%d_%m_%y__%H_%M_%S")
    nome_arquivo = f"log/log_execucao_{data_hora}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(nome_arquivo, encoding="utf-8")
        ]
    )

