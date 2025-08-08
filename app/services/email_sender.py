import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

def enviar_log_por_email(caminho_arquivo_log, traceback_erro):
    """
    Envia um arquivo de log por e-mail para o desenvolvedor e tenta excluí-lo após o envio.
    """
    # Credenciais e configurações do e-mail
    remetente = os.getenv("EMAIL_USER")
    destinatario = os.getenv("EMAIL_TO")
    senha = os.getenv("EMAIL_PASS")
    host = os.getenv("EMAIL_HOST")
    porta = os.getenv("EMAIL_PORT")

    if not all([remetente, destinatario, senha, host, porta]):
        logging.error("As variáveis de ambiente para envio de e-mail não estão configuradas.")
        return

    try:
        # Criação do e-mail
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = "⚠️ Erro Crítico na Aplicação - Log de Execução"

        corpo = (
            "Olá,\n\n"
            "Ocorreu um erro crítico na aplicação. O log de execução está anexado.\n\n"
            "--- TRACEBACK DO ERRO ---\n"
            f"{traceback_erro}\n"
            "--------------------------\n\n"
            "Atenciosamente,\n"
            "Sistema de Alertas Automático"
        )
        msg.attach(MIMEText(corpo, 'plain'))

        # Anexo do log
        if os.path.exists(caminho_arquivo_log):
            with open(caminho_arquivo_log, "rb") as anexo:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(anexo.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f"attachment; filename={os.path.basename(caminho_arquivo_log)}",
                )
                msg.attach(part)
        else:
            logging.warning(f"Arquivo de log não encontrado: {caminho_arquivo_log}")

        # Envio
        server = smtplib.SMTP(host, int(porta))
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())
        server.quit()

        logging.info(f"E-mail de erro enviado com sucesso para {destinatario}.")

    except Exception as e:
        logging.error(f"Falha ao tentar enviar o e-mail de log: {e}")
        return  # Não tenta excluir o log se envio falhar

    # Força remoção de todos os FileHandlers associados ao logging global
    for handler in logging.root.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            handler.flush()
            handler.close()
            logging.root.removeHandler(handler)

    # Exclui o log sem usar logging
    if os.path.exists(caminho_arquivo_log):
        try:
            os.remove(caminho_arquivo_log)
            print(f"🧹 Log excluído após envio: {caminho_arquivo_log}")
        except Exception as e:
            print(f"⚠️ Não foi possível excluir o log: {e}")
