import requests
import json
import logging
import time
import random
import os

config_path = os.path.join(os.path.dirname(__file__), "..", "..", "static", "js", "config.json")
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

EVOLUTION_URL = config["EVOLUTION_URL"]
EVOLUTION_INSTANCE = config["EVOLUTION_INSTANCE"]
EVOLUTION_TOKEN = config.get("EVOLUTION_TOKEN", "")

def _get_headers():
    """Retorna os headers padrão para as requisições"""
    return {
        "Content-Type": "application/json",
        "apikey": EVOLUTION_TOKEN
    }

def _send_presence(numero, presence="composing"):
    """Envia status de presença (composing/paused)"""
    try:
        url = f"{EVOLUTION_URL}/message/setPresence/{EVOLUTION_INSTANCE}"
        payload = {
            "number": numero,
            "presence": presence
        }
        requests.post(url, json=payload, headers=_get_headers())
    except Exception as e:
        logging.warning(f"Erro ao enviar presença: {e}")

def enviar_whatsapp(numero, mensagem, equipe=None):
    """
    Envia mensagem via Evolution API
    
    Args:
        numero: Número no formato brasileiro (ex: 5561999999999)
        mensagem: Texto da mensagem
        equipe: Nome da equipe (opcional, apenas para log)
    """
    # Evolution API espera número no formato internacional sem caracteres especiais
    numero_formatado = numero.replace("+", "").replace("-", "").replace(" ", "")
    
    url = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    
    payload = {
        "number": numero_formatado,
        "textMessage": {
            "text": mensagem
        }
    }

    try:
        logging.info(f"⏳ Enviando para {numero_formatado} (Equipe: {equipe})")
        logging.info(f"Payload: {payload}")

        # Simula digitação
        _send_presence(numero_formatado, "composing")
        time.sleep(random.uniform(2, 4))
        _send_presence(numero_formatado, "paused")

        # Envia a mensagem
        response = requests.post(url, json=payload, headers=_get_headers())

        logging.info(f"Evolution API status: {response.status_code}")
        logging.info(f"Evolution API response: {response.text}")

        if response.status_code not in [200, 201]:
            raise Exception(f"Erro Evolution API: {response.status_code} - {response.text}")

        # Verifica se a resposta contém erro
        response_data = response.json()
        if not response_data.get("success", True):
            raise Exception(f"Erro na resposta: {response_data.get('message', 'Erro desconhecido')}")

        logging.info(f"✅ Mensagem enviada para {numero_formatado} (Equipe: {equipe})")
        time.sleep(random.uniform(4, 8))

    except Exception as e:
        logging.error(f"❌ Falha ao enviar para {numero_formatado} - {e}")
        raise