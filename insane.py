import pygame
import sys
import random
import math

from random import randint
from pygame.locals import *

pygame.init()
#Versão definitiva 21/10/2024

info = pygame.display.Info()
largura = info.current_w - 20
altura = info.current_h

zombie_death = pygame.mixer.Sound('Sounds/colisser.wav')
dano = pygame.mixer.Sound('Sounds/dano.wav')
projetil_som = pygame.mixer.Sound('Sounds/projetil.wav')
click_sound = pygame.mixer.Sound('Sounds/click1.wav')
direcaoProjetilSom = pygame.mixer.Sound('Sounds/direcaoProjetil.wav')
menu_music = 'Sounds/InsaneMenu2.wav'
game_music = 'Sounds/InsaneGameTheme.wav'
end_music = 'Sounds/End.wav'
atirador_sound = pygame.mixer.Sound('Sounds/atirador.wav')
visualEffect = pygame.mixer.Sound('Sounds/visual_effect_noise.wav')

pontos = 0
rodando = True
xHero = largura / 2
yHero = altura / 2
velHero = 8.0
projetil_ativo = False
xProjetil = xHero
yProjetil = yHero
velocidade_projetil = 30
xZombie = randint(10, 600)
yZombie = randint(10, 600)
fps = pygame.time.Clock()
janela = pygame.display.set_mode((largura, altura), FULLSCREEN) # type: ignore
nomeDaJanela = pygame.display.set_caption('Insane Dreams')
velZombie = 5.5
pause = False
tamanhoxHero = 20
tamanhoyHero = 40
xZombieNovo = randint(20,200)
yZombieNovo = randint(20,200)
zumbisAzuis = []
atiradores = []
posAtiradorX = randint(1,400)
posAtiradorY = randint(20,100)
velAtirador = 4.6
velProjetilAtirador = 15
retangulos = []
projeteis_atirador = []
posicoesAleatoriasX = randint(1,2180)
posicoesAleatoriasY = randint(20,100)


def mostrar_tutorial():
    fonte = pygame.font.Font('fonte/Symtext.ttf', 40)
    mensagem1 = "W  mover-se para cima"
    mensagem2 = "S mover-se para baixo"
    mensagem3 = "D mover-se para direita"
    mensagem4 = "A mover-se para esquerda"

    objetivo = "Seu único objetivo é sobreviver e fazer 200 pontos."

    m_1 = "atirar para cima"
    m_2 = "atirar para direita"
    m_3 = "atirar para esquerda"
    m_4 = "atirar para baixo"

    up_img = pygame.image.load("img/up.png")
    down_img =  pygame.image.load("img/down.png")
    left_img =  pygame.image.load("img/left.png")
    right_img =  pygame.image.load("img/right.png")

    while True:
        janela.fill((0,0,0))
         # Renderiza o texto
        mov_texto1 = fonte.render(mensagem1, True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        mov_texto2 = fonte.render(mensagem2, True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        mov_texto3 = fonte.render(mensagem3, True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        mov_texto4 = fonte.render(mensagem4, True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        ob = fonte.render(objetivo,True,(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        atirar_texto1 = fonte.render(m_1, True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        atirar_texto2 = fonte.render(m_2, True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        atirar_texto3 = fonte.render(m_3, True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        atirar_texto4 = fonte.render(m_4, True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        janela.blit(mov_texto1, (50, 100))
        janela.blit(mov_texto2, (50, 180))
        janela.blit(mov_texto3, (50, 260))
        janela.blit(mov_texto4, (50, 340))

        janela.blit(ob,(ob.get_width()//largura,ob.get_height()+700))


        # Exibe os textos de tiro (coluna direita)
        janela.blit(up_img, (800, 100))  # Exibe a imagem "up" ao lado do texto
        janela.blit(atirar_texto1, (930, 150))  # Texto "atirar para cima"

        janela.blit(right_img, (800, 200))  # Exibe a imagem "right" ao lado do texto
        janela.blit(atirar_texto2, (930, 250))  # Texto "atirar para direita"

        janela.blit(left_img, (800, 300))  # Exibe a imagem "left" ao lado do texto
        janela.blit(atirar_texto3, (930, 350))  # Texto "atirar para esquerda"

        janela.blit(down_img, (800, 400))  # Exibe a imagem "down" ao lado do texto
        janela.blit(atirar_texto4, (930, 450))  # Texto "atirar para baixo"

        
        pygame.display.update()
        pygame.time.wait(100)
        
   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                click_sound.play()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #retorna para a função onde foi chamada
                    click_sound.play()
                    return
              
def gerar_cor_aleatoria():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

def desenhar_circulos_hipnoticos(janela, largura, altura):
    
    for corner in [(0, 0), (0, altura), (largura, 0), (largura, altura)]:
        for i in range(10):
            raio = (pygame.time.get_ticks() % 500) + (i * 10)
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            cor = (r, g, b)

            # Desenha círculos com centro em cada canto
            pygame.draw.circle(janela, cor, corner, int(raio % (largura // 4)), 5)


def desenhar_retangulos_caoticos(janela, largura, altura, lista_retangulos):
    for retangulo in lista_retangulos:
        x, y, largura_ret, altura_ret, cor, velocidade = retangulo
        
        
        x += velocidade[0] * 0.05  
        y += velocidade[1] * 0.05
        
        
        if x < 0:
            x = 0
            velocidade[0] *= -1  # Inverte a direção no eixo X
        elif x + largura_ret > largura:
            x = largura - largura_ret
            velocidade[0] *= -1
        
        if y < 0:
            y = 0
            velocidade[1] *= -1  # Inverte a direção no eixo Y
        elif y + altura_ret > altura:
            y = altura - altura_ret
            velocidade[1] *= -1

        # Desenha o retângulo na nova posição
        pygame.draw.rect(janela, cor, (x, y, largura_ret, altura_ret))
        
        # Atualiza a posição do retângulo na lista
        retangulo[0] = x
        retangulo[1] = y     

def resetar_jogo():
    global pontos, xHero, yHero, projetil_ativo, xProjetil, yProjetil, zumbisAzuis, atiradores, projeteis_atirador, projetil_atirador_ativo,velHero,velocidade_projetil
    pontos = 0
    velHero = 8.0
    velocidade_projetil = 35
    # Resetar a posição do herói
    xHero = largura / 2
    yHero = altura / 2

    # Resetar estado do projetil
    projetil_ativo = False
    xProjetil = xHero
    yProjetil = yHero

    # Resetar inimigos e atiradores
    zumbisAzuis.clear()  # Limpa a lista de zumbis
    atiradores.clear()    # Limpa a lista de atiradores

    
    projeteis_atirador.clear()  # Limpa a lista de projéteis do atirador
    projetil_atirador_ativo = False  # Reseta o estado do projetil do atirador
 


       
def desenhar_botao(texto, cor_botao, cor_texto, posicao, tamanho):
    fonte = pygame.font.Font('fonte/Symtext.ttf', 40)
    texto_surface = fonte.render(texto, True, cor_texto)
    texto_retangulo = texto_surface.get_rect(center=posicao)
    
    botao_rect = pygame.Rect(0, 0, tamanho[0], tamanho[1])
    botao_rect.center = posicao
    
    pygame.draw.rect(janela, cor_botao, botao_rect)
    janela.blit(texto_surface, texto_retangulo)
    
    return botao_rect

def selecionar_dificuldade():
    no_dificuldade = True
    while no_dificuldade:
        janela.fill((0, 0, 0))

        # Criar três botões para selecionar a dificuldade
        botao_facil = desenhar_botao("Fácil", 
                              (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
                              (255, 255, 255),  # Cor do texto
                              (largura // 2, altura // 2 - 60), 
                              (400, 60))
        botao_medio = desenhar_botao("Médio", 
                              (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
                              (255, 255, 255),  # Cor do texto
                              (largura // 2, altura // 2), 
                              (400, 60))
        botao_dificil = desenhar_botao("Difícil", 
                              (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
                              (255, 255, 255),  # Cor do texto
                              (largura // 2, altura // 2 + 60), 
                              (400, 60))

        botao_tutorial = desenhar_botao("Tutorial",
                                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                ((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                                ( (largura // 2, altura // 2 + 120)),
                                (400, 60))
        
        
                             
        pygame.display.update()
        pygame.time.wait(100)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_facil.collidepoint(event.pos):
                    click_sound.play()
                    ajustar_dificuldade("facil")
                    no_dificuldade = False
                elif botao_medio.collidepoint(event.pos):
                    click_sound.play()
                    ajustar_dificuldade("medio")
                    no_dificuldade = False
                elif botao_dificil.collidepoint(event.pos):
                    click_sound.play()
                    ajustar_dificuldade("dificil")
                    no_dificuldade = False
                elif botao_tutorial.collidepoint(event.pos):
                    click_sound.play()
                    mostrar_tutorial()       

def ajustar_dificuldade(nivel):
    global velZombie, velHero, velAtirador, velProjetilAtirador, velocidade_projetil
    resetar_jogo()
    if nivel == "facil":
        velZombie = 2
        velAtirador = 2
    elif nivel == "medio":
        velZombie = 5.5
    elif nivel == "dificil":
        velZombie = 6.5
        velAtirador = 7
        velProjetilAtirador = 10
        velocidade_projetil = 60
        velHero = 15
    
    pygame.mixer.music.stop()
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1)
        

def fade(janela, largura, altura, fade_in=True):
    fade_surface = pygame.Surface((largura, altura))
    fade_surface.fill((0, 0, 0))


    if fade_in:
        alpha_range = range(0, 256, 5) 
    else:
        alpha_range = range(255, -1, -5)  

    for alpha in alpha_range:
        fade_surface.set_alpha(alpha)
        janela.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(50)

def exibirAviso(janela,largura,altura): 
    
    aviso = pygame.image.load('img/warning2.jpeg')
    aviso_f =  pygame.transform.scale(aviso,(largura,altura))
    janela.blit(aviso_f, (0, 0))
    pygame.display.update()
    pygame.time.delay(2000) 
    fade(janela, largura, altura, fade_in=True)
    
    aviso1 = pygame.image.load('img/warning.jpeg')
    aviso1_f = pygame.transform.scale(aviso1,(largura,altura))
    janela.blit(aviso1_f, (0, 0))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    fade(janela, largura, altura, fade_in=True)
                    mostrar_menu()
                    return


def verificar_colisao_hero(projeteis_atirador, xHero, yHero, larguraHero, alturaHero, pontos):
    global posAtiradorX,posAtiradorY,xZombie,yZombie,xZombieNovo,yZombieNovo
    for proj in projeteis_atirador:
        # Verificar se o projétil colide com o herói
        if (proj[0] < xHero + larguraHero and
            proj[0] + 10 > xHero and
            proj[1] < yHero + alturaHero and
            proj[1] + 10 > yHero):
            
            # Colisão detectada
            projeteis_atirador.remove(proj)  # Remover o projétil
            
            # Chamar a função de pontuação
            dano.play()
            pontuacao(pontos)
            resetar_jogo()          
            break 
             
def mover_atirador():
    global posAtiradorY,posAtiradorX,velAtirador,xHero,yHero
    deltaX = xHero - posAtiradorX
    deltaY = yHero - posAtiradorY

    # Calcular a distância
    distancia = (deltaX ** 2 + deltaY ** 2) ** 0.5

    # Apenas mover o atirador se a distância for significativa
    if distancia > 1:  # Um pequeno valor para evitar movimento desnecessário
        # Normalizar a direção e mover na velocidade constante
        direcaoX = deltaX / distancia
        direcaoY = deltaY / distancia

        posAtiradorX += direcaoX * velAtirador
        posAtiradorY += direcaoY * velAtirador
    else:
        # Alinhar o atirador se estiver muito próximo do jogador
        posAtiradorX = xHero
        posAtiradorY = yHero
def atirar_inimigo():
    global projetil_atirador_ativo, projeteis_atirador, xHero, yHero, posAtiradorX, posAtiradorY

    # Verificar se o inimigo está alinhado para atirar
    alinhado_em_x = abs(xHero - posAtiradorX) <= 200
    alinhado_em_y = abs(yHero - posAtiradorY) <= 200
    
    # Atirar somente se estiver alinhado e não houver projétil ativo
    if (alinhado_em_x or alinhado_em_y) and not projetil_atirador_ativo:
        
        projetil_atirador_ativo = True
        atirador_sound.play()

        # Calcular direção normalizada do projétil
        deltaX = xHero - posAtiradorX +1
        deltaY = yHero - posAtiradorY +1
        magnitude = (deltaX ** 2 + deltaY ** 2) ** 0.5
        direcaoX = deltaX / magnitude
        direcaoY = deltaY / magnitude

        # Adicionar o projétil à lista com posição inicial e direção normalizada
        projeteis_atirador.append([posAtiradorX + 25, posAtiradorY + 25, direcaoX, direcaoY])

def atualizar_projeteis():
    global projetil_atirador_ativo, projeteis_atirador, velocidade_projetil, largura, altura
    
    for proj in projeteis_atirador[:]:
        # Atualizar a posição do projétil em direção ao jogador
        proj[0] += proj[2] * velProjetilAtirador # Movimento em X
        proj[1] += proj[3] * velProjetilAtirador  # Movimento em Y

        # Desenhar o projétil
        pygame.draw.rect(janela, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), (proj[0], proj[1], 40, 40))

        
        # Remover projétil se sair da tela
        if proj[0] > largura or proj[0] < 0 or proj[1] > altura or proj[1] < 0:
            projeteis_atirador.remove(proj)

    # Se todos os projéteis foram removidos, liberar o atirador para disparar novamente
    if not projeteis_atirador:
        projetil_atirador_ativo = False                
def regularSom(rodando):
    if rodando:
        while True:
            janela.fill((0, 0, 0))
            fonte1 = pygame.font.Font('fonte/Symtext.ttf', 20)
            textoTela = fonte1.render(
                "Regule o volume da Música e Sons pressionando as teclas de 0 a 5",
                True, 
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            )
            janela.blit(textoTela, (largura // 4, altura // 2))
            pygame.display.update()
            pygame.time.wait(200)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        click_sound.play()
                        volume_mestre = 0.0  # Silenciar tudo
                    elif event.key == pygame.K_1:
                        click_sound.play()
                        volume_mestre = 0.2
                    elif event.key == pygame.K_2:
                        click_sound.play()
                        volume_mestre = 0.4
                    elif event.key == pygame.K_3:
                        click_sound.play()
                        volume_mestre = 0.6
                    elif event.key == pygame.K_4:
                        click_sound.play()
                        volume_mestre = 0.8
                    elif event.key == pygame.K_5:
                        click_sound.play()
                        volume_mestre = 1.0  # Volume máximo
                    if event.key == pygame.K_ESCAPE:
                        click_sound.play()
                        return    
                        
                    # Ajustar o volume da música e de todos os sons
                    pygame.mixer.music.set_volume(volume_mestre)
                    click_sound.set_volume(volume_mestre)
                    zombie_death.set_volume(volume_mestre)
                    dano.set_volume(volume_mestre)

                    # Reproduz o som de clique para confirmar a mudança
                    click_sound.play()                  
        

def mostrar_menu():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)

    no_menu = True
    while no_menu:
        janela.fill((0, 0, 0))
        fonte1 = pygame.font.Font('fonte/Symtext.ttf', 100)
        name = pygame.font.Font('fonte/Symtext.ttf', 20)
        marca = pygame.font.Font('fonte/Symtext.ttf', 30)
        
        apresentar_nome = fonte1.render("INSANE DREAMS", True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        mostre_name = name.render("Criado por DaviZer0", True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        marca_nome = marca.render("®", True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        janela.blit(apresentar_nome, (largura // 2 - apresentar_nome.get_width() // 2, altura // 2 - apresentar_nome.get_height()))
        janela.blit(mostre_name, (largura // 2 - mostre_name.get_width() // 2, altura - 400))
        janela.blit(marca_nome, (largura - apresentar_nome.get_width() +410 , altura//2.5))

        # Exibe a opção de selecionar dificuldade
        botao_dificuldade = desenhar_botao("Jogar", (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (largura // 2, altura - 300), (200, 60))
        

        for _ in range(13):  # quantidade de retângulos
            largura_ret = random.randint(10, 150)
            altura_ret = random.randint(10, 100)
            x = random.randint(0, largura - largura_ret)
            y = random.randint(0, altura - altura_ret)
            cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pygame.draw.rect(janela, cor, (x, y, largura_ret, altura_ret), 5)    
        pygame.display.update()
        pygame.time.wait(100)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_dificuldade.collidepoint(event.pos):
                    click_sound.play()
                    selecionar_dificuldade()
                    no_menu = False
                    return
    
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    click_sound.play()
                    selecionar_dificuldade()
                    no_menu = False
                    return    
              
def mostrar_pause():
    global pontos
    global historico_pontos
    pause = True
    
    while pause:
        pygame.mixer.music.pause()
        janela.fill((0, 0, 0))
        
        fonte = pygame.font.Font('fonte/Symtext.ttf', 50)
        texto_pause = fonte.render("Jogo Pausado", True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        janela.blit(texto_pause, (largura // 2 - texto_pause.get_width() // 2, altura // 3 - texto_pause.get_height() // 2))
        
        # Desenhar botões
        botao_continuar = desenhar_botao("Continuar", 
                                 (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
                                 (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),  
                                 (largura // 2, altura // 2), (400, 60))

        botao_sair = desenhar_botao("Sair", 
                                    (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
                                    (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
                                    (largura // 2, altura // 2 + 80), (400, 60))

        botao_som = desenhar_botao("Som", 
                                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
                                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
                                (largura // 2, altura // 2 + 160), (400, 60))
        botao_menu = desenhar_botao("Voltar ao Menu", 
                                    (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
                                    (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
                                    (largura // 2, altura // 2 + 240), (400, 60))                        

        pygame.display.update()
        pygame.time.wait(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                click_sound.play()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_continuar.collidepoint(event.pos):
                    click_sound.play()
                    pygame.mixer.music.unpause()
                    return
                if botao_sair.collidepoint(event.pos):
                    click_sound.play()
                    pygame.quit()
                    sys.exit()
                if botao_som.collidepoint(event.pos):
                    click_sound.play()
                    regularSom(True)  # Função para ajustar o som
                    
                if botao_menu.collidepoint(event.pos):
                    click_sound.play()
                    pygame.mixer.music.stop()
                    mostrar_menu()  # Retorna ao menu principal
                    return    

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    click_sound.play()
                    pygame.mixer.music.unpause()
                    return
                if event.key == pygame.K_l:
                    click_sound.play()
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_4:
                    click_sound.play()
                    regularSom(True)
                if event.key == pygame.K_m:  # Tecla para voltar ao menu
                    click_sound.play()
                    pygame.mixer.music.stop()
                    mostrar_menu()  # Retorna ao menu principal
                    return    
                       
def pontuacao(ponto):
    global pontos  
    while True:
        janela.fill((0, 0, 0))
        diedmsg = "Você morreu!"
        fonte = pygame.font.Font('fonte/Symtext.ttf', 74)
        texto_pontuacao = fonte.render("Pontuação do jogador: " + str(ponto), True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        texto_died = fonte.render(diedmsg,True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        janela.blit(texto_pontuacao, (largura // 2 - texto_pontuacao.get_width() // 2, altura // 2 - texto_pontuacao.get_height() // 2))
        janela.blit(texto_died,(largura//2 - texto_died.get_width()//2,texto_died.get_height()+130))
        pygame.display.update()
        pygame.time.wait(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                click_sound.play()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    click_sound.play()
                    pontos = 0  # Reseta a pontuação
                    return
                 

def efeito_psicodelico(tempo=1000):
    inicio = pygame.time.get_ticks()
    fonte = pygame.font.Font('fonte/Symtext.ttf', 50)
    msg_for = fonte.render('VOCÊ VAI MORRER',True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    largura, altura = janela.get_size()
    max_raio = math.hypot(largura, altura) / 2
    while pygame.time.get_ticks() - inicio < tempo:
  
        janela.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        janela.blit(msg_for,(largura//2-220,altura//2 - 50))
        for i in range(10):
            raio = (pygame.time.get_ticks() % 500) + (i * 20)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            cor = (r, g, b)
            pygame.draw.circle(janela, cor, (largura // 2, altura // 2), int(raio % max_raio), 5)  

        for i in range(10):
            raio = (pygame.time.get_ticks() % 500) + (i * 20)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            cor = (r, g, b)
            pygame.draw.circle(janela, cor, (largura // 2, altura // 2), int(raio % max_raio), 5)
        pygame.display.update()
        pygame.time.delay(50) 

def efeito_ondas_psicodelicas(janela, tempo_duracao=500):
    fim_efeito = pygame.time.get_ticks() + tempo_duracao
    largura, altura = janela.get_size()
    max_raio = math.hypot(largura, altura) / 2

    while pygame.time.get_ticks() < fim_efeito:
        # Limpa a tela
        janela.fill((0, 0, 0))
        janela.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        for i in range(10):
            raio = (pygame.time.get_ticks() % 500) + (i * 20)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            cor = (r, g, b)
            pygame.draw.circle(janela, cor, (largura // 2, altura // 2), int(raio % max_raio), 5)  
    # Desenhar retângulos
        for i in range(3):  # quantidade de retângulos
            largura_ret = random.randint(50, 100)
            altura_ret = random.randint(50, 100)
            x = random.randint(0, largura - largura_ret)
            y = random.randint(0, altura - altura_ret)
            cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pygame.draw.rect(janela, cor, (x, y, largura_ret, altura_ret), 5)

        pygame.display.update()
        pygame.time.delay(50) 

def mostrandoFim():
    
    pygame.mixer.music.load(end_music)
    pygame.mixer.music.play(-1)
    fonte2 = pygame.font.Font('fonte/Symtext.ttf', 40)
    
    largura, altura = janela.get_size()
    max_raio = math.hypot(largura, altura) / 2

    while True:
        fimDeJogo_for = fonte2.render('Da loucura até a eternidade',True,(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        janela.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        janela.blit(fimDeJogo_for,(largura//2 -400,altura//2 - 50))
        for i in range(10):
            raio = (pygame.time.get_ticks() % 500) + (i * 20)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            cor = (r, g, b)
            pygame.draw.circle(janela, cor, (largura // 2, altura // 2), int(raio % max_raio), 5)
        for i in range(3):  # quantidade de retângulos
            largura_ret = random.randint(50, 100)
            altura_ret = random.randint(50, 100)
            x = random.randint(0, largura - largura_ret)
            y = random.randint(0, altura - altura_ret)
            cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pygame.draw.rect(janela, cor, (x, y, largura_ret, altura_ret), 5) 
        desenhar_circulos_hipnoticos(janela, largura, altura)    
             
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                   pygame.mixer.music.stop()
                   easterEgg1()
                   
        pygame.display.update()
        pygame.time.delay(40)




def easterEgg1():
    visualEffect.play()
    
    
    # Coordenadas iniciais do título "Insane Dreams"
    pos_x, pos_y = 0, 0
    
    # Velocidade inicial de movimento
    vel_x, vel_y = 5, 5

    while True:
        fonte = pygame.font.Font('fonte/Symtext.ttf', 50)
        # Preenchendo a tela com uma cor aleatória
        janela.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        # Renderizando o texto "Insane Dreams" com cores aleatórias
        INSANE = "Insane Dreams"
        InsaneF = fonte.render(INSANE, True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        # Desenhando o texto na janela
        janela.blit(InsaneF, (pos_x, pos_y))

        # Atualizando a posição do título com base na velocidade
        pos_x += vel_x
        pos_y += vel_y

        # Checando colisão com as bordas da janela para reverter o movimento
        if pos_x <= 0 or pos_x + InsaneF.get_width() >= largura:
            vel_x = -vel_x
        if pos_y <= 0 or pos_y + InsaneF.get_height() >= altura:
            vel_y = -vel_y

        # Desenhando os círculos hipnóticos
        desenhar_circulos_hipnoticos(janela, largura, altura)
        

        # Eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    easterEgg2() 

        # Delay e atualização da tela
        pygame.time.delay(30)
        pygame.display.update()

def easterEgg2():
    
    # Inicializando Pygame e a fonte
    largura, altura = janela.get_size()
    max_raio = math.hypot(largura, altura) / 2
    fonte_base = pygame.font.Font('fonte/Symtext.ttf', 40)

    # Parâmetros do efeito pulsante
    escala = 1
    aumentando = True

    # Parâmetros de desintegração do texto
    fragmentos = []
    tempo_fragmentos = 0

    # Tempo de duração de cada fragmento (velocidade de "desintegração")
    tempo_fragmento_max = 5

    while True:
        # Preenchendo a tela com um fundo psicodélico
        janela.fill((0,0,0))

        # Ajustando a escala do texto
        if aumentando:
            escala += 0.05
            if escala >= 2:
                aumentando = False
        else:
            escala -= 0.05
            if escala <= 1:
                aumentando = True

        # Criando a fonte em tamanho variável
        fonte = pygame.font.Font('fonte/Symtext.ttf', int(40 * escala))
        INSANE = "Insane Dreams"
        InsaneF = fonte.render(INSANE, True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        # Coordenadas do centro da tela para centralizar o texto
        pos_x = (largura - InsaneF.get_width()) // 2
        pos_y = (altura - InsaneF.get_height()) // 2

        # Desenhando o texto principal
        janela.blit(InsaneF, (pos_x, pos_y))
        for i in range(10):
            raio = (pygame.time.get_ticks() % 500) + (i * 20)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            cor = (r, g, b)
            pygame.draw.circle(janela, cor, (largura // 2, altura // 2), int(raio % max_raio), 5)

        # Fragmentos de texto que "desintegram"
        tempo_fragmentos += 1
        if tempo_fragmentos >= tempo_fragmento_max:
            fragmentos = [(random.randint(0, largura), random.randint(0, altura)) for _ in range(10)]
            tempo_fragmentos = 0

        # Desenhando fragmentos do texto em posições aleatórias
        for frag_x, frag_y in fragmentos:
            janela.blit(fonte_base.render("Insane", True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))), (frag_x, frag_y))

        # Desenhando efeitos hipnóticos em segundo plano
        desenhar_circulos_hipnoticos(janela, largura, altura)

        # Eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    
                    easterEgg3()

        # Delay e atualização da tela
        pygame.time.delay(30)
        pygame.display.update()

def easterEgg3():
    # Inicializando Pygame e fontes
    fonte_titulo = pygame.font.Font('fonte/Symtext.ttf', 50)
    fonte_legenda = pygame.font.Font('fonte/Symtext.ttf', 30)

    # Texto do título e legenda
    INSANE = "Insane Dreams"
    LEGENDA = "Criado por Davizer0"


    # Coordenadas e dimensões dos retângulos
    largura_retangulo = largura // 6
    altura_retangulo = 10  # Começa pequeno
    crescimento = 3        # Velocidade de crescimento dos retângulos
    y_centro = altura // 2  # Ponto central da tela

    # Controle de transparência para o efeito fade-in
    alpha = 0
    max_alpha = 255
    alpha_incremento = 5

    # Superfície para aplicar efeitos de transparência no título
    superficie_titulo = pygame.Surface((largura, altura), pygame.SRCALPHA)

    while True:
        # Preenchendo a tela com um fundo escuro
        cores = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        janela.fill((0, 0, 0))
        # Atualizando a transparência do título até o máximo
        if alpha < max_alpha:
            alpha += alpha_incremento

        # Desenhando os retângulos coloridos que se expandem
        for i, cor in enumerate(cores):
            x_retangulo = i * largura_retangulo
            pygame.draw.rect(janela, cor, (x_retangulo, y_centro - altura_retangulo // 2, largura_retangulo, altura_retangulo))

    
        if altura_retangulo < altura // 2:
            altura_retangulo += crescimento
   
        InsaneF = fonte_titulo.render(INSANE, True, (0,0,0))
        LegendaF = fonte_legenda.render(LEGENDA, True, (0,0,0))
        pos_x_legenda = (largura - LegendaF.get_width()) // 2
        janela.blit(LegendaF, (pos_x_legenda, y_centro + 150))

        pos_x_titulo = (largura - InsaneF.get_width()) // 2
        superficie_titulo.blit(InsaneF, (pos_x_titulo, y_centro - 150))
        janela.blit(superficie_titulo, (0, 0))

        # Eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Delay e atualização da tela
        pygame.time.delay(50)
        pygame.display.update()


        


exibirAviso(janela,largura,altura)
pygame.mixer.music.load(game_music)
pygame.mixer.music.play(-1)
while rodando:
   
    global hero
    max_raio = math.hypot(largura, altura) / 2
    janela.fill((0, 0, 0))
    hero = pygame.draw.rect(janela, (255, 255, 255), (xHero, yHero, tamanhoxHero, tamanhoyHero))
    zombie = pygame.draw.rect(janela, (0, 255, 0), (xZombie, yZombie, 40, 100))
    zumbiNovo = pygame.draw.rect(janela,(255,100,0),(xZombieNovo,yZombieNovo,80,80))
    mover_atirador()
    atualizar_projeteis() 
   
    lista_retangulos = [[random.randint(0, largura - 50), random.randint(0, altura - 50), 
                        random.randint(5, 20), random.randint(5, 15), gerar_cor_aleatoria(), 
                        [random.uniform(-1, 1), random.uniform(-1, 1)]] for _ in range(5)] 
   
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                click_sound.play()
                pause = True
                mostrar_pause()
                                
    keys = pygame.key.get_pressed()
    #movimentação do herói
    if keys[pygame.K_a]:
            xHero -= velHero
    if xHero < 0:  # Limite esquerdo da tela
            xHero = 0
    if keys[pygame.K_d]:
        xHero += velHero
        if xHero + tamanhoxHero > largura:  # Limite direito da tela
            xHero = largura
    if keys[pygame.K_w]:
        yHero -= velHero
        if yHero < 0:  # Limite superior da tela
            yHero = 0
    if keys[pygame.K_s]:
        yHero += velHero
        if yHero + tamanhoyHero > altura:  # Limite inferior da tela
            yHero = altura - tamanhoyHero

    #projétil do jogador
    if keys[pygame.K_UP] and not projetil_ativo:  # Atira para cima
        projetil_som.play()
        projetil_ativo = True
        xProjetil = xHero
        yProjetil = yHero
        direcao_projetil = 'cima'  # Impede controle após disparo
    if keys[pygame.K_DOWN] and not projetil_ativo:  # Atira para baixo
        projetil_som.play()
        projetil_ativo = True
        xProjetil = xHero
        yProjetil = yHero
        direcao_projetil = 'baixo'
    if keys[pygame.K_LEFT] and not projetil_ativo:  # Atira para esquerda
        projetil_som.play()
        projetil_ativo = True
        xProjetil = xHero
        yProjetil = yHero
        direcao_projetil = 'esquerda'
    if keys[pygame.K_RIGHT] and not projetil_ativo:  # Atira para direita
        projetil_som.play()
        projetil_ativo = True
        xProjetil = xHero
        yProjetil = yHero
        direcao_projetil = 'direita'

# Atualizando a posição do projétil
    if projetil_ativo:
        if direcao_projetil == 'esquerda':
            xProjetil -= velocidade_projetil
            if xProjetil < 0:  # Se o projétil sair da tela
                projetil_ativo = False
        elif direcao_projetil == 'direita':
            xProjetil += velocidade_projetil
            if xProjetil > largura:  # Se o projétil sair da tela
                projetil_ativo = False
        elif direcao_projetil == 'cima':
            yProjetil -= velocidade_projetil
            if yProjetil < 0:  # Se o projétil sair da tela
                projetil_ativo = False
        elif direcao_projetil == 'baixo':
            yProjetil += velocidade_projetil
            if yProjetil > altura:  # Se o projétil sair da tela
                projetil_ativo = False

# Desenhando o projétil
    if projetil_ativo:
        projetil = pygame.draw.rect(janela, (255, 255, 0), (xProjetil, yProjetil, 20, 20))
        if projetil.colliderect(zombie):
            pontos += 1.5
            
            zombie_death.play()
            xZombie = randint(1000, 2000)
            yZombie = randint(7,1080)
                    
            if pontos in[10,50,90]: 
                efeito_psicodelico()
                efeito_ondas_psicodelicas(janela)

        #colisão de projétil
        if projetil.colliderect(zumbiNovo):
            pontos += 1
            zombie_death.play()
            xZombieNovo = randint(10, 2180) 
            yZombieNovo = 50
            # Adiciona um novo zumbi azul na lista
            zumbisAzuis.append((2180,1080))
            atiradores.append((randint(10, 100), randint(40, 60)))
            if pontos in[10,50,90]: 
                efeito_psicodelico()
                efeito_ondas_psicodelicas(janela)
            
    # movimentação do zumbi(verde) em relação ao player
    if xHero > xZombie:
        xZombie += velZombie - 2
    elif xHero < xZombie:
        xZombie -= velZombie - 2
    if yHero > yZombie:
        yZombie += velZombie - 1
    elif yHero < yZombie:
        yZombie -= velZombie - 1
#zumbiAzul movimentação
    if xHero > posicoesAleatoriasX:
        posicoesAleatoriasX += velZombie
    elif xHero < posicoesAleatoriasX:
        posicoesAleatoriasX -= velZombie

    if yHero > posicoesAleatoriasY:
        posicoesAleatoriasY += velZombie
    elif yHero < posicoesAleatoriasY:
        posicoesAleatoriasY -= velZombie
                  
    #ZombieNovo(laranja)
    if xHero > xZombieNovo:
        xZombieNovo += velZombie - 0.2
    elif xHero < xZombieNovo:
        xZombieNovo -= velZombie - 0.2

    if yHero > yZombieNovo:
        yZombieNovo += velZombie - 0.2

    elif yHero < yZombieNovo:
        yZombieNovo -= velZombie - 0.2
                  
    if hero.colliderect(zombie):
        xZombie = 0
        yZombie = 0
        dano.play()
        #reseta todas as posições
        pontuacao(pontos)
        resetar_jogo()

    if hero.colliderect(zumbiNovo):
        xZombieNovo = 0
        yZombieNovo = 0
        dano.play()
        pontuacao(pontos)
        resetar_jogo()
      
    for pos in zumbisAzuis:
        zumbiAzul = pygame.draw.rect(janela, (0, 0, 255), (posicoesAleatoriasX, posicoesAleatoriasY, 40, 100))
        atirador = pygame.draw.rect(janela,(255,0,0),(posAtiradorX,posAtiradorY,90,90))
        atirar_inimigo()
        verificar_colisao_hero(projeteis_atirador, xHero, yHero, tamanhoxHero, tamanhoyHero, pontos)
             
        if hero.colliderect(zumbiAzul):
            
            dano.play()

            pontuacao(pontos)
            resetar_jogo() 

        if hero.colliderect(atirador):
            dano.play()
            
            pontuacao(pontos) 
            resetar_jogo() 
        
        if projetil.colliderect(atirador):
            dano.play()
            posAtiradorX = randint(10, 1000)
            posAtiradorY = randint(10, 200)
            pontos += 1

        if projetil_ativo and projetil.colliderect(zumbiAzul):
            pontos += 0.5
            zombie_death.play()
            posicoesAleatoriasX = 4
            posicoesAleatoriasY = randint(10,200)
            if pontos in[10,50,90]: 
                efeito_psicodelico()
                efeito_ondas_psicodelicas(janela)
        
           
        if pontos >= 150:
            desenhar_retangulos_caoticos(janela, largura, altura, lista_retangulos) 

        if pontos >= 200:
            mostrandoFim()   
                  
    fonte = pygame.font.Font('fonte/Symtext.ttf', 35)
    texto_pontos = fonte.render("Pontos: " + str(pontos), True, (255,255,255))
    
    janela.blit(texto_pontos, (50, 50))

    fps.tick(60)
    pygame.display.update()
    
