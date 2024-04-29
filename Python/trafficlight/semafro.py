import pygame
import random
import time
import pickle


pygame.init()


largura = 400
altura = 300
tamanho_quadrado = 100


branco = (255, 255, 255)
preto = (0, 0, 0)
verde = (0, 128, 0)
amarelo = (255, 255, 0)
vermelho = (255, 0, 0)


janela = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Jogo do Semaforo")


def desenhar_tabuleiro(tabuleiro):
    janela.fill(branco)

    tabuleiro_x = (janela.get_width() - largura) // 2
    tabuleiro_y = (janela.get_height() - altura) // 2

    for linha in range(3):
        for coluna in range(4):
            quadrado_x = tabuleiro_x + coluna * tamanho_quadrado
            quadrado_y = tabuleiro_y + linha * tamanho_quadrado

            pygame.draw.rect(
                janela,
                preto,
                (
                    quadrado_x,
                    quadrado_y,
                    tamanho_quadrado,
                    tamanho_quadrado,
                ),
                2,
            )

            if tabuleiro[linha][coluna] == 1:
                pygame.draw.circle(
                    janela,
                    verde,
                    (
                        int(quadrado_x + tamanho_quadrado / 2),
                        int(quadrado_y + tamanho_quadrado / 2),
                    ),
                    40,
                    0,
                )
            elif tabuleiro[linha][coluna] == 2:
                pygame.draw.circle(
                    janela,
                    amarelo,
                    (
                        int(quadrado_x + tamanho_quadrado / 2),
                        int(quadrado_y + tamanho_quadrado / 2),
                    ),
                    40,
                    0,
                )
            elif tabuleiro[linha][coluna] == 3:
                pygame.draw.circle(
                    janela,
                    vermelho,
                    (
                        int(quadrado_x + tamanho_quadrado / 2),
                        int(quadrado_y + tamanho_quadrado / 2),
                    ),
                    40,
                    0,
                )

    pygame.display.update()


def verificar_vitoria(tabuleiro, jogador):
    for linha in range(3):
        if (
            tabuleiro[linha][0] == jogador
            and tabuleiro[linha][1] == jogador
            and tabuleiro[linha][2] == jogador
        ):
            return True

        elif (
            tabuleiro[linha][1] == jogador
            and tabuleiro[linha][2] == jogador
            and tabuleiro[linha][3] == jogador
        ):
            return True
    for coluna in range(4):
        if (
            tabuleiro[0][coluna] == jogador
            and tabuleiro[1][coluna] == jogador
            and tabuleiro[2][coluna] == jogador
        ):
            return True
    if (
        tabuleiro[0][0] == jogador
        and tabuleiro[1][1] == jogador
        and tabuleiro[2][2] == jogador
    ):
        return True
    if (
        tabuleiro[0][3] == jogador
        and tabuleiro[1][2] == jogador
        and tabuleiro[2][1] == jogador
    ):
        return True
    return False


def realizar_jogada(tabuleiro, linha, coluna, jogador_atual):
    if tabuleiro[linha][coluna] == 0:
        tabuleiro[linha][coluna] = jogador_atual
    elif tabuleiro[linha][coluna] == 1:
        tabuleiro[linha][coluna] = 2
    elif tabuleiro[linha][coluna] == 2:
        tabuleiro[linha][coluna] = 3

    return tabuleiro


def exibir_mensagem(tela, mensagem):
    fonte = pygame.font.Font(None, 24)
    texto = fonte.render(mensagem, True, preto)
    posicao = texto.get_rect(center=(960, 510))
    tela.blit(texto, posicao)


def jogada_bot(tabuleiro):
    jogadas_disponiveis = []
    for linha in range(3):
        for coluna in range(4):
            if tabuleiro[linha][coluna] == 0:
                jogadas_disponiveis.append((linha, coluna))

    for linha in range(3):
        for coluna in range(4):
            if tabuleiro[linha][coluna] == 0:
                tabuleiro[linha][coluna] = 1
                if verificar_vitoria(tabuleiro, 1):
                    return tabuleiro

                tabuleiro[linha][coluna] = 0

            elif tabuleiro[linha][coluna] == 1:
                tabuleiro[linha][coluna] = 2
                if verificar_vitoria(tabuleiro, 2):
                    return tabuleiro

                tabuleiro[linha][coluna] = 1
            elif tabuleiro[linha][coluna] == 2:
                tabuleiro[linha][coluna] = 3
                if verificar_vitoria(tabuleiro, 2):
                    return tabuleiro

                tabuleiro[linha][coluna] = 2

    for linha, coluna in jogadas_disponiveis:
        if tabuleiro[linha][coluna] == 0:
            tabuleiro[linha][coluna] = 1
            return tabuleiro

    return tabuleiro


def exibir_menu():
    menu_rodando = True
    while menu_rodando:
        janela.fill(branco)

        fonte_titulo = pygame.font.Font(None, 36)
        texto_titulo = fonte_titulo.render("Jogo do Semaforo", True, preto)
        posicao_titulo = texto_titulo.get_rect(center=(960, 300))

        fonte_opcao = pygame.font.Font(None, 24)
        texto_jogar = fonte_opcao.render("1. Jogar", True, preto)
        texto_carregar = fonte_opcao.render("2. Carregar jogo salvo", True, preto)
        texto_descricao = fonte_opcao.render("3. Descrição", True, preto)
        texto_sair = fonte_opcao.render("4. Sair", True, preto)
        posicao_jogar = texto_jogar.get_rect(center=(960, 400))
        posicao_carregar = texto_carregar.get_rect(center=(960, 450))
        posicao_descricao = texto_descricao.get_rect(center=(960, 500))
        posicao_sair = texto_sair.get_rect(center=(960, 550))

        janela.blit(texto_titulo, posicao_titulo)
        janela.blit(texto_jogar, posicao_jogar)
        janela.blit(texto_carregar, posicao_carregar)
        janela.blit(texto_descricao, posicao_descricao)
        janela.blit(texto_sair, posicao_sair)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_rodando = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    menu_rodando = False
                    inserir_nome_jogador(tela)
                    iniciar_jogo()
                elif event.key == pygame.K_2:
                    menu_rodando = False
                    carregar_jogo()
                elif event.key == pygame.K_3:
                    menu_rodando = False
                    exibir_descricao()
                elif event.key == pygame.K_4:
                    menu_rodando = False
                    pygame.quit()


def salvar_jogo(tabuleiro, jogador_atual):
    jogo_salvo = {"tabuleiro": tabuleiro, "jogador_atual": jogador_atual}
    with open("jogo_salvo.pickle", "wb") as arquivo:
        pickle.dump(jogo_salvo, arquivo)


def carregar_jogo():
    try:
        with open("jogo_salvo.pickle", "rb") as arquivo:
            jogo_salvo = pickle.load(arquivo)
        tabuleiro = jogo_salvo["tabuleiro"]
        jogador_atual = jogo_salvo["jogador_atual"]
        iniciar_jogo(tabuleiro, jogador_atual)
    except FileNotFoundError:
        print("Nenhum jogo salvo encontrado.")


def primeira_jogada():
    if random.randint(0, 1) == 0:
        return 1
    else:
        return 2


def inserir_nome_jogador(tela):
    global nome_jogador
    fonte = pygame.font.Font(None, 50)
    input_box = pygame.Rect(760, 540, 400, 50)
    cor_ativa = pygame.Color("lightskyblue3")
    cor_inativa = pygame.Color("gray15")
    cor_texto = pygame.Color("black")
    ativo = False
    texto = ""

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(evento.pos):
                    ativo = not ativo
                else:
                    ativo = False
            if evento.type == pygame.KEYDOWN:
                if ativo:
                    if evento.key == pygame.K_RETURN:
                        nome_jogador = texto
                        return
                    elif evento.key == pygame.K_BACKSPACE:
                        texto = texto[:-1]
                    else:
                        texto += evento.unicode

        tela.fill((255, 255, 255))
        cor = cor_ativa if ativo else cor_inativa
        pygame.draw.rect(tela, cor, input_box, 2)

        texto_surface = fonte.render(texto, True, cor_texto)
        tela.blit(texto_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(tela, cor_texto, input_box, 2)

        exibir_mensagem(tela, "Insira o nome do jogador 1:")

        pygame.display.flip()
        clock.tick(30)


largura_tela = 1920
altura_tela = 1080
tela = pygame.display.set_mode((largura_tela, altura_tela))
clock = pygame.time.Clock()


def primeira_jogada():
    if random.randint(0, 1) == 0:
        return 1
    else:
        return 2


def exibir_vencedor(jogador):
    janela.fill(branco)
    fonte_vencedor = pygame.font.Font(None, 48)
    texto_vencedor = fonte_vencedor.render(
        "Jogador {} venceu!".format(jogador), True, preto
    )
    posicao_vencedor = texto_vencedor.get_rect(center=(960, 600))
    janela.blit(texto_vencedor, posicao_vencedor)
    pygame.display.update()
    time.sleep(2)


def iniciar_jogo(tabuleiro=None, jogador_atual=None):
    tabuleiro_x = (janela.get_width() - largura) // 2
    tabuleiro_y = (janela.get_height() - altura) // 2

    if tabuleiro is None or jogador_atual is None:
        tabuleiro = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        jogador_atual = primeira_jogada()

    jogo_rodando = True
    mouse_pressionado = False
    while jogo_rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogo_rodando = False
            elif event.type == pygame.MOUSEBUTTONDOWN and jogador_atual == 1:
                mouse_pressionado = True
            elif event.type == pygame.MOUSEBUTTONUP and jogador_atual == 1:
                if mouse_pressionado:
                    mouse_pressionado = False
                    pos = pygame.mouse.get_pos()
                    coluna_clicada = (pos[0] - tabuleiro_x) // tamanho_quadrado
                    linha_clicada = (pos[1] - tabuleiro_y) // tamanho_quadrado

                    if (
                        linha_clicada >= 0
                        and linha_clicada < len(tabuleiro)
                        and coluna_clicada >= 0
                        and coluna_clicada < len(tabuleiro[0])
                    ):
                        tabuleiro = realizar_jogada(
                            tabuleiro, linha_clicada, coluna_clicada, jogador_atual
                        )
                        if verificar_vitoria(tabuleiro, jogador_atual):
                            print("Jogador", jogador_atual, "venceu!")
                            jogo_rodando = False
                        jogador_atual = 2

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    salvar_jogo(tabuleiro, jogador_atual)

            if jogador_atual == 2 and jogo_rodando:
                tabuleiro = jogada_bot(tabuleiro).copy()
                if verificar_vitoria(tabuleiro, jogador_atual):
                    print("Bot venceu!")
                    jogo_rodando = False
            jogador_atual = 1

        desenhar_tabuleiro(tabuleiro)

    exibir_vencedor(jogador_atual)


def exibir_descricao():
    descricao_rodando = True
    while descricao_rodando:
        janela.fill(branco)

        fonte_titulo = pygame.font.Font(None, 36)
        texto_titulo = fonte_titulo.render("Regras", True, preto)
        posicao_titulo = texto_titulo.get_rect(center=(960, 300))

        fonte_descricao = pygame.font.Font(None, 24)
        texto_descricao = fonte_descricao.render("", True, preto)
        texto_descricao2 = fonte_descricao.render(
            "Em cada jogada, cada jogador realiza uma das seguintes ações:", True, preto
        )
        texto_descricao3 = fonte_descricao.render(
            "1- Coloca uma peça verde num quadrado vazio;", True, preto
        )
        texto_descricao4 = fonte_descricao.render(
            "2- Substitui uma peça verde por uma peça amarela;", True, preto
        )
        texto_descricao5 = fonte_descricao.render(
            "3- Substitui uma peça amarela por uma peça vermelha.", True, preto
        )
        texto_descricao6 = fonte_descricao.render("", True, preto)
        texto_descricao7 = fonte_descricao.render(
            "De notar que as peças vermelhas não podem ser substituidas. Isto significa que o jogo tem de terminar sempre.",
            True,
            preto,
        )
        texto_descricao9 = fonte_descricao.render(
            "À medida que o tabuleiro fica com peças vermelhas, é inevitável que surja uma linha de três peças.",
            True,
            preto,
        )
        texto_descricao8 = fonte_descricao.render(
            "Pressione 'Enter' para voltar para o menu", True, preto
        )
        posicao_descricao = texto_descricao.get_rect(center=(650, 350))

        fonte_voltar = pygame.font.Font(None, 24)
        texto_voltar = fonte_voltar.render("", True, preto)
        posicao_voltar = texto_voltar.get_rect(center=(950, 600))

        janela.blit(texto_titulo, posicao_titulo)
        janela.blit(texto_descricao, posicao_descricao)
        janela.blit(texto_descricao2, (posicao_descricao.x, posicao_descricao.y + 30))
        janela.blit(texto_descricao3, (posicao_descricao.x, posicao_descricao.y + 60))
        janela.blit(texto_descricao4, (posicao_descricao.x, posicao_descricao.y + 90))
        janela.blit(texto_descricao5, (posicao_descricao.x, posicao_descricao.y + 120))
        janela.blit(texto_descricao6, (posicao_descricao.x, posicao_descricao.y + 150))
        janela.blit(texto_descricao7, (posicao_descricao.x, posicao_descricao.y + 180))
        janela.blit(texto_descricao8, (posicao_descricao.x, posicao_descricao.y + 260))
        janela.blit(texto_descricao9, (posicao_descricao.x, posicao_descricao.y + 210))
        janela.blit(texto_voltar, posicao_voltar)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                descricao_rodando = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    descricao_rodando = False
                    exibir_menu()


exibir_menu()
