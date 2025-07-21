import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()
WAHA_URL = os.getenv("WAHA_URL")
WAHA_SESSION = os.getenv("WAHA_SESSION")

def enviar_whatsapp(numero, mensagem, equipe=None):
    url = f"{WAHA_URL}/api/sendText"
    payload = {
        "session": WAHA_SESSION,
        "chatId": f"{numero}@c.us",
        "text": mensagem
    }

    try:
        r = requests.post(url, json=payload)
        if r.status_code == 201:
            if equipe:
                logging.info(f"✅ Mensagem da equipe {equipe} enviada para {numero}")
            else:
                logging.info(f"✅ Mensagem enviada para {numero}")
        else:
            logging.error(f"❌ Erro ao enviar para {numero} - Status {r.status_code}")
            logging.error(r.text)
    except Exception as e:
        logging.error(f"❌ Erro ao enviar para {numero}: {e}")
