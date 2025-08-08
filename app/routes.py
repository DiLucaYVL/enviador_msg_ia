from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import json
import logging
import uuid
import traceback
from app.services.email_sender import enviar_log_por_email
from app.processamento.log import configurar_log 
from app.processamento.log import finalizar_log
from app.controller import processar_csv
from app.processamento.mapear_gerencia import mapear_equipe
from app.processamento.csv_reader import carregar_dados

api_bp = Blueprint('api', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@api_bp.route('/enviar', methods=['POST'])
def enviar():
    nome_arquivo_log = configurar_log()

    try:
        file = request.files.get('csvFile')
        ignorar_sabados = request.form.get('ignorarSabados', 'true') == 'true'
        tipo_relatorio = request.form.get('tipoRelatorio', 'Auditoria')
        tipo_relatorio = tipo_relatorio.strip()
        if tipo_relatorio not in {"Auditoria", "Ocorrências"}:
            return jsonify({
                "success": False,
                "log": [{"type": "error", "message": f"❌ Tipo de relatório inválido: {tipo_relatorio}. Selecione 'Auditoria' ou 'Ocorrências'."}]
            }), 400

        debug_mode = request.form.get('debugMode', 'false') == 'true'

        if not file:
            return jsonify({"success": False, "log": ["❌ Nenhum arquivo CSV enviado."]}), 400

        if not file.filename.lower().endswith('csv'):
            return jsonify({"success": False, "log": ["❌ Formato inválido. Envie um arquivo .csv"]}), 400

        filename = secure_filename(file.filename)
        filename = f"{uuid.uuid4().hex[:8]}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        equipes_selecionadas = request.form.get('equipesSelecionadas')
        equipes_selecionadas = set(json.loads(equipes_selecionadas)) if equipes_selecionadas else None

        logging.info(">>> Chamando processar_csv()")
        logs, stats, nome_arquivo_log = processar_csv(filepath, ignorar_sabados, tipo_relatorio, equipes_selecionadas)

        df_debug = None

        if debug_mode:
            if tipo_relatorio == "Ocorrências":
                from app.processamento.csv_reader_ocorrencias import carregar_dados_ocorrencias
                df_debug = carregar_dados_ocorrencias(filepath).to_json(orient="records", force_ascii=False)
            else:
                from app.processamento.csv_reader import carregar_dados
                df_debug = carregar_dados(filepath, ignorar_sabados, tipo_relatorio).to_json(orient="records", force_ascii=False)


        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            "success": True,
            "log": logs,
            "stats": stats,
            "debug": df_debug if debug_mode else None
        })

    except Exception as e:
        tb = traceback.format_exc()
        logging.error("❌ EXCEÇÃO DETALHADA:\n" + tb)

        log_ja_enviado = False

        if nome_arquivo_log:
            try:
                enviar_log_por_email(nome_arquivo_log, tb)
                log_ja_enviado = True
            except Exception as erro_envio:
                logging.error(f"❌ Falha ao enviar log por e-mail: {erro_envio}")

            try:
                finalizar_log(nome_arquivo_log)
            except Exception as e:
                logging.warning(f"⚠️ Falha ao finalizar log: {e}")

            try:
                if os.path.exists(nome_arquivo_log):
                    os.remove(nome_arquivo_log)
                    print(f"🧹 Log excluído com sucesso: {nome_arquivo_log}")
            except Exception as e:
                print(f"⚠️ Não foi possível excluir o log: {e}")
        else:
            logging.warning("⚠️ Nenhum arquivo de log disponível para envio.")

        # ✅ ESSA LINHA É ESSENCIAL
        return jsonify({
            "success": False,
            "log": [{"type": "error", "message": "❌ Erro interno no servidor. Verifique os logs."}]
        }), 500


@api_bp.route('/equipes', methods=['POST'])
def obter_equipes():
    file = request.files.get('csvFile')
    ignorar_sabados = request.form.get('ignorarSabados', 'true') == 'true'
    tipo_relatorio = request.form.get('tipoRelatorio', 'Auditoria')

    if not file or not file.filename.lower().endswith('csv'):
        return jsonify({"success": False, "error": "Arquivo CSV inválido"}), 400

    filename = secure_filename(file.filename)
    filename = f"{uuid.uuid4().hex[:8]}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        df = carregar_dados(filepath, ignorar_sabados, tipo_relatorio)

        df['EquipeTratada'] = df['Equipe'].apply(mapear_equipe)

        equipes = sorted(df['EquipeTratada'].dropna().unique().tolist())
        logging.info(f"Equipes extraídas: {len(equipes)}")

        return jsonify({"success": True, "equipes": equipes})
    
    except Exception as e:
        logging.exception("Erro ao processar CSV para extração de equipes.")
        return jsonify({"success": False, "error": str(e)}), 500
    
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
