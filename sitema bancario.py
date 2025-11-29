import textwrap


def menu():
    menu = """\n
    -------- Bem-vindo ao Seu Banco --------
    ==== Escolha uma opção =====
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q]  Sair
    => """
    return input(textwrap.dedent(menu)).strip().lower()


def ler_valor(msg):
    """Lê um valor numérico com validação."""
    try:
        return float(input(msg))
    except ValueError:
        print("\n@@@ Valor inválido! @@@")
        return None


def depositar(saldo, valor, extrato, /):
    if valor and valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! Valor inválido. @@@")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor <= 0:
        print("\n@@@ Valor inválido! @@@")

    elif valor > saldo:
        print("\n@@@ Operação falhou! Saldo insuficiente. @@@")

    elif valor > limite:
        print("\n@@@ Operação falhou! Limite de saque excedido. @@@")

    elif numero_saques >= limite_saques:
        print("\n@@@ Operação falhou! Número máximo de saques atingido. @@@")

    else:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip()

    if filtrar_usuario(cpf, usuarios):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (rua, nro - bairro - cidade/UF): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("\n=== Usuário criado com sucesso! ===")


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n@@@ Usuário não encontrado. @@@")
        return None

    print("\n=== Conta criada com sucesso! ===")
    return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}


def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada! @@@")
        return

    for conta in contas:
        linha = f"""
        Agência:\t{conta['agencia']}
        Conta:\t\t{conta['numero_conta']}
        Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 40)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = ler_valor("Informe o valor do depósito: ")
            if valor is not None:
                saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = ler_valor("Informe o valor do saque: ")
            if valor is not None:
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\nObrigado por usar nosso banco! Volte sempre.")
            break

        else:
            print("\n@@@ Opção inválida! Tente novamente. @@@")


main()
