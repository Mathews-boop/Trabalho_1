from enum import IntEnum
from vulnerabilidades import Vulnerabilidade

class TipoAtivo(IntEnum):
    NOTEBOOK = 1
    SERVIDOR = 2
    ROTEADOR = 3
    APLICACAO_WEB = 4
    BANCO_DE_DADOS = 5
    REDE_DE_IMPRESSORA = 6


class Ativo:
    def __init__(self, identificador: int, nome: str, responsavel: str, setor: str, tipo: TipoAtivo):
        self.identificador = identificador
        self.nome = nome
        self.responsavel = responsavel
        self.setor = setor
        self.tipo = TipoAtivo(tipo)
        self.vulnerabilidades: list[Vulnerabilidade] = []

    def adicionar_vulnerabilidade(self, vulnerabilidade: Vulnerabilidade):
        self.vulnerabilidades.append(vulnerabilidade)

    def contar_vulnerabilidades(self) -> int:
        return len(self.vulnerabilidades)

    def para_dicionario(self) -> dict:
        return {
            'identificador': self.identificador,
            'nome': self.nome,
            'responsavel': self.responsavel,
            'setor': self.setor,
            'tipo': int(self.tipo),
            'vulnerabilidades': [v.para_dicionario() for v in self.vulnerabilidades]
        }

@classmethod
def de_dicionario(cls, dados: dict) -> 'Ativo':
    ativo = cls(
        identificador = int(dados['identificador']),
        nome = dados['nome'],
        responsavel = dados['responsavel'],
        setor = dados['setor'],
        tipo = TipoAtivo(dados['tipo'])
    )
    for v_dados in dados.get('vulnerabilidades', []):
        ativo.adicionar_vulnerabilidade(Vulnerabilidade.de_dicionario(v_dados))
    return ativo

def exibir(self):
    print(f'\n[ID: {self.identificador}] {self.nome} ({self.tipo.name})')
    print(f'  Responsável: {self.responsavel} | Setor/Localização: {self.setor}')
    print(f'  Vulnerabilidades registradas ({self.contar_vulnerabilidades()}):')
    if not self.vulnerabilidades:
        print('   -> Ativo sem vulnerabilidades registradas.')
    else:
        for v in self.vulnerabilidades:
            v.exibir()