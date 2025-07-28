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
    configurar_log()
    df = carregar_dados(caminho_csv, ignorar_sabados, tipo_relatorio)

    # 🔍 Normaliza para filtro de equipes funcionar corretamente
    df["EquipeTratada"] = df["EquipeTratada"].astype(str).str.strip().str.upper()

    mensagens_por_grupo = gerar_mensagens(df, tipo_relatorio)
    numero_equipe = carregar_numeros_equipes()
    
    mensagens_por_equipe_data = defaultdict(lambda: defaultdict(list))
    logs = []
    equipes_sem_numero = []
    stats = {
        "total": 0,
        "equipes": set(),
        "sucesso": 0,
        "erro": 0
    }

    for (nome, data), mensagem in mensagens_por_grupo.items():
        equipe_match = df.loc[(df["Nome"] == nome) & (df["Data"] == data), "EquipeTratada"]
        if equipe_match.empty:
            continue
        equipe = equipe_match.iloc[0]
        mensagens_por_equipe_data[equipe][data].append(mensagem)

    for equipe, datas in sorted(mensagens_por_equipe_data.items()):
        equipe = str(equipe).strip().upper()
        equipe_normalizada = equipe.strip().upper()

        # 🎯 Aplica filtro por equipes selecionadas
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

        # 🔀 Subdividir por KRA e HPS na coluna original 'Equipe'
        subgrupos = []

        if df_equipe["Equipe"].str.contains("KRA", case=False, na=False).any():
            sub_kra = df_equipe[df_equipe["Equipe"].str.contains("KRA", case=False, na=False)]
            subgrupos.append(("KRA", sub_kra))

        if df_equipe["Equipe"].str.contains("HPS", case=False, na=False).any():
            sub_hps = df_equipe[df_equipe["Equipe"].str.contains("HPS", case=False, na=False)]
            subgrupos.append(("HPS", sub_hps))

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

            titulo = f"EQUIPE {equipe}"
            if sufixo:
                titulo += f" | {sufixo}"

            mensagem_final = f"*{titulo}*\n\n"
            for data in sorted(datas_sub.keys(), key=lambda d: datetime.strptime(d, "%d/%m/%Y")):
                mensagem_final += f"*NO DIA {data}:*\n"
                for m in datas_sub[data]:
                    mensagem_final += f"• {m.strip()}\n"
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
        lista_equipes = ", ".join(equipes_sem_numero)
        logs.append({"type": "warning", "message": f" Números não encontrados para a(s) equipe(s): {lista_equipes}"})

    stats["equipes"] = len(stats["equipes"])
    logging.info(">>> Finalizando processamento CSV. Total de equipes: %d", stats["total"])
    return logs, stats
