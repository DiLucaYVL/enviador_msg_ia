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

# === Funções auxiliares ===

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

# === Geração de mensagem individual por grupo (Nome + Data) ===

def gerar_mensagem(grupo):
    nome = grupo["Nome"].iloc[0]
    data = grupo["Data"].iloc[0]
    ocorrencias = grupo.set_index("Ocorrência")["Valor"].astype(str).to_dict()

    # Normaliza as chaves e valores
    ocorrencias_norm = {normalizar(k): normalizar(v) for k, v in ocorrencias.items()}

    msgs = []
    mensagens_set = set()

    # Verifica se há falta justificada/abonada para a mesma pessoa e data
    # Agora, verifica a nova coluna 'FaltaAbonadaJustificada' no grupo
    falta_justificada_ou_abonada = grupo["FaltaAbonadaJustificada"].any()

    # Ignora duplicidade entre duas ocorrências iguais
    tem_ambas_horas_extras = (
        "horas extras" in ocorrencias_norm and
        "mais de duas horas extras" in ocorrencias_norm and
        ocorrencias.get("Horas extras") == ocorrencias.get("Mais de duas horas extras")
    )

    for index, row in grupo.iterrows(): # Itera sobre as linhas do grupo, não apenas as chaves de ocorrencias
        ocorr = row["Ocorrência"]
        valor = row["Valor"]

        if not isinstance(ocorr, str) or ocorr.strip() == "":
            continue

        ocorr_norm = normalizar(ocorr)
        valor_norm = normalizar(valor)

        # ✅ Regra principal: ignora mensagem de horas faltantes se houver falta justificada
        if ocorr_norm == "horas faltantes" and falta_justificada_ou_abonada:
            continue

        # Ignora a própria ocorrência de Falta se ela for abonada/justificada
        if ocorr_norm == "falta" and row["FaltaAbonadaJustificada"]:
            continue

        if tem_ambas_horas_extras and ocorr_norm == "mais de duas horas extras":
            continue

        if ocorr_norm == "horas faltantes":
            if converter_horas_para_minutos(valor) < 60:
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

# === Gera todas as mensagens agrupadas por Nome + Data ===

def gerar_mensagens(df, tipo_relatorio):
    if tipo_relatorio == "Auditoria":
        # Certifica-se de que a coluna 'FaltaAbonadaJustificada' existe antes de agrupar
        if 'FaltaAbonadaJustificada' not in df.columns:
            df['FaltaAbonadaJustificada'] = False # Default para False se não existir
        mensagens = df.groupby(["Nome", "Data"], group_keys=False).apply(gerar_mensagem, include_groups=True)
    else:
        raise ValueError("Tipo de relatório inválido. Escolha \"Auditoria\" ou \"Ocorrências\".")
    return mensagens.dropna()


