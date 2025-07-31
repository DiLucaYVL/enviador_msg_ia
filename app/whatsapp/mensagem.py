import unicodedata

# === Templates para relatório de Auditoria ===
TEMPLATES = {
    "Menos de 1 hora de intervalo": "*{nome}* teve menos de 1 hora de intervalo. _Intervalo registrado_: *{valor}*. Qual o motivo de não ter feito a pausa completa?",
    "Mais de 10 horas de jornada": "*{nome}* trabalhou mais de 10 horas. _Total acumulado_: *{valor}*. Isso está previsto na escala?",
    "Mais de 6 dias de trabalho consecutivos": "*{nome}* está com mais de 6 dias consecutivos de trabalho. Qual o motivo dessa carga contínua?",
    "Mais de duas horas extras": "*{nome}* fez mais de 2 horas extras. _Total_: *{valor}*. Foi autorizado previamente?",
    "Falta": "*{nome}* _faltou_. Foi verificado o motivo?",
    "Horas Faltantes": "*{nome}* ficou devendo *{horas}*.",
    "Interjornada insuficiente": "*{nome}* teve interjornada menor que 11h. _Tempo registrado_: *{horas}*. Houve compensação prevista?",
    "Intrajornada insuficiente": "*{nome}* teve pausa de almoço menor que 1h. _Tempo registrado_: *{horas}*. Qual seria o motivo de não ter tirado o horário de almoço?",
    "Horas extras": "*{nome}* fez mais de 2 horas extras. _Total_: *{valor}*. Foi autorizado previamente?"
}

TEMPLATES_OCORRENCIAS = {
    ("Número de pontos menor que o previsto", "Colaborador solicitar ajuste"):
        "*{nome}* registrou menos pontos que o normal. Houve abono, folga ou falta no restante do período? Se sim, confira as horas trabalhadas: *mais de 4h exige 15min de intervalo; mais de 6h exige pelo menos 1h*. Se não for nenhum desses casos, faça apenas o ajuste necessário.",
    ("Número de pontos menor que o previsto", "Gestor corrigir lançamento de exceção"):
        "*{nome}* registrou menos pontos que o normal. Houve abono, folga ou falta no restante do período? Se sim, confira as horas trabalhadas: *mais de 4h exige 15min de intervalo; mais de 6h exige pelo menos 1h*. Se não for nenhum desses casos, faça apenas o ajuste necessário.",
    ("Número de pontos menor que o previsto", "Gestor aprovar solicitação de ajuste"):
        "*{nome}* registrou menos pontos que o normal. Houve abono, folga ou falta no restante do período? Se sim, confira as horas trabalhadas: *mais de 4h exige 15min de intervalo; mais de 6h exige pelo menos 1h*. Se não for nenhum desses casos, faça apenas o ajuste necessário.",
    ("Número errado de pontos", "Colaborador solicitar ajuste"):
        "*{nome}* apresentou número incorreto de pontos. Houve abono, folga ou falta no restante do período? Se sim, confira as horas trabalhadas: *mais de 4h exige 15min de intervalo; mais de 6h exige pelo menos 1h*. Se não for nenhum desses casos, faça apenas o ajuste necessário.",
    ("Possui pontos durante exceção", "Gestor corrigir lançamento de exceção"):
        "*{nome}* teve pontos durante período de exceção. Gestor precisa corrigir o lançamento.",
}

def converter_horas_para_minutos(valor_horas):
    try:
        if not isinstance(valor_horas, str) or ":" not in valor_horas:
            return 0
        horas, minutos = valor_horas.strip().split(":")
        return int(horas) * 60 + int(minutos)
    except:
        return 0

def formatar_horas(valor):
    if not isinstance(valor, str) or ":" not in valor:
        return valor
    horas, minutos = valor.strip().split(":")
    h, m = int(horas), int(minutos)
    if h == 0 and m == 0:
        return "00:00"
    if h == 0:
        return f"{horas}:{minutos} minutos"
    if m == 0:
        return f"{horas}:{minutos} horas"
    return f"{horas}:{minutos} horas"

def normalizar(texto):
    if not isinstance(texto, str):
        return ""
    return unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode().strip().lower()

def gerar_mensagens_ocorrencias(df):
    def gerar_linha(row):
        nome = row["Nome"]
        data = row["Data"]
        motivo = row["Motivo"]
        acao = row["Ação pendente"]
        chave = (motivo, acao)
        tpl = TEMPLATES_OCORRENCIAS.get(chave)
        if tpl:
            return tpl.format(nome=nome, data=data)
        else:
            return f"*{nome}* em *{data}* apresentou: _{motivo}_.\nAção pendente: *{acao}*."

    mensagens = df.groupby(["Nome", "Data"]).apply(
        lambda g: "\n".join([gerar_linha(row) for _, row in g.iterrows()])
    )
    return mensagens.dropna()

def gerar_mensagem(grupo):
    nome = grupo["Nome"].iloc[0]
    data = grupo["Data"].iloc[0]
    ocorrencias = grupo.set_index("Ocorrência")["Valor"].astype(str).to_dict()
    ocorrencias_norm = {normalizar(k): normalizar(v) for k, v in ocorrencias.items()}

    falta_justificada_ou_abonada = grupo.get("FaltaAbonadaJustificada", False).any()
    tem_falta = "falta" in ocorrencias_norm
    tem_horas_faltantes = "horas faltantes" in ocorrencias_norm

    # Caso especial: falta + horas faltantes no mesmo dia (ambos não justificados)
    if tem_falta and tem_horas_faltantes and not falta_justificada_ou_abonada:
        horas = ocorrencias.get("Horas Faltantes")
        if horas and converter_horas_para_minutos(horas) >= 60:
            return f"*{nome}* _faltou e ficou devendo_ *{formatar_horas(horas)}*. Foi verificado o motivo da falta?"

    msgs = []
    mensagens_set = set()

    tem_ambas_horas_extras = (
        "horas extras" in ocorrencias_norm and
        "mais de duas horas extras" in ocorrencias_norm and
        ocorrencias.get("Horas extras") == ocorrencias.get("Mais de duas horas extras")
    )

    for index, row in grupo.iterrows():
        ocorr = row["Ocorrência"]
        valor = row["Valor"]
        if not isinstance(ocorr, str) or ocorr.strip() == "":
            continue

        ocorr_norm = normalizar(ocorr)

        if ocorr_norm == "horas faltantes" and falta_justificada_ou_abonada:
            continue
        if ocorr_norm == "falta" and row.get("FaltaAbonadaJustificada", False):
            continue
        if tem_ambas_horas_extras and ocorr_norm == "mais de duas horas extras":
            continue
        if ocorr_norm == "horas faltantes" and converter_horas_para_minutos(valor) < 60:
            continue
        if ocorr_norm == "horas extras":
            try:
                h, m = map(int, valor.strip().split(":"))
                if h * 60 + m < 120:
                    continue
            except:
                continue

        tpl = TEMPLATES.get(ocorr.strip())
        if not tpl:
            continue

        msg = tpl.format(
            nome=nome,
            data=data,
            valor=valor,
            horas=formatar_horas(valor)
        ).strip()

        if msg and msg not in mensagens_set:
            msgs.append(msg)
            mensagens_set.add(msg)

    return "\n".join(msgs) if msgs else None

def gerar_mensagens(df, tipo_relatorio):
    if tipo_relatorio == "Auditoria":
        if 'FaltaAbonadaJustificada' not in df.columns:
            df['FaltaAbonadaJustificada'] = False
        mensagens = df.groupby(["Nome", "Data"], group_keys=False).apply(gerar_mensagem, include_groups=True)
    elif tipo_relatorio == "Ocorrências":
        mensagens = gerar_mensagens_ocorrencias(df)
    else:
        raise ValueError("Tipo de relatório inválido. Escolha \"Auditoria\" ou \"Ocorrências\".")
    return mensagens.dropna()