from app.processamento.csv_reader import carregar_dados
from app.whatsapp.mensagem import gerar_mensagens
from app.whatsapp.enviar_mensagem import enviar_whatsapp
from app.whatsapp.numeros_equipes import carregar_numeros_equipes
from app.processamento.log import configurar_log
from collections import defaultdict
from datetime import datetime
import logging

def processar_csv(caminho_csv, ignorar_sabados, equipes_selecionadas=None):
    logging.info(">>> ENTROU EM /enviar <<<")
    configurar_log()
    df = carregar_dados(caminho_csv, ignorar_sabados)
    mensagens_por_grupo = gerar_mensagens(df)

    numero_equipe = carregar_numeros_equipes()

    
    mensagens_por_equipe_data = defaultdict(lambda: defaultdict(list))
    logs = []
    equipes_sem_numero = []  # 👈 acumula as equipes sem número
    stats = {
        "total": 0,
        "equipes": set(),
        "sucesso": 0,
        "erro": 0
    }

    for (nome, data), mensagem in mensagens_por_grupo.items():
        equipe = df.loc[(df['Nome'] == nome) & (df['Data'] == data), 'EquipeTratada'].iloc[0]
        mensagens_por_equipe_data[equipe][data].append(mensagem)

    for equipe, datas in sorted(mensagens_por_equipe_data.items()):
        equipe = str(equipe).strip().upper()
        equipe_normalizada = equipe.strip().upper()
        numero = numero_equipe.get(equipe_normalizada)

        # Filtrar equipes se necessário
        if equipes_selecionadas and equipe_normalizada not in {e.strip().upper() for e in equipes_selecionadas}:
            continue
       

        if not numero or numero.strip().lower() in ["nan", "none", ""]:
            equipes_sem_numero.append(equipe)
            stats["erro"] += 1
            continue

        mensagem_final = f"*EQUIPE {equipe.upper()}*\n\n"
        for data in sorted(datas.keys(), key=lambda d: datetime.strptime(d, "%d/%m/%Y")):
            mensagem_final += f"*NO DIA {data}:*\n"
            for m in datas[data]:
                mensagem_final += f"• {m.strip()}\n"
            mensagem_final += "\n"
        
        try:
            enviar_whatsapp(numero, mensagem_final.strip(), equipe)
            logs.append({"type": "success", "message": f" Mensagem enviada para {equipe}"})
            stats["sucesso"] += 1
        except Exception as e:
            logs.append({"type": "error", "message": f" Erro ao enviar para {equipe}: {str(e)}"})
            stats["erro"] += 1

        stats["total"] += 1
        stats["equipes"].add(equipe)

    if equipes_sem_numero:
        lista_equipes = ", ".join(equipes_sem_numero)
        logs.append({"type": "warning", "message": f" Números não encontrados para a(s) equipe(s): {lista_equipes}"})

    stats["equipes"] = len(stats["equipes"])
    logging.info(">>> Finalizando processamento CSV. Total de equipes:", stats["total"])
    return logs, stats
