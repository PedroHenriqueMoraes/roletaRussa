import random
import time
import pygame
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from criarDb import Jogadores

DATABASE_URL = "sqlite:///players.db"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def criar_revolver():
    # Criar uma nova lista embaralhada para cada revólver
    revolver = ['vazio','vazio','vazio','vazio','vazio','BALA']
    random.seed(time.time())  # Nova seed para cada revólver criado
    random.shuffle(revolver)  # Embaralha a lista antes de retornar
    return revolver

def atirar(jogador_lista):
    print("Você puxou o gatilho!")
    # Nova seed baseada no tempo atual para cada tiro
    random.seed(time.time())
    
    # Se a lista estiver vazia, não há o que escolher
    if not jogador_lista:
        return None
        
    # Pega um índice aleatório da lista
    index = random.randint(0, len(jogador_lista) - 1)
    cartucho = jogador_lista[index]
    print("\n", cartucho)
    return cartucho

def remover(jogador_obj, lista_atual):
    # Remove um 'vazio' da lista atual
    if 'vazio' in lista_atual:
        lista_atual.remove('vazio')
        # Atualiza a lista do jogador no banco de dados
        jogador_obj.lista = lista_atual
        session.add(jogador_obj)  # Marca o objeto para atualização
        session.commit()  # Salva as alterações
    print(f"Lista atual: {lista_atual}")
    return lista_atual

def cartasdavez():
    cartas = ['4', '8', '1', '+2', '7']
    # Nova seed para cada rodada de cartas
    random.seed(time.time())
    # Embaralhar as cartas antes de escolher
    random.shuffle(cartas)
    print("\nCartas disponíveis (embaralhadas):", cartas)
    cartaDaVez = cartas[0]  # Pega a primeira carta do baralho embaralhado
    print(f'A carta da vez é: {cartaDaVez}')
    return cartaDaVez

def iniciar():
    # Seed inicial para o jogo
    random.seed(time.time())
    acao = input('jogar insira o comando: ')

    jogo_iniciado = True
    numeroJogadores = int(input('quantos jogadores? '))

    # Limpa jogadores anteriores se houver
    session.query(Jogadores).delete()
    session.commit()

    for n in range(numeroJogadores):
        usuario = input('nome de usuario: ')
        # Cria uma nova cópia da lista para cada jogador
        # Nova seed para cada jogador criado
        random.seed(time.time() + n)  # Adiciona n para garantir seeds diferentes
        novoUser = Jogadores(usuario=usuario, vida=int(5), lista=criar_revolver())
        session.add(novoUser)
        session.commit()

    input()
    print("O jogo foi iniciado!")
    print('~'* 50)

    if acao == 'jogar':
        cartasdavez()

        while acao == 'jogar':
            jogadorDaVez = input('jogador da vez: ')
            time.sleep(1)
            
            # Busca o jogador atual
            player = session.query(Jogadores).filter(Jogadores.usuario == jogadorDaVez).first()

            if player is None:
                print(f"Jogador {jogadorDaVez} não encontrado ou foi eliminado!")
                jogadores_restantes = session.query(Jogadores).all()
                if len(jogadores_restantes) > 0:
                    print("\nJogadores ainda vivos:")
                    for j in jogadores_restantes:
                        print(f"- {j.usuario}")
                continue

            comando = input('acao: ')
            if comando == 'atirar':
                # Busca o estado mais recente do jogador
                current_player = session.query(Jogadores).filter(Jogadores.usuario == jogadorDaVez).first()
                # Cria uma cópia da lista atual para manipulação
                lista_atual = current_player.lista.copy()
                
                print(f"Lista antes do tiro: {lista_atual}")
                cartucho = atirar(jogador_lista=lista_atual)

                if cartucho == 'vazio':
                    # Atualiza a lista removendo um 'vazio'
                    lista_atual = remover(current_player, lista_atual)
                    print(f"Lista após remover: {lista_atual}")
                    
                    pygame.mixer.init()
                    pygame.mixer.music.load('sonsTiro/falhar.mp3')
                    pygame.mixer.music.play()
                    time.sleep(1)
                    pygame.mixer.music.stop()
                    cartasdavez()

                else:
                    pygame.mixer.init()
                    pygame.mixer.music.load('sonsTiro/tiro.mp3')
                    pygame.mixer.music.play()
                    time.sleep(2)
                    pygame.mixer.music.stop()
                    print(f"Lista final: {lista_atual}")
                    print(f"{jogadorDaVez} morreu, BURRO!!!")
                    session.delete(current_player)
                    session.commit()
                    
                    jogadores_restantes = session.query(Jogadores).all()
                    if len(jogadores_restantes) == 0:
                        print("Fim de jogo! Todos os jogadores morreram!")
                        return
                    cartasdavez()

            elif comando == 'sair':
                print("Você saiu do jogo.")
                exit()

iniciar()