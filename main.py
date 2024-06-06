import json
import os

cardapio = "cardapio.json"
reservas = "reservas.json"
pedidos = "pedidos.json"


def ler_dados(arquivo):
    if not os.path.exists(arquivo): 
        return {}
    with open(arquivo, "r") as file: 
        return json.load(file)


def salvar_dados(arquivo, dados):
    
    with open(arquivo, "w") as file:  
        json.dump(dados, file, indent=4) 



def criar_prato(nome, descricao, preco, tipo):
    
    dados = ler_dados(cardapio)  
    prato_id = str(len(dados) + 1)  
    dados[prato_id] = {
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
        "tipo": tipo
    } 
    salvar_dados(cardapio, dados)  
    return prato_id


def ler_pratos(prato_id):
    
    dados = ler_dados(cardapio) 
    return dados.get(prato_id) 


def atualizar_prato(prato_id, nome=None, descricao=None, preco=None, tipo=None):
    
    dados = ler_dados(cardapio)  
    if prato_id in dados:  
        if nome:  
            dados[prato_id]["nome"] = nome
        if descricao:
            dados[prato_id]["descricao"] = descricao
        if preco:
            dados[prato_id]["preco"] = preco
        if tipo:
            dados[prato_id]["tipo"] = tipo
        salvar_dados(cardapio, dados)
        print("\nPedido atualizado com sucesso!")
        return prato_id
    return print("\nPrato não encontrado no cardápio.")


def deletar_prato(prato_id):
    dados = ler_dados(cardapio) 
    if prato_id in dados: 
        del dados[prato_id]
    else:
        return print("\nPrato não encontrado no cardápio.")

    ids_ordenados = sorted(dados.keys(), key = int)
    dados_reindexados = {}
    id_novo = 1
    
    for id in ids_ordenados:
        dados_reindexados[str(id_novo)] = dados[id]
        id_novo += 1
        
    salvar_dados(cardapio, dados_reindexados)
    return print("\nPrato exluído com sucesso!")
    


def listar_pratos():
    dados = ler_dados(cardapio)
    for prato_id, prato in dados.items():
        print(f"ID: {prato_id}, Detalhes: {prato}")
    return dados


def ler_pratos_pelo_nome(nome):
    dados = ler_dados(cardapio)
    pratos_encontrados = []
    for prato_id, prato in dados.items():
        if prato["nome"] == nome:
            pratos_encontrados.append((prato_id, prato))
    return pratos_encontrados



def criar_reserva(numeroMesa, nome, data, hora, n_pessoas):
    
    dados = ler_dados(reservas)  
    reserva_id = str(len(dados) + 1) 
    dados[reserva_id] = {
        "numeroMesa": numeroMesa,
        "nome": nome,
        "data": data,
        "hora": hora,
        "n_pessoas": n_pessoas
    }  
    salvar_dados(reservas, dados)  
    return reserva_id


def ler_reserva(reserva_id):
    
    dados = ler_dados(reservas)  
    return dados.get(reserva_id)  


def atualizar_reserva(reserva_id,
                      numeroMesa=None,
                      nome=None,
                      data=None,
                      hora=None,
                      n_pessoas=None):
    
    dados = ler_dados(reservas)  
    if reserva_id in dados: 
        if numeroMesa:
            dados[reserva_id]["numeroMesa"] = numeroMesa
        if nome: 
            dados[reserva_id]["nome"] = nome
        if data:
            dados[reserva_id]["data"] = data
        if hora:
            dados[reserva_id]["hora"] = hora
        if n_pessoas:
            dados[reserva_id]["n_pessoas"] = n_pessoas
        salvar_dados(reservas, dados)
        print("\nPedido atualizado com sucesso!")
        return reserva_id
    return print("\nReserva não encontrada!")


def deletar_reserva(reserva_id):
    
    dados = ler_dados(reservas) 
    if reserva_id in dados: 
        del dados[reserva_id]
    else:
        return print("\nReserva não encontrada")

    ids_ordenados = sorted(dados.keys(), key = int)
    dados_reindexados = {}
    id_novo = 1
    
    for id in ids_ordenados:
        dados_reindexados[str(id_novo)] = dados[id]
        id_novo += 1
        
    salvar_dados(reservas, dados_reindexados)
    return print("\nReserva deletada.")


def listar_reservas():
    dados = ler_dados(reservas)
    for reserva_id, reserva in dados.items():
        print(f"\nID: {reserva_id}, Detalhes: {reserva}.")
    return dados


def ler_reserva_pelo_nome(nome):
    dados = ler_dados(reservas)
    reservas_encontradas = []
    for reserva_id, reserva in dados.items():
        if reserva["nome"] == nome:
            reservas_encontradas.append((reserva_id, reserva))
    return reservas_encontradas


def criar_pedido(numeroMesa):  

    dados_cardapio = ler_dados(cardapio)
    if not dados_cardapio:
        print("O cardápio está vazio.")
        return

    print("\n--- Cardápio ---")
    for prato_id, prato in dados_cardapio.items():
        print(f"ID: {prato_id}, Nome: {prato["nome"]}, Preço: R$ {prato["preco"]}, Descrição: {prato["descricao"]}")

    pedido_id = str(len(ler_dados(pedidos)) + 1)  
    pratos_selecionados = []
    total = 0

    while True:
        prato_id = input("Digite o ID do prato que deseja adicionar (ou 0 para concluir o pedido): ")
        if prato_id == "0":
            break

        if prato_id in dados_cardapio:
            qtd_porcoes = int(input("Quantidade de porções: "))
            prato = dados_cardapio[prato_id]
            preco_unitario = float(prato["preco"].replace("R$ ", "").replace(",", "."))
            preco_total = preco_unitario * qtd_porcoes
            pratos_selecionados.append({
                "id": prato_id,
                "nome": prato["nome"],
                "quantidade": qtd_porcoes,
                "preco_unitario": preco_unitario,
                "preco_total": preco_total
            })
            total += preco_total
        else:
            print("ID do prato inválido. Tente novamente.")

    observacoes = input("Observações (deixe em branco se não houver): ")

    dados_pedidos = ler_dados(pedidos)
    dados_pedidos[pedido_id] = {
        "numeroMesa": numeroMesa,
        "pratos": pratos_selecionados,
        "obs": observacoes,
        "total": total
    }

    salvar_dados(pedidos, dados_pedidos)
    print("\nPedido criado com sucesso!")

    print("\n--- Detalhes do Pedido ---")
    print(f"Pedido ID: {pedido_id}")
    print(f"Número da Mesa: {numeroMesa}")
    for prato in pratos_selecionados:
        print(f"Prato: {prato["nome"]}, Quantidade: {prato["quantidade"]} \nPreço Unitário: R$ {prato["preco_unitario"]:.2f} \nPreço Total: R$ {prato["preco_total"]:.2f}")
    print(f"Observações: {observacoes}")
    print(f"Total: R$ {total:.2f}")
    return pedido_id


def ler_pedido(pedido_id):  
    dados = ler_dados(pedidos) 
    return dados.get(pedido_id)  


def atualizar_pedido(pedido_id): 
    dados_pedidos = ler_dados(pedidos)  
    dados_cardapio = ler_dados(cardapio)  
    
    if pedido_id not in dados_pedidos:
        print("\nPedido não encontrado!")
        return
    
    pedido = dados_pedidos[pedido_id]

    print("\n--- Cardápio ---")
    for prato_id, prato in dados_cardapio.items():
        print(f"ID: {prato_id}, Nome: {prato['nome']}, Preço: R$ {prato['preco']}, Descrição: {prato['descricao']}")
    
    prato_id_atualizar = input("Digite o ID do prato que deseja atualizar no pedido: ")
    
    prato_existente = None
    for prato in pedido["pratos"]:
        if prato["id"] == prato_id_atualizar:
            prato_existente = prato
            break
    
    if not prato_existente:
        print("Prato não encontrado no pedido.")
        return
    
    pedido["pratos"].remove(prato_existente)
    preco_total = 0

    if prato_id_atualizar in dados_cardapio:
        qtd_porcoes = int(input("Quantidade de porções: "))
        prato = dados_cardapio[prato_id]
        preco_unitario = float(prato["preco"].replace("R$ ", "").replace(",", "."))
        preco_total = preco_unitario * qtd_porcoes
        pedido["pratos"].append({
            "id": prato_id,
            "nome": prato["nome"],
            "quantidade": qtd_porcoes,
            "preco_unitario": preco_unitario,
            "preco_total": preco_total
        })
    else:
        print("ID do novo prato inválido. Tente novamente.")
        return

    salvar_dados(pedidos, dados_pedidos)
    print("\nPedido atualizado com sucesso!")
    
    print("\n--- Detalhes do Pedido Atualizado ---")
    print(f"Pedido ID: {pedido_id}")
    print(f"Número da Mesa: {pedido['numeroMesa']}")
    for prato in pedido["pratos"]:
        print(f"Prato: {prato['nome']}, Quantidade: {prato['quantidade']}, Preço Unitário: R$ {prato['preco_unitario']:.2f}, Preço Total: R$ {prato['preco_total']:.2f}")
    print(f"Observações: {pedido['obs']}")
    print(f"Total: R$ {pedido['total']:.2f}")
    return pedido_id


def deletar_pedido(pedido_id):
    dados = ler_dados(pedidos) 
    if pedido_id in dados: 
        del dados[pedido_id]
    else:
        return print("\nPedido não encontrado no sistema.")

    ids_ordenados = sorted(dados.keys(), key = int)
    dados_reindexados = {}
    id_novo = 1
    
    for id in ids_ordenados:
        dados_reindexados[str(id_novo)] = dados[id]
        id_novo += 1
        
    salvar_dados(pedidos, dados_reindexados)
    return print("\nPedido excluído com sucesso!")

def deletar_prato(prato_nome):
    dados = ler_dados(cardapio)
    if prato_nome in dados: 
        del dados[prato_nome]
    else:
        return print("\nPrato não encontrado no sistema.")

    ids_ordenados = sorted(dados.keys(), key = int)
    dados_reindexados = {}
    id_novo = 1
    
    for id in ids_ordenados:
        dados_reindexados[str(id_novo)] = dados[id]
        id_novo += 1
        
    salvar_dados(cardapio, dados_reindexados)
    return print("\nPrato excluído com sucesso!")


def listar_pedidos():
    dados = ler_dados(pedidos)
    for pedido_id, pedido in dados.items():
        print(f"\nID: {pedido_id}, Detalhes: {pedido}.")
    return dados


def ler_pedido_mesa(numeroMesa):
    dados = ler_dados(pedidos)
    mesa_encontrada = []
    for pedido_id, pedido in dados.items():
        if pedido["numeroMesa"] == numeroMesa:
            mesa_encontrada.append((pedido_id, pedido))
    return mesa_encontrada


def sair_funcionário():
    opcao = int(input("\n1 - Realizar outra operação \n2 - Sair do programa \n"))
    print("\n")
    if opcao == 1:
        menu_funcionario()
    elif opcao == 2:
        print("\nObrigado, até a próxima!")
        exit()
    else:
        print("\nOpção inválida. Tente novamente!")
        sair_funcionário()


def sair_cliente():
    opcao = int(input("\n1 - Realizar outra operação \n2 - Sair do programa \n"))
    print("\n")
    if opcao == 1:
        menu_cliente()
    elif opcao == 2:
        print("\nObrigada pela preferência! Até a próxima!")
        exit()
    else:
        print("\nOpção inválida. Tente novamente!")
        sair_cliente()


def menu_cardapio():
    while True:
        print("\nBem vindo ao Menu destinado ao Cardápio!\n")
        print("O que deseja fazer hoje?\n")
        opcao = int(input(
            "1 - Ver Cardápio \n2 - Editar Item \n3 - Adicionar Item \n4 - Remover Item \n5 - Achar prato pelo nome \n6 - Achar prato pelo id \n7 - Voltar ao menu principal \n8 - Sair do programa\n"))
        print("\n")
        if opcao == 1:
            listar_pratos()
            sair_funcionário()
        elif opcao == 2:
            atualizar_prato(input("\nID do prato: "), input("Nome: "), input("Descricao do prato: "),
                            input("Preco do prato: R$ "), input("Qual é o tipo do prato: "))
            sair_funcionário()
        elif opcao == 3:
            id = criar_prato(input("\nNome: "), input("Descricao do prato: "),
                                     input("Preco do prato: R$ "), input("Tipo do prato: "))
            print("O id do prato é: ", id)
            sair_funcionário()
        elif opcao == 4:
            deletar_prato(input("\nDigite o ID do prato que deseja deletar: "))
            sair_funcionário()
        elif opcao == 5:
            nome = input("Nome do prato: ")
            pratos = ler_pratos_pelo_nome(nome)
            if pratos:
                for prato_id, prato in pratos:
                    print(f"ID: {prato_id}, Detalhes: {prato}")
            else:
                print("Prato não encontrado.")
            sair_funcionário()
        elif opcao == 6:
            print(ler_pratos(input("ID do prato: ")))
            sair_funcionário()
        elif opcao == 7:
            menu_principal()
            break
        elif opcao == 8:
            print("Obrigado, até a próxima!")
            exit()
        else:
            print("Opção inválida. Tente novamente!")


def menu_reservas():
    while True:
        print("Bem vindo ao Menu destinado às Reservas!\n")
        print("O que deseja fazer hoje?\n")
        opcao = int(input(
            "1 - Ver Reservas \n2 - Editar reserva \n3 - Criar Reserva \n4 - Remover reserva \n5 - Achar reserva pelo nome \n6 - Achar reserva pelo id \n7 - Voltar ao menu principal \n8 - Sair do programa\n"))
        print("\n")
        if opcao == 1:
            listar_reservas()
            sair_funcionário()
        elif opcao == 2:
            print("O id da sua reserva é: ",
                  atualizar_reserva(input("ID da reserva: "), input("Nome: "), input("Data da reserva: "),
                                    input("Horário da Reserva: "), input("Número de pessoas: ")))
            sair_funcionário()
        elif opcao == 3:
            id = criar_reserva(input("Número da mesa: "), input("Nome: "), input("Data da reserva: "),
                               input("Horário da Reserva: "), input("Número de pessoas: "))
            print("O id da sua reserva é: ", id)
            sair_funcionário()
        elif opcao == 4:
            deletar_reserva(input("Digite o ID da reserva que deseja deletar: "))
            sair_funcionário()
        elif opcao == 5:
            nome = input("\nNome da pessoa que fez a reserva: ")
            reservas = ler_reserva_pelo_nome(nome)
            if reservas:
                for reserva_id, reserva in reservas:
                    print(f"ID: {reserva_id}, Detalhes: {reserva}")
            else:
                print("Reserva não encontrada.")
            sair_funcionário()
        elif opcao == 6:
            print(ler_reserva(input("Id da reserva: ")))
            sair_funcionário()           
        elif opcao == 7:
            menu_principal()
            break
        elif opcao == 8:
            print("Obrigado, até a próxima!")
            exit()
        else:
            print("Opção inválida. Tente novamente!")


def menu_pedido():
    while True:
        print("\nBem vindo ao Menu destinado aos Pedidos!\n")
        print("O que deseja fazer hoje?\n")
        opcao = int(input("1 - Ver Pedidos \n2 - Voltar ao menu principal \n3 - Sair do programa\n"))
        print("\n")
        if opcao == 1:
            listar_pedidos()
            sair_funcionário()
        elif opcao == 2:
            menu_principal()
            break
        elif opcao == 3:
            print("\nObrigado, até a próxima!")
            exit()
        else:
            print("\nOpção inválida. Tente novamente!")


def menu_cliente():
    while True:
        print("\nOlá cliente! O que deseja fazer hoje?\n")
        opcao = int(input(
            "1 - Ver Cardápio \n2 - Fazer Pedido \n3 - Atualizar Pedido \n4 - Excluir Pedido \n5 - Ver Pedido pelo ID \n6 - Ver Pedido pela Mesa \n7 - Ver Reserva pelo ID \n8 - Ver Reserva pelo Nome \n9 - Voltar ao Menu Principal \n10 - Sair do programa\n"))
        print("\n")
        if opcao == 1:
            listar_pratos()
            sair_cliente()
        elif opcao == 2:
            criar_pedido(input("Digite o numero da Mesa: "))
            sair_cliente()
        elif opcao == 3:
            pedido_id = input("ID do pedido: ")
            pedido = ler_pedido(pedido_id) ##verificar se o ID existe antes de atualizar o pedido.
            if pedido:
                atualizar_pedido(pedido_id)
                print("Pedido atualizado com sucesso!")
            else:
                print("Pedido não encontrado. Verifique o ID fornecido.")
            sair_cliente()
        elif opcao == 4:
            deletar_pedido(input("Digite o ID do pedido que deseja deletar: "))
            sair_cliente()
        elif opcao == 5:
            print(ler_pedido(input("Id do pedido: ")))
            sair_cliente()
        elif opcao == 6:
            numero_mesa = input("Número da Mesa: ")
            pedidos = ler_pedido_mesa(numero_mesa)
            if pedidos:
                for pedido_id, pedido in pedidos:
                    print(f"ID: {pedido_id}, Detalhes: {pedido}")
            else:
                print("Pedido não encontrado.")
            sair_cliente()           
        elif opcao == 7:
            print(ler_reserva(input("Id da reserva: ")))
            sair_cliente()
        elif opcao == 8:
            nome = input("Nome da pessoa que fez a reserva: ")
            reservas = ler_reserva_pelo_nome(nome)
            if reservas:
                for reserva_id, reserva in reservas:
                    print(f"ID: {reserva_id}, Detalhes: {reserva}")
            else:
                print("Reserva não encontrada.")
            sair_cliente()
        elif opcao == 9:
            menu_principal()
            break
        elif opcao == 10:
            print("Obrigada pela preferência! Até a próxima!")
            exit()
        else:
            print("Opção inválida. Tente novamente!\n")


def menu_funcionario():
    while True:
        print("Olá colaborador! Onde você trabalhará hoje?\n")
        opcao = int(input(
            "1 - Menu do Cardápio \n2 - Menu de Reservas \n3 - Menu dos Pedidos \n4 - Voltar ao Menu Principal \n5 - Sair do programa\n"))
        print("\n")
        if opcao == 1:
            menu_cardapio()
        elif opcao == 2:
            menu_reservas()
        elif opcao == 3:
            menu_pedido()
        elif opcao == 4:
            menu_principal()
            break
        elif opcao == 5:
            print("Obrigado. Até a próxima colaborado!")
            exit()
        else:
            print("Opção inválida. Tente novamente!")


def menu_principal():
    print("***** Bem vindos ao Restaurante Maracujenios!! ***** \n \n")
    while True:
        opcao = int(input("Você Deseja entrar como: \n1 - Cliente \n2 - Funcionario \n3 - Sair\n"))
        print("\n")
        if opcao == 1:
            menu_cliente()
        elif opcao == 2:
            menu_funcionario()
        elif opcao == 3:
            print("\nObrigada. Até a próxima!")
            exit()
        else:
            print("\nOpção inválida. Tente novamente!\n")


menu_principal()
