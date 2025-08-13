import pandas as pd
from app.processamento.mapear_gerencia import mapear_equipe
from app.processamento.motivos_ocorrencias import validar_motivo, validar_acao_pendente

def carregar_dados_ocorrencias(caminho_csv):
    """
    Carrega dados do relatório de ocorrências.
    Ignora as primeiras 4 linhas e as últimas 5 linhas.
    Colunas esperadas: Nome, Equipe, Data, Motivo, Ação pendente
    """
    
    # Ler o CSV ignorando as primeiras 4 linhas e as últimas 5
    df = pd.read_csv(caminho_csv, skiprows=4, skipfooter=5, engine='python')
    
    # Verificar se as colunas necessárias existem
    colunas_esperadas = ['Nome', 'Equipe', 'Data', 'Motivo', 'Ação pendente']
    colunas_faltantes = [col for col in colunas_esperadas if col not in df.columns]
    
    if colunas_faltantes:
        raise ValueError(f"Colunas faltantes no arquivo CSV: {colunas_faltantes}")
    
    # Limpar dados
    df['Data'] = df['Data'].astype(str).str.split(',').str[-1].str.strip() # Remove "Sáb, ", etc
    df['Nome'] = df['Nome'].astype(str).str.strip()
    df['Motivo'] = df['Motivo'].astype(str).str.strip()
    df['Ação pendente'] = df['Ação pendente'].astype(str).str.strip()
    
    # Mapear equipes
    df['EquipeTratada'] = df['Equipe'].apply(mapear_equipe)
    
    # Remover linhas com dados vazios ou inválidos
    df = df.dropna(subset=['Nome', 'Data', 'Motivo', 'Ação pendente'])

    # Valida se os motivos são os que estão listados
    df = df[df['Motivo'].apply(validar_motivo)]
    df = df[df['Ação pendente'].apply(validar_acao_pendente)]    

    return df

