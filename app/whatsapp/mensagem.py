# === Templates com placeholders ===
TEMPLATES = {
    "Mais de 6 dias de trabalho consecutivos": "*{nome}* está com mais de 6 dias consecutivos de trabalho. Qual o motivo dessa carga contínua?",
    "Mais de 10 horas de jornada": "*{nome}* trabalhou mais de 10 horas. _Total acumulado_: *{valor}*. Isso está previsto na escala?",
    "Mais de duas horas extras": "*{nome}* fez mais de 2 horas extras. _Total acumulado_: *{valor}*. Foi autorizado previamente?",
    "Menos de 1 hora de intervalo": "*{nome}* teve menos de 1 hora de intervalo. _Intervalo registrado_: *{valor}*. Qual o motivo de não ter feito a pausa completa?",
    "Falta": "*{nome}* _faltou_. Foi verificado o motivo?",
    "Horas Faltantes": "*{nome}* ficou devendo *{horas}*.",
    "Interjornada insuficiente": "*{nome}* teve interjornada menor que 11h. _Tempo registrado_: *{horas}*. Houve compensação prevista?",
    "Intrajornada insuficiente": "*{nome}* teve pausa de almoço menor que 1h. _Tempo registrado_: *{horas}*. Qual seria o motivo de não ter tirado o horário de almoço?"
}

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

# === Monta a mensagem por colaborador + data ===
def gerar_mensagem(grupo):
    nome = grupo['Nome'].iloc[0]
    data = grupo['Data'].iloc[0]
    ocorrencias = grupo.set_index('Ocorrência')['Valor'].astype(str).to_dict()

    # 💡 Regra nova: ignorar se tiver falta + horas e for justificada
    tem_falta = "Falta" in ocorrencias
    tem_horas = "Horas Faltantes" in ocorrencias
    falta_justificada = ocorrencias.get("Falta", "").strip().lower() == "justificada"

    if tem_falta and tem_horas and falta_justificada:
        return None  # Ignora esse grupo completamente

    # Caso especial: falta + horas (não justificada)
    if tem_falta and tem_horas:
        horas = formatar_horas(ocorrencias["Horas Faltantes"])
        return f"*{nome}* _faltou e ficou devendo_ *{horas}*. Foi verificado o motivo da falta?"

    msgs = []
    for ocorr, valor in ocorrencias.items():
        tpl = TEMPLATES.get(ocorr)
        if not tpl:
            msgs.append(f"[Ocorrência não tratada: {ocorr}]")
            continue

        msg = tpl.format(
            nome=f"{nome}",
            data=data,
            valor=valor,
            horas=formatar_horas(valor)
        )

        # ✅ Regra especial para Horas Faltantes > 03:30
        if ocorr == "Horas Faltantes":
            try:
                h, m = map(int, valor.split(":"))
                total_min = h * 60 + m
                if total_min > 210:  # 3h30 = 210 minutos
                    msg += " Houve falta?"
            except:
                pass  # ignora erro de parsing se não for no formato HH:MM

        msgs.append(msg)

    return "\n".join(msgs)

# === Gera todas as mensagens agrupadas por Nome + Data ===
def gerar_mensagens(df):
    mensagens = df.groupby(['Nome', 'Data'], group_keys=False).apply(gerar_mensagem, include_groups=True)
    return mensagens.dropna()
