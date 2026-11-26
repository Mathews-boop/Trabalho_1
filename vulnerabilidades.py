from enum import IntEnum

class Severidade(IntEnum):
    BAIXA = 1
    MÉDIA = 2
    ALTA = 3
    CRÍTICA = 4

class StatusVulnerabilidade(IntEnum):
    ABERTA = 1
    EM_TRATAMENTO = 2
    RETIFICADA = 3
    ACEITA_COMO_RISCO = 4

class Vulnerabilidade:
    def __init__(self, descricao: str, categoria: str, severidade: Severidade, status: StatusVulnerabilidade):
        self.descricao = descricao
        self.categoria = categoria
        self.severidade = Severidade(severidade)
        self.status = StatusVulnerabilidade(status)


    def para_dicionario(self) -> dict:
        return{
            'descricao': self.descricao,
            'categoria': self.categoria,
            'severidade': int(self.severidade),
            'status': int(self.status)

        }

@classmethod
def de_dicionario(cls, dados: dict) -> 'Vulnerabilidade':
    return cls(
        descricao = dados['descricao'],
        categoria = dados['categoria'],
        severidade = Severidade(dados['severidade']),
        status = StatusVulnerabilidade(dados['satus'])
    )

def exibir(self):
    print(f' - Descrição: {self.descricao} | Categoria: {self.categoria} | '
          f' - Severidade: {self.severidade.name} | Status: {self.satus.name}')