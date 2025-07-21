import pandas as pd
import os
import re

def limpar_numero_br(numero):
    # Remove tudo que não for dígito
    numero = re.sub(r'\D', '', str(numero))

    # Remove prefixo +55, 0055 ou apenas 55
    if numero.startswith('0055'):
        numero = numero[4:]
    elif numero.startswith('55'):
        numero = numero[2:]

    # Se sobrou exatamente 11 dígitos (com 9 depois do DDD), remove o 9
    if len(numero) == 11 and numero[2] == '9':
        numero = numero[:2] + numero[3:]

    # Se agora temos 10 dígitos (DDXXXXXXXX), adiciona prefixo 55
    if len(numero) == 10:
        numero = '55' + numero

    # Valida se está no formato correto final
    if numero.startswith('55') and len(numero) == 12:
        return numero

    # Se não for válido, retorna vazio
    return ''

def carregar_numeros_equipes():
    url = os.getenv("PLANILHA_EQUIPES_URL")  # Deve ser o link CSV do Google Sheets
    df = pd.read_csv(url, usecols=[0, 1], skiprows=1)

    # Renomear colunas
    df.columns = ['Equipe', 'Numero']

    # Remover linhas com célula vazia em Equipe ou Numero
    df.dropna(subset=['Equipe', 'Numero'], inplace=True)

    # Padronizar nomes das equipes
    df['Equipe'] = df['Equipe'].astype(str).str.strip().str.upper()

    # Aplicar limpeza aos números
    df['Numero'] = df['Numero'].apply(limpar_numero_br)

    # Remover linhas com números vazios ou inválidos
    df = df[df['Numero'] != '']

    # Retorna um dicionário: {'OPS': '556399999999', 'LOJA 75': '556398887777'}
    return dict(zip(df['Equipe'], df['Numero']))
