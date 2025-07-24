import requests
import os
import logging
import time
import random
from dotenv import load_dotenv

load_dotenv()
WAHA_URL = os.getenv("WAHA_URL")
WAHA_SESSION = os.getenv("WAHA_SESSION")

def _send_seen(chat_id):
    requests.post(f"{WAHA_URL}/api/sendSeen", json={"session": WAHA_SESSION, "chatId": chat_id})

def _start_typing(chat_id):
    requests.post(f"{WAHA_URL}/api/startTyping", json={"session": WAHA_SESSION, "chatId": chat_id})

def _stop_typing(chat_id):
    requests.post(f"{WAHA_URL}/api/stopTyping", json={"session": WAHA_SESSION, "chatId": chat_id})

def enviar_whatsapp(numero, mensagem, equipe=None):
    chat_id = f"{numero}@c.us"
    url = f"{WAHA_URL}/api/sendText"
    payload = {
        "session": WAHA_SESSION,
        "chatId": chat_id,
        "text": mensagem
    }

    try:
        logging.info(f"⏳ Enviando para {chat_id} (Equipe: {equipe})")
        logging.info(f"Payload: {payload}")

        _send_seen(chat_id)
        _start_typing(chat_id)
        time.sleep(random.uniform(2, 4))
        _stop_typing(chat_id)

        r = requests.post(url, json=payload)

        logging.info(f"WAHA status: {r.status_code}")
        logging.info(f"WAHA response: {r.text}")

        if r.status_code != 201:
            raise Exception(f"Erro WAHA: {r.status_code} - {r.text}")

        logging.info(f"✅ Mensagem enviada para {numero} (Equipe: {equipe})")
        time.sleep(random.uniform(4, 8))

    except Exception as e:
        logging.error(f"❌ Falha ao enviar para {numero} - {e}")
        raise

    except Exception as e:
        logging.error(f"❌ Erro ao enviar para {numero}: {e}")
