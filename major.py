from enum import IntEnum
from ativos import Ativo, TipoAtivo
from vulnerabilidades import Vulnerabilidade, Severidade, StatusVulnerabilidade
from permanência import salvar_dados, carregar_dados


def ler_inteiro(mensagem: str) -> int:
    while True:
        try:
            return int(input(mensagem).strip())
        except ValueError:
            print('Erro: Digite um número inteiro válido.')

def ler_texto_nao_vazio(mensagem: str) -> str:
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print('Erro: Este campo não pode ficar vazio.')


def ler_enum(mensagem: str, enum_cls: type[IntEnum]) -> IntEnum:
    opcoes = ', '.join(f'{item.value}-{item.name}' for item in enum_cls)
    while True:
        print(f'Opções disponíveis: {opcoes}')
        codigo = ler_inteiro(mensagem)
        try:
            return enum_cls(codigo)
        except ValueError:
            print('Erro: Código inexistente. Escolha uma das opções listadas.')


def criar_vulnerabilidade_interativa() -> Vulnerabilidade:
    descricao = ler_texto_nao_vazio('Descrição da vulnerabilidade: ')
    categoria = ler_texto_nao_vazio('Categoria (ex: Senha fraca, Falha de config): ')
    severidade = ler_enum('Código da severidade: ', Severidade)
    status = ler_enum('Código do status de tratamento: ', StatusVulnerabilidade)
    return Vulnerabilidade(descricao, categoria, severidade, status)


def cadastrar_ativo(ativos: dict[int, Ativo]):
    print('\n--- Cadastrar Novo Ativo ---')
    identificador = ler_inteiro('ID único do ativo: ')
    if identificador in ativos:
        print(f'Erro: Já existe um ativo cadastrado com o ID {identificador}.')
        return

    nome = ler_texto_nao_vazio('Nome ou hostname do ativo: ')
    responsavel = ler_texto_nao_vazio('Responsável: ')
    setor = ler_texto_nao_vazio('Setor ou localização: ')
    tipo = ler_enum('Código do tipo de ativo: ', TipoAtivo)

    novo_ativo = Ativo(identificador, nome, responsavel, setor, tipo)

    while True:
        adicionar = input('Deseja cadastrar uma vulnerabilidade inicial? (s/n):').strip().lower()
        if adicionar == 's':
            vuln = criar_vulnerabilidade_interativa()
            novo_ativo.adicionar_vulnerabilidade(vuln)
        elif adicionar == 'n':
            break
        else:
            print(" Digite 's' para sim ou 'n' para não. ")

    
    ativos[identificador] = novo_ativo
    salvar_dados(ativos)
    print(f"Ativo '{nome}' cadastrado com sucesso!")


def buscar_ativo(ativos: dict[int, Ativo]):
    print('\n--- Consultar Ativo ---')
    if not ativos:
        print('Nenhum ativo cadastrado no sistema.')
        return
    
    print('1 - Buscar por ID | 2 - Buscar por Nome/Hostname | 3 - Listar todos')
    opcao = input('Escolha o modo de consulta: ').strip()

    if opcao == "1":
        identificador = ler_inteiro('Informe o ID do ativo:')
        ativo = ativos.get(identificador)
        if ativo:
            ativo.exibir()
        else:
            print('Ativo não encontrado para o ID informado.')

    elif opcao == "2":
        termo = ler_texto_nao_vazio('Informe o nome ou hostname: ').lower()
        encontrados = [a for a in ativos.values() if termo in a.nome.lower()]
        if encontrados:
            for ativo in encontrados:
                ativo.exibir()
        else:
            print('Nenhum ativo encontrado com esse nome.')

    elif opcao == "3":
        for ativo in ativos.values():
            ativo.exibir()
    else:
        print('Opção de busca inválida.')


def atualizar_ativo(ativos: dict[int, Ativo]):
    print('\n--- Atualizar Ativo ---')
    identificador = ler_inteiro('Informe o ID do ativo a atualizar:')
    ativo = ativos.get(identificador)
    if not ativo:
        print('Ativo não encontrado.')
        return

    ativo.exibir()
    print('\nPressione ENTER para manter o valor atual.')

    novo_nome = input(f'Novo nome [{ativo.nome}]: ').strip()
    if novo_nome:
        ativo.nome = novo_nome

    novo_resp = input(f'Novo respon´savel [{ativo.responsavel}]:').strip()
    if novo_resp:
        ativo.responsavel = novo_resp

    novo_setor = input(f'Novo setor/localização [{ativo.setor}]: ').strip()
    if novo_setor:
        ativo.setor = novo_setor

    alterar_tipo = input('Deseja alterar o tipo de ativo? (s/n):').strip().lower()
    if alterar_tipo == 's':
        ativo.tipo = ler_enum('Novo código do tipo de ativo:', TipoAtivo)

    salvar_dados(ativos)
    print('Ativo atualizado com sucesso!')

def deletar_ativo(ativos: dict[int, Ativo]):
    print('\n--- Remover Ativo ---')
    identificador = ler_inteiro('Informe o ID do ativo a remover: ')
    ativo = ativos.get(identificador)
    if not ativo:
        print('Ativo não encontrado.')
        return

    confirmacao = input(f"Confirmar a remoção de '{ativo.nome}' e suas {ativo.contar_vulnerabilidades()} vulnerabilidade(s)? (s/n): ").strip().lower()
    if confirmacao == 's':
        ativos.pop(identificador)
        salvar_dados(ativos)
        print('Ativo e vulnerabilidades associadas removidos com sucesso.')
    else:
        print('Operação cancelada.')

    
def adicionar_vulnerabilidade_a_ativo(ativos: dict[int, Ativo]):
    print('\n--- Cadastrar Vulnerabilidade em Ativo ---')
    identificador = ler_inteiro('Informe o ID do ativo: ')
    ativo = ativos.get(identificador)
    if not ativo:
        print('Ativo não encontrado.')
        return

    vuln = criar_vulnerabilidade_interativa()
    ativo.adicionar_vulnerabilidade(vuln)
    salvar_dados(ativos)
    print(f"Vulnerabilidade associada ao ativo '{ativo.nome}' com sucesso!")

def visualizar_vulnerabilidades_ativo(ativos: dict[int, Ativo]):
    print('\n--- Visualizar Vulnerabilidades de um Ativo --- ')
    identificador = ler_inteiro('Informe o ID do ativo: ')
    ativo = ativos.get(identificador)
    if not ativo:
        print('Ativo não encontrado.')
        return

    print(f'\nAtivo: {ativo.nome} (ID: {ativo.identificador})')
    if not ativo.vulnerabilidades:
        print('Este ativo está sem vulnerabilidades registradas.')
    else:
        for v in ativo.vulnerabilidades:
            print(f'- Descrição: {v.descricao} | Severidade: {v.severidade.name} | Status: {v.status.name}')


def menu_principal():
    ativos = carregar_dados
    while True:
        print('\n============================================')
        print('  INVENTÁRIO DE ATIVOS E VULNERABILIDADES TI ')
        print('============================================')
        print('1 - Cadastrar ativo')
        print('2 - Consultar ativo (ID, Nome ou Todos)')
        print('3 - Atualizar ativo')
        print('4 - Remover ativo')
        print('5 - Cadastrar vulnerabilidade em um ativo')
        print('6 - Visualizar vulnerabilidades de um ativo')
        print('0 - Sair')

        opcao = input('Escolha uma opção:').strip()

        if opcao == '1':
            cadastrar_ativo(ativos)
        elif opcao == '2':
            buscar_ativo(ativos)
        elif opcao == '3':
            atualizar_ativo(ativos)
        elif opcao == '4':
            deletar_ativo(ativos)
        elif opcao == '5':
            adicionar_vulnerabilidade_a_ativo(ativos)
        elif opcao == '6':
            visualizar_vulnerabilidades_ativo(ativos)
        elif opcao == '0':
            print('Encerrando o sistema...')
            break
        else:
            print('Opção inválida. Tente novamente.')


if __name__ == '__major__':
    menu_principal()