from flask import Blueprint, request, jsonify
from app.controller import processar_csv
from werkzeug.utils import secure_filename
import os
import json
import logging

api_bp = Blueprint('api', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@api_bp.route('/enviar', methods=['POST'])
def enviar():
    print(">>> [ROUTE] /enviar acionado <<<")
    try:
        file = request.files.get('csvFile')
        ignorar_sabados = request.form.get('ignorarSabados', 'true') == 'true'
        debug_mode = request.form.get('debugMode', 'false') == 'true'

        if not file:
            return jsonify({'success': False, 'log': ['❌ Nenhum arquivo CSV enviado.']}), 400

        if not file.filename.lower().endswith('.csv'):
            return jsonify({'success': False, 'log': ['❌ Formato inválido. Envie um arquivo .csv']}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join("uploads", filename)
        file.save(filepath)

        equipes_selecionadas = request.form.get('equipesSelecionadas')
        equipes_selecionadas = set(json.loads(equipes_selecionadas)) if equipes_selecionadas else None

        logging.info(">>> Chamando processar_csv()")
        from app.controller import processar_csv
        logs, stats = processar_csv(filepath, ignorar_sabados, equipes_selecionadas)

        df_debug = None
        if debug_mode:
            from app.processamento.csv_reader import carregar_dados
            df_debug = carregar_dados(filepath, ignorar_sabados).to_json(orient="records", force_ascii=False)

        return jsonify({
            'success': True,
            'log': logs,
            'stats': stats,
            'debug': df_debug if debug_mode else None
        })
    except Exception as e:
        logging.info(f"❌ ERRO EM /enviar: {str(e)}")
        return jsonify({'success': False, 'log': [f"❌ Erro interno no servidor: {str(e)}"]}), 500

@api_bp.route('/equipes', methods=['POST'])
def obter_equipes():
    file = request.files.get('csvFile')
    ignorar_sabados = request.form.get('ignorarSabados', 'true') == 'true'

    if not file or not file.filename.lower().endswith('.csv'):
        return jsonify({'success': False, 'error': 'Arquivo CSV inválido'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join("uploads", filename)
    file.save(filepath)

    from app.processamento.csv_reader import carregar_dados
    df = carregar_dados(filepath, ignorar_sabados)

    from app.processamento.mapear_gerencia import mapear_equipe
    df['EquipeTratada'] = df['Equipe'].apply(mapear_equipe)

    equipes = sorted(df['EquipeTratada'].dropna().unique().tolist())
    logging.info(f"Equipes extraídas: {len(equipes)}")

    return jsonify({'success': True, 'equipes': equipes})

