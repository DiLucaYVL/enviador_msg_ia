import pandas as pd

def processar_ocorrencias(df):
    # Lógica para processar as colunas 'Motivo' e 'Ação pendente'
    # e gerar as mensagens específicas para o relatório de ocorrências.
    # Esta função será chamada pelo controller.
    
    def gerar_linha_ocorrencia(row):
        nome = row["Nome"]
        motivo = row["Motivo"]
        acao_pendente = row["Ação pendente"]

        return (
            f"*{nome}* apresentou o seguinte problema: _{motivo}_.\n"
            f"Ação pendente: *{acao_pendente}*."
        )

    # Agrupar por Nome e Data para consolidar as mensagens por ocorrência
    mensagens_ocorrencias = df.groupby(["Nome", "Data"]).apply(
        lambda g: "\n".join([gerar_linha_ocorrencia(row) for _, row in g.iterrows()])
    )
    return mensagens_ocorrencias.dropna()


