import pygame
import sys
import random
import math

from random import randint
from pygame.locals import *

pygame.init()
#Versão definitiva em análises

info = pygame.display.Info()
largura = info.current_w - 20
altura = info.current_h

zombie_death = pygame.mixer.Sound('colisser.wav')
dano = pygame.mixer.Sound('dano.wav')
projetil_som = pygame.mixer.Sound('projetil.wav')
click_sound = pygame.mixer.Sound('click1.wav')
direcaoProjetilSom = pygame.mixer.Sound('direcaoProjetil.wav')
menu_music = 'InsaneMenu2.wav'
game_music = 'InsaneGameTheme.wav'
end_music = 'End.wav'
atirador_sound = pygame.mixer.Sound('atirador.wav')

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
direcionador = 1
fps = pygame.time.Clock()
janela = pygame.display.set_mode((largura, altura), FULLSCREEN) # type: ignore
nomeDaJanela = pygame.display.set_caption('Insane Dreams')
velZombie = 3
pontos = 0
historico_pontos = []
pause = False
tamanhoxHero = 20
tamanhoyHero = 40
xZombieNovo = randint(20,200)
yZombieNovo = randint(20,200)
posicoesAleatoriasX = randint(10,100)
posicoesAleatoriasY = randint(10,300)
zumbisAzuis = []
atiradores = []
posAtiradorX = randint(90,400)
posAtiradorY = randint(60,100)
velAtirador = 5
velProjetilAtirador = 12
retangulos = []
projeteis_atirador = []
projetil_atirador_ativo = False
xProjetilAtirador = 0
yProjetilAtirador = 0 

def resetar_jogo():
    global pontos, xHero, yHero, projetil_ativo, xProjetil, yProjetil, zumbisAzuis, atiradores, projeteis_atirador, projetil_atirador_ativo,velHero
    # Resetar a pontuação
    pontos = 0
    historico_pontos.clear()  # Limpa o histórico de pontos
    velHero = 8.0
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


def fade(janela, largura, altura, fade_in=True):
    fade_surface = pygame.Surface((largura, altura))
    fade_surface.fill((0, 0, 0))

    # Corrigindo a lógica de fade para que o fade_in comece transparente
    if fade_in:
        alpha_range = range(0, 256, 5)  # Fade In (do transparente ao preto)
    else:
        alpha_range = range(255, -1, -5)  # Fade Out (do preto ao transparente)

    for alpha in alpha_range:
        fade_surface.set_alpha(alpha)
        janela.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(50)

def exibirAviso(janela,largura,altura): 
    
    aviso = pygame.image.load('warning2.jpeg')
    aviso_f =  pygame.transform.scale(aviso,(largura,altura))
    janela.blit(aviso_f, (0, 0))
    pygame.display.update()
    pygame.time.delay(2000) 
    fade(janela, largura, altura, fade_in=True)
    
    aviso1 = pygame.image.load('warning.jpeg')
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
            posAtiradorX = randint(0,100)
            posAtiradorY = randint(0,100)
            xZombieNovo = randint(0,100)
            yZombieNovo = randint(0,100) 
            xZombie = randint(0,100)
            yZombie = randint(0,100)           
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
        deltaX = xHero - posAtiradorX
        deltaY = yHero - posAtiradorY
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
    if rodando == True:
        while True:
            janela.fill((0,0,0))
            fonte1 = pygame.font.Font('fonte/Symtext.ttf',20)
            textoTela = fonte1.render("Regule o volume da Música pressionando as teclas de 0 a 5",True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            janela.blit(textoTela,(largura//4,altura//2))
            pygame.display.update()
            pygame.time.wait(200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        pygame.mixer.music.set_volume(0.0)  # Silenciar
                        
                    if event.key == pygame.K_1:
                        pygame.mixer.music.set_volume(0.2)
                        click_sound.play()
                        
                    if event.key == pygame.K_2:
                        pygame.mixer.music.set_volume(0.4)
                        click_sound.play()
                        
                    if event.key == pygame.K_3:
                        pygame.mixer.music.set_volume(0.6)
                        click_sound.play()
                        
                    if event.key == pygame.K_4:
                        pygame.mixer.music.set_volume(0.8)
                        click_sound.play()
                        
                    if event.key == pygame.K_5:
                        pygame.mixer.music.set_volume(1.0)
                        click_sound.play()  # Volume máximo
                        
                    if event.key == pygame.K_ESCAPE:
                        click_sound.play()                    
                        return  
                   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                pygame.mixer.music.set_volume(0.0)  # Silenciar
            if event.key == pygame.K_1:
                pygame.mixer.music.set_volume(0.2)
                click_sound.play()
            if event.key == pygame.K_2:
                pygame.mixer.music.set_volume(0.4)
                click_sound.play()
            if event.key == pygame.K_3:
                pygame.mixer.music.set_volume(0.6)
                click_sound.play()
            if event.key == pygame.K_4:
                pygame.mixer.music.set_volume(0.8)
                click_sound.play()
            if event.key == pygame.K_5:
                pygame.mixer.music.set_volume(1.0)
                click_sound.play()  # Volume máximo
            if event.key == pygame.K_ESCAPE:
                click_sound.play()
                mostrar_menu()
                return
for _ in range(10):
    posicoesAleatoriasX =  random.randint(10,2180)
    posicoesAleatoriasY =  random.randint(0,670)
    retangulos.append([posicoesAleatoriasX,posicoesAleatoriasY])
def mostrar_menu():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)
    global velZombie
    global velHero
    global velAtirador,velProjetilAtirador,velocidade_projetil
    no_menu = True
    while no_menu:
        janela.fill((0, 0, 0))
        fonte = pygame.font.Font('fonte/Symtext.ttf', 40)
        fonte1 = pygame.font.Font('fonte/Symtext.ttf',100)
        name = pygame.font.Font('fonte/Symtext.ttf',20)
        marca = pygame.font.Font('fonte/Symtext.ttf',30)
        marca_nome = marca.render("®",True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        apresentar_nome = fonte1.render("INSANE DREAMS",True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        mostre_name = name.render("Criad0 p0r DaviZer0",True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        texto_menu = fonte.render("1 Fácil, 2 Médio, 3 Difícil", True, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        texto_cofigs = fonte.render("Config. 4",True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        janela.blit(apresentar_nome, (largura/2 - apresentar_nome.get_width()//2, altura/2 - apresentar_nome.get_height()))
        janela.blit(texto_cofigs,(largura-texto_cofigs.get_width(),altura-texto_cofigs.get_height()))
        janela.blit(texto_menu, (largura//2 - texto_menu.get_width()//2, altura -300 - texto_menu.get_height()//2))
        janela.blit(mostre_name, (largura//2 - mostre_name.get_width()//2, altura - 400))
        janela.blit(marca_nome, (largura - texto_menu.get_width() +150 , altura//2.5))

        for _ in range(13):  # quantidade de retângulos
            largura_ret = random.randint(10, 150)
            altura_ret = random.randint(10, 100)
            x = random.randint(0, largura - largura_ret)
            y = random.randint(0, altura - altura_ret)
            cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pygame.draw.rect(janela, cor, (x, y, largura_ret, altura_ret), 5)    
        pygame.display.update()
        pygame.time.wait(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    click_sound.play()
                    velZombie = 2  # Velocidade dos zumbis para a dificuldade Fácil
                    velAtirador = 2
                    pygame.mixer.music.stop()  # Para a música do menu ao começar o jogo
                    pygame.mixer.music.load(game_music)  # Carrega a música da gameplay
                    pygame.mixer.music.play(-1)  # Reproduz a música da gameplay
                    resetar_jogo()
                    no_menu = False
                    return
                if event.key == pygame.K_2:
                    click_sound.play()
                    velZombie = 4.6  # Velocidade dos zumbis para a dificuldade Médio
                    pygame.mixer.music.stop()  # Para a música do menu ao começar o jogo
                    pygame.mixer.music.load(game_music)  # Carrega a música da gameplay
                    pygame.mixer.music.play(-1)  # Reproduz a música da gameplay
                    resetar_jogo()
                    no_menu = False
                    return
                if event.key == pygame.K_3:
                    click_sound.play()
                    velZombie = 6.5  # Velocidade dos zumbis para a dificuldade Difícil
                    velAtirador = 7
                    velProjetilAtirador = 10
                    velocidade_projetil = 60
                    velHero = 15
                    pygame.mixer.music.stop()  # Para a música do menu ao começar o jogo
                    pygame.mixer.music.load(game_music)  # Carrega a música da gameplay
                    pygame.mixer.music.play(-1)  # Reproduz a música da gameplay
                    no_menu = False
                    return
                if event.key == pygame.K_ESCAPE:
                    click_sound.play()
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_4:
                    click_sound.play()
                    regularSom(rodando)

                       

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
                                    (largura // 2, altura // 2 + 320), (400, 60))                        

        botao_reset = desenhar_botao("Resetar", 
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
                    
                if botao_reset.collidepoint(event.pos):
                    click_sound.play()
                    pygame.mixer.music.stop()
                    resetar_jogo()  # Chama a função que reseta o jogo
                    return
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
                if event.key == pygame.K_x:
                    click_sound.play()
                    pygame.mixer.music.stop()
                    resetar_jogo()
                    return
                if event.key == pygame.K_m:  # Tecla para voltar ao menu
                    click_sound.play()
                    pygame.mixer.music.stop()
                    mostrar_menu()  # Retorna ao menu principal
                    return    
                    
    

def pontuacao(ponto):
    global pontos  
    while True:
        janela.fill((0, 0, 0))
        fonte = pygame.font.Font('fonte/Symtext.ttf', 74)
        texto_pontuacao = fonte.render("Pontuação do jogador: " + str(ponto), True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        janela.blit(texto_pontuacao, (largura // 2 - texto_pontuacao.get_width() // 2, altura // 2 - texto_pontuacao.get_height() // 2))
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
                if event.key == pygame.K_h:
                    click_sound.play()
                    mostrarHistorico(historico_pontos)
                
                      

def mostrarHistorico(historico):
    global historico_pontos

    janela.fill((0, 0, 0))
    fonte = pygame.font.Font('fonte/Symtext.ttf', 74)
    y = 50
    for ponto in historico:
        textoHs = fonte.render(f"Histórico de pontuação: {ponto}", True, (255, 0, 255))
        janela.blit(textoHs, (largura // 2 - textoHs.get_width() // 2, y))
        y += 80
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_l:
                    pygame.quit()
                    sys.exit()   
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
    fimDeJogo_for = fonte2.render('Para a loucura até a eternidade',True,(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    largura, altura = janela.get_size()
    max_raio = math.hypot(largura, altura) / 2

    while True:
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
             
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    pygame.quit()
                    sys.exit()  
        pygame.display.update()
        pygame.time.delay(40)
      

exibirAviso(janela,largura,altura)
pygame.mixer.music.load(game_music)
pygame.mixer.music.play(-1)

while rodando:
    
    global hero
    janela.fill((0, 0, 0))
    hero = pygame.draw.rect(janela, (255, 255, 255), (xHero, yHero, tamanhoxHero, tamanhoyHero))
    zombie = pygame.draw.rect(janela, (0, 255, 0), (xZombie, yZombie, 40, 100))
    zumbiNovo = pygame.draw.rect(janela,(255,100,0),(xZombieNovo,yZombieNovo,80,80))
    mover_atirador()
    atualizar_projeteis()  
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                direcionador = 1
                direcaoProjetilSom.play()
            if event.key == pygame.K_2:
                direcionador = 2
                direcaoProjetilSom.play()
            if event.key == pygame.K_3:
                direcionador = 3
                direcaoProjetilSom.play()
            if event.key == pygame.K_4:
                direcionador = 4
                direcaoProjetilSom.play()
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
    if keys[pygame.K_p] and not projetil_ativo:
        projetil_som.play()
        projetil_ativo = True
        xProjetil = xHero -2
        yProjetil = yHero - 2
        direcao_projetil = direcionador  # impedir o controle do projétil após disparo

    if projetil_ativo:
        #esquerda
        if direcao_projetil == 1:
            xProjetil -= velocidade_projetil
            if xProjetil < 0:  # Se o projétil sair da tela
                projetil_ativo = False
        #direita
        if direcao_projetil == 2:
            xProjetil += velocidade_projetil
            if xProjetil > largura:  # Se o projétil sair da tela
                projetil_ativo = False
        #cima        
        if direcao_projetil == 3:
            yProjetil -= velocidade_projetil
            if yProjetil < 0:  # Se o projétil sair da tela
                projetil_ativo = False
        #baixo        
        if direcao_projetil == 4:
            yProjetil += velocidade_projetil
            if yProjetil > altura:  # Se o projétil sair da tela
                projetil_ativo = False

    if projetil_ativo:
        projetil = pygame.draw.rect(janela, (255, 255, 0), (xProjetil, yProjetil, 20, 20))
        if projetil.colliderect(zombie):
            pontos += 1
            historico_pontos.append(pontos)
            zombie_death.play()
            xZombie = randint(10, 2180)
            yZombie = randint(10, 1080)
            
            # Se atingir a pontuação de 10, ativa o efeito psicodélico
            if pontos in[10,50,90]: 
                efeito_psicodelico()
                efeito_ondas_psicodelicas(janela)

        #colisão de projétil
        if projetil.colliderect(zumbiNovo):
            pontos += 1
            historico_pontos.append(pontos)
            zombie_death.play()
            xZombieNovo = randint(10, 1900) 
            yZombieNovo = randint(10, 200) 
            # Adiciona um novo zumbi azul na lista
            zumbisAzuis.append((randint(10, 2180), randint(10, 1080)))
            atiradores.append((randint(10, 100), randint(40, 100)))
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
        dano.play()
        #reseta todas as posições
        xZombie = randint(10, 600)
        yZombie = randint(10, 600)
        posicoesAleatoriasX = randint(10, 300)
        posicoesAleatoriasY = randint(100, 500)
        posAtiradorX = randint(10, 200)
        posAtiradorY = randint(10, 200)
        xZombieNovo = randint(10, 300)
        yZombieNovo = randint(10, 600)
        pontuacao(pontos)

    if hero.colliderect(zumbiNovo):
        dano.play()
        xZombie = randint(10, 600)
        yZombie = randint(10, 600)
        posicoesAleatoriasX = randint(10, 300)
        posicoesAleatoriasY = randint(100, 500)
        posAtiradorX = randint(10, 200)
        posAtiradorY = randint(10, 200)
        xZombieNovo = randint(10, 300)
        yZombieNovo = randint(10, 600)
        pontuacao(pontos)
      
    for pos in zumbisAzuis:
        zumbiAzul = pygame.draw.rect(janela, (0, 0, 255), (posicoesAleatoriasX, posicoesAleatoriasY, 40, 100))
        atirador = pygame.draw.rect(janela,(255,0,0),(posAtiradorX,posAtiradorY,90,90))
        atirar_inimigo()
        verificar_colisao_hero(projeteis_atirador, xHero, yHero, tamanhoxHero, tamanhoyHero, pontos)
        
         
        if hero.colliderect(zumbiAzul):
            dano.play()
            posicoesAleatoriasX = randint(10, 300)
            posicoesAleatoriasY = randint(100, 500)
            posAtiradorX = randint(10, 200)
            posAtiradorY = randint(10, 200)
            xZombieNovo = randint(10, 300)
            yZombieNovo = randint(10, 600)
            pontuacao(pontos) 
        if hero.colliderect(atirador):
            dano.play()
            posAtiradorX = randint(10, 200)
            posAtiradorY = randint(10, 200)
            pontuacao(pontos)  
        if projetil.colliderect(atirador):
            dano.play()
            posAtiradorX = randint(10, 1000)
            posAtiradorY = randint(10, 200)
            pontos += 1.5

        if projetil_ativo and projetil.colliderect(zumbiAzul):
            pontos += 1
            historico_pontos.append(pontos)
            zombie_death.play()
            posicoesAleatoriasX = randint(10,1080)
            posicoesAleatoriasY = randint(10,200)
            if pontos in[10,50,90]: 
                efeito_psicodelico()
                efeito_ondas_psicodelicas(janela)

        if pontos >= 130:
            mostrandoFim()   
                  
    fonte = pygame.font.Font('fonte/Symtext.ttf', 35)
    texto_pontos = fonte.render("Pontos: " + str(pontos), True, (255,255,255))
    
    janela.blit(texto_pontos, (50, 50))

    fps.tick(60)
    pygame.display.update()
    
