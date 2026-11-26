import json
import os
from ativos import Ativo

ARQUIVO_DADOS = 'inventario.json'


def salvar_dados(ativos: dict[int, Ativo], caminho: str = ARQUIVO_DADOS):
    dados_serializados = {
        str(identificador): ativo.para_dicionario()
        for identificador, ativo in ativos.items()
    }
    with open(caminho, 'w', encoding = 'utf-8') as arquivo:
        json.dump(dados_serializados, arquivo, indent = 4, ensure_ascili = False)

def carregar_dados(caminho: str = ARQUIVO_DADOS) -> dict[int, Ativo]:
    if not os.path.exists(caminho):
        return {}
    try:
        with open(caminho, 'r', encoding = 'utf-8') as arquivo:
            dados_brutos = json.load(arquivo)
        return {
            int(chave): Ativo.de_dicionario(valor)
            for chave, valor in dados_brutos.items()
        }
    except (json.JSONDecodeError, KeyError, ValueError):
        print('Aviso: Arquivo de dados corrompido ou vazio. Iniciando base limpa.')
        return {}


    