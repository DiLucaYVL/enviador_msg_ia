# Mapeamento dos tipos de motivos para o relatório de ocorrências
MOTIVOS_OCORRENCIAS = {
    "Número de pontos menor que o previsto": "Número de pontos menor que o previsto",
    "Número errado de pontos": "Número errado de pontos",
    "Possui pontos durante exceção": "Possui pontos durante exceção"
}

# Mapeamento dos tipos de ações pendentes para o relatório de ocorrências
ACOES_PENDENTES = {
    "Colaborador solicitar ajuste": "Colaborador solicitar ajuste",
    "Gestor aprovar solicitação de ajuste": "Gestor aprovar solicitação de ajuste",
    "Gestor corrigir lançamento de exceção": "Gestor corrigir lançamento de exceção"
}

def validar_motivo(motivo):
    """Valida se o motivo está na lista de motivos válidos"""
    return motivo in MOTIVOS_OCORRENCIAS

def validar_acao_pendente(acao):
    """Valida se a ação pendente está na lista de ações válidas"""
    return acao in ACOES_PENDENTES

def obter_motivos_validos():
    """Retorna a lista de motivos válidos"""
    return list(MOTIVOS_OCORRENCIAS.keys())

def obter_acoes_validas():
    """Retorna a lista de ações pendentes válidas"""
    return list(ACOES_PENDENTES.keys())

