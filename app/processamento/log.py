import logging
import os
from datetime import datetime

def configurar_log():
    """Cria e configura log com nome baseado na data/hora da execução"""
    os.makedirs("log", exist_ok=True)

    data_hora = datetime.now().strftime("%d_%m_%y__%H_%M_%S")
    nome_arquivo = f"log/log_execucao_{data_hora}.log"

    # Limpa handlers anteriores
    logging.getLogger().handlers.clear()

    # Configura o log
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(nome_arquivo, encoding="utf-8", mode='w')
        ],
        force=True
    )

    logging.info(f"Log configurado: {nome_arquivo}")
    return nome_arquivo

def finalizar_log(caminho_log):
    """Fecha e remove o FileHandler para liberar o arquivo"""
    for handler in logging.getLogger().handlers[:]:
        if isinstance(handler, logging.FileHandler) and handler.baseFilename == caminho_log:
            handler.flush()
            handler.close()
            logging.getLogger().removeHandler(handler)
