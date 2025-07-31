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

# === Templates para relatório de Ocorrências ===
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

# === Converte horas para minutos ===
def converter_horas_para_minutos(valor_horas):
    """
    Converte uma string de horas no formato 'HH:MM' para minutos totais.
    Exemplo: '01:30' -> 90 minutos
    """
    try:
        if not isinstance(valor_horas, str) or ":" not in valor_horas:
            return 0
        
        valor_limpo = valor_horas.strip()
        horas, minutos = valor_limpo.split(":")
        return int(horas) * 60 + int(minutos)
    except (ValueError, AttributeError):
        return 0

# === Formata valor de horas ===
def formatar_horas(valor):
    if not isinstance(valor, str) or ":" not in valor:
        return valor
    horas, minutos = valor.strip().split(":")
    horas_int = int(horas)
    minutos_int = int(minutos)
    if horas_int == 0 and minutos_int == 0:
        return "00:00"
    elif horas_int == 0:
        return f"{horas}:{minutos} minutos"
    elif minutos_int == 0:
        return f"{horas}:{minutos} horas"
    else:
        return f"{horas}:{minutos} horas"

def normalizar(texto):
    return unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode().strip().lower()

# === Monta mensagens para relatório de Ocorrências ===
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
            return (
                f"*{nome}* em *{data}* apresentou: _{motivo}_.\n"
                f"Ação pendente: *{acao}*."
            )

    mensagens = df.groupby(["Nome", "Data"]).apply(
        lambda g: "\n".join([gerar_linha(row) for _, row in g.iterrows()])
    )
    return mensagens.dropna()

# === Monta mensagens por colaborador + data para relatório de Auditoria ===
def gerar_mensagem(grupo):
    nome = grupo["Nome"].iloc[0]
    data = grupo["Data"].iloc[0]
    ocorrencias = grupo.set_index("Ocorrência")["Valor"].astype(str).to_dict()

    # 💡 Regra: ignorar se tiver falta + horas e for justificada
    tem_falta = "Falta" in ocorrencias
    tem_horas = "Horas Faltantes" in ocorrencias
    falta_valor = normalizar(ocorrencias.get("Falta", ""))
    falta_justificada = falta_valor in ["justificada", "abonada"]

    if tem_falta and tem_horas and falta_justificada:
        return None
    if tem_falta and falta_justificada:
        return None

    # 🆕 NOVA REGRA: Ignorar se horas faltantes for menor que 1 hora (60 minutos)
    if tem_horas and not tem_falta:  # Apenas horas faltantes, sem falta
        horas_faltantes_valor = ocorrencias.get("Horas Faltantes", "")
        minutos_faltantes = converter_horas_para_minutos(horas_faltantes_valor)
        
        if minutos_faltantes < 60:  # Menos de 1 hora
            return None  # Ignora a mensagem

    if tem_falta and tem_horas:
        # Mesmo com falta, verifica se as horas são menores que 1 hora
        horas_faltantes_valor = ocorrencias.get("Horas Faltantes", "")
        minutos_faltantes = converter_horas_para_minutos(horas_faltantes_valor)
        
        if minutos_faltantes < 60:  # Menos de 1 hora
            # Se tem falta mas horas < 1h, envia apenas mensagem de falta
            return f"*{nome}* _faltou_. Foi verificado o motivo?"
        else:
            # Falta + horas >= 1h, envia mensagem completa
            horas = formatar_horas(ocorrencias["Horas Faltantes"])
            return f"*{nome}* _faltou e ficou devendo_ *{horas}*. Foi verificado o motivo da falta?"

    msgs = []
    mensagens_set = set()

    # Verifica se há duplicidade entre as duas ocorrências
    tem_ambas_horas_extras = (
        "Horas extras" in ocorrencias and
        "Mais de duas horas extras" in ocorrencias and
        ocorrencias["Horas extras"] == ocorrencias["Mais de duas horas extras"]
    )

    for ocorr, valor in ocorrencias.items():
        if tem_ambas_horas_extras and ocorr == "Mais de duas horas extras":
            continue

        # 🆕 FILTRO ADICIONAL: Ignora "Horas Faltantes" menores que 1 hora
        if ocorr == "Horas Faltantes":
            minutos_faltantes = converter_horas_para_minutos(valor)
            if minutos_faltantes < 60:
                continue  # Pula esta ocorrência

        tpl = TEMPLATES.get(ocorr)
        if not tpl:
            continue

        # Regra extra para horas extras curtas
        if ocorr == "Horas extras":
            try:
                h, m = map(int, valor.strip().split(":"))
                total_min = h * 60 + m
                if total_min < 120:
                    continue
            except:
                pass

        msg = tpl.format(
            nome=nome,
            data=data,
            valor=valor,
            horas=formatar_horas(valor)
        ).strip()

        # Garante que mensagens idênticas não sejam adicionadas 2x
        if msg and msg not in mensagens_set:
            msgs.append(msg)
            mensagens_set.add(msg)

    # Retorna None se tudo foi filtrado
    return "\n".join(msgs) if msgs else None

# === Gera todas as mensagens agrupadas por Nome + Data ===
def gerar_mensagens(df, tipo_relatorio):
    if tipo_relatorio == "Auditoria":
        mensagens = df.groupby(["Nome", "Data"], group_keys=False).apply(gerar_mensagem, include_groups=True)
    elif tipo_relatorio == "Ocorrências":
        mensagens = gerar_mensagens_ocorrencias(df)
    else:
        raise ValueError("Tipo de relatório inválido. Escolha \"Auditoria\" ou \"Ocorrências\".")
    return mensagens.dropna()
