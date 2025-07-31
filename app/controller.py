from app.processamento.csv_reader import carregar_dados
from app.whatsapp.mensagem import gerar_mensagens
from app.whatsapp.enviar_mensagem import enviar_whatsapp
from app.whatsapp.numeros_equipes import carregar_numeros_equipes
from app.processamento.log import configurar_log
from collections import defaultdict
from datetime import datetime
import logging
import pandas as pd

def processar_csv(caminho_csv, ignorar_sabados, tipo_relatorio, equipes_selecionadas=None):
    nome_arquivo_log = configurar_log()
    logging.info(f">>> Iniciando processamento CSV: {caminho_csv}")
    logging.info(f">>> Parâmetros: ignorar_sabados={ignorar_sabados}, tipo={tipo_relatorio}")
    
    df = carregar_dados(caminho_csv, ignorar_sabados, tipo_relatorio)

    # ✅ Renomeia colunas comuns
    df.columns = df.columns.str.strip()
    df.rename(columns={
        "Funcionário": "Nome",
        "Funcionario": "Nome",
        "Colaborador": "Nome",
        "Data do ponto": "Data",
        "Data Registro": "Data"
    }, inplace=True)
    print("🧪 Colunas carregadas:", df.columns.tolist())

    df["EquipeTratada"] = df["EquipeTratada"].astype(str).str.strip().str.upper()

    mensagens_por_grupo = gerar_mensagens(df, tipo_relatorio)
    numero_equipe = carregar_numeros_equipes()
    
    mensagens_por_equipe_data = defaultdict(lambda: defaultdict(list))
    logs = []
    equipes_sem_numero = []
    stats = {"total": 0, "equipes": set(), "sucesso": 0, "erro": 0}

    for (nome, data), mensagem in mensagens_por_grupo.items():
        equipe_match = df.loc[(df["Nome"] == nome) & (df["Data"] == data), "EquipeTratada"]
        if equipe_match.empty:
            continue
        equipe = equipe_match.iloc[0]
        mensagens_por_equipe_data[equipe][data].append(mensagem)

    for equipe, datas in sorted(mensagens_por_equipe_data.items()):
        equipe_normalizada = str(equipe).strip().upper()
        if equipes_selecionadas:
            equipes_normalizadas = {e.strip().upper() for e in equipes_selecionadas}
            if equipe_normalizada not in equipes_normalizadas:
                continue

        numero = numero_equipe.get(equipe_normalizada)
        if not numero or numero.strip().lower() in ["nan", "none", ""]:
            equipes_sem_numero.append(equipe)
            stats["erro"] += 1
            continue

        df_equipe = df[df["EquipeTratada"] == equipe_normalizada]
        subgrupos = []

        if df_equipe["Equipe"].str.contains("KRA", case=False, na=False).any():
            subgrupos.append(("KRA", df_equipe[df_equipe["Equipe"].str.contains("KRA", case=False, na=False)]))
        if df_equipe["Equipe"].str.contains("HPS", case=False, na=False).any():
            subgrupos.append(("HPS", df_equipe[df_equipe["Equipe"].str.contains("HPS", case=False, na=False)]))
        if not subgrupos:
            subgrupos.append((None, df_equipe))

        for sufixo, sub_df in subgrupos:
            mensagens_sub = gerar_mensagens(sub_df, tipo_relatorio)
            datas_sub = defaultdict(list)
            for (nome, data), mensagem in mensagens_sub.items():
                if pd.isna(mensagem):
                    continue
                datas_sub[data].append(mensagem)

            if not datas_sub:
                continue

            titulo = f"EQUIPE {equipe}" + (f" | {sufixo}" if sufixo else "")
            mensagem_final = f"*{titulo}*\n\n"

            for data in sorted(datas_sub.keys(), key=lambda d: datetime.strptime(d, "%d/%m/%Y")):
                mensagens_validas = [m.strip() for m in datas_sub[data] if m and m.strip()]
                if not mensagens_validas:
                    continue
                mensagem_final += f"*NO DIA {data}:*\n"
                for m in mensagens_validas:
                    mensagem_final += f"• {m}\n"
                mensagem_final += "\n"

            try:
                enviar_whatsapp(numero, mensagem_final.strip(), equipe)
                logs.append({"type": "success", "message": f" Mensagem enviada para {titulo}"})
                stats["sucesso"] += 1
            except Exception as e:
                logs.append({"type": "error", "message": f" Erro ao enviar para {titulo}: {str(e)}"})
                stats["erro"] += 1

            stats["total"] += 1
            stats["equipes"].add(equipe)

    if equipes_sem_numero:
        logs.append({"type": "warning", "message": f" Números não encontrados para: {', '.join(equipes_sem_numero)}"})

    stats["equipes"] = len(stats["equipes"])
    logging.info(">>> Finalizando processamento CSV. Total de equipes: %d", stats["total"])
    return logs, stats
