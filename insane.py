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
menu_music = 'ZombiesMenu.wav'
game_music = 'MusicB_1.wav'
end_music = 'End.wav'
atirador_sound = pygame.mixer.Sound('atirador.wav')

rodando = True
xHero = largura / 2
yHero = altura / 2
velHero = 7.3
projetil_ativo = False
xProjetil = xHero
yProjetil = yHero
velocidade_projetil = 30
xZombie = randint(10, 600)
yZombie = randint(10, 600)
direcionador = 1
fps = pygame.time.Clock()
janela = pygame.display.set_mode((largura, altura), FULLSCREEN) # type: ignore
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
velAtirador = 3
velProjetilAtirador = 10
retangulos = []
projeteis_atirador = []
projetil_atirador_ativo = False
xProjetilAtirador = 0
yProjetilAtirador = 0 
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
    alinhado_em_x = abs(xHero - posAtiradorX) <= 60
    alinhado_em_y = abs(yHero - posAtiradorY) <= 60
    
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
        projetilAtirador = pygame.draw.rect(janela, (255, 255, 0), (proj[0], proj[1], 10, 10))

        
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
            fonte1 = pygame.font.Font(None,50)
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
                    if event.key == pygame.K_2:
                        pygame.mixer.music.set_volume(0.4)
                    if event.key == pygame.K_3:
                        pygame.mixer.music.set_volume(0.6)
                    if event.key == pygame.K_4:
                        pygame.mixer.music.set_volume(0.8)
                    if event.key == pygame.K_5:
                        pygame.mixer.music.set_volume(1.0)  # Volume máximo
                    if event.key == pygame.K_ESCAPE:                    
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
            if event.key == pygame.K_2:
                pygame.mixer.music.set_volume(0.4)
            if event.key == pygame.K_3:
                pygame.mixer.music.set_volume(0.6)
            if event.key == pygame.K_4:
                pygame.mixer.music.set_volume(0.8)
            if event.key == pygame.K_5:
                pygame.mixer.music.set_volume(1.0)  # Volume máximo
            if event.key == pygame.K_ESCAPE:
                return
for _ in range(10):
    posicoesAleatoriasX =  random.randint(10,2180)
    posicoesAleatoriasY =  random.randint(0,670)
    retangulos.append([posicoesAleatoriasX,posicoesAleatoriasY])
def mostrar_menu():
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)
    global velZombie
    global velHero
    global velAtirador,velProjetilAtirador
    while True:
        janela.fill((0, 0, 0))
        fonte = pygame.font.Font(None, 40)
        fonte1 = pygame.font.Font(None,100)
        name = pygame.font.Font(None,20)
        marca = pygame.font.Font(None,25)
        marca_nome = marca.render("®",True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        apresentar_nome = fonte1.render("INSANE DREAM",True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        mostre_name = name.render("Made by DaviZero",True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        texto_menu = fonte.render("1 Fácil, 2 Médio, 3 Difícil", True, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        texto_cofigs = fonte.render("Config. 4",True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        janela.blit(apresentar_nome, (largura/2 - apresentar_nome.get_width()//2, altura/2 - apresentar_nome.get_height()))
        janela.blit(texto_cofigs,(largura-texto_cofigs.get_width(),altura-texto_cofigs.get_height()))
        janela.blit(texto_menu, (largura//2 - texto_menu.get_width()//2, altura -300 - texto_menu.get_height()//2))
        janela.blit(mostre_name, (largura//2 - mostre_name.get_width()//2, altura - 400))
        janela.blit(marca_nome, (largura/2 + texto_menu.get_width() , altura/2))

        for i in range(10):  # quantidade de retângulos
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
                    velZombie = 2  # Velocidade dos zumbis para a dificuldade Fácil
                    velAtirador = 1.2
                    return
                if event.key == pygame.K_2:
                    velZombie = 4.6  # Velocidade dos zumbis para a dificuldade Médio
                    return
                if event.key == pygame.K_3:
                    velZombie = 6.5  # Velocidade dos zumbis para a dificuldade Difícil
                    velAtirador = 5
                    velProjetilAtirador = 8
                    velHero = 15
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_4:
                    regularSom(rodando)
                    return    

def mostrar_pause():
    global pontos
    global historico_pontos
    while pause:
        pygame.mixer.music.pause()
        janela.fill((0, 0, 0))
        fonte = pygame.font.Font(None, 74)
        texto_pause = fonte.render("Jogo Pausado. Pressione ESC para continuar.", True, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        janela.blit(texto_pause, (largura//2 - texto_pause.get_width()//2, altura//2 - texto_pause.get_height()//2))
        pygame.display.update()
        pygame.time.wait(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.unpause()
                    return
                if event.key == pygame.K_l:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_x:
                    regularSom(rodando)    


def pontuacao(ponto):
    global pontos  
    while True:
        janela.fill((0, 0, 0))
        fonte = pygame.font.Font(None, 74)
        texto_pontuacao = fonte.render("Pontuação do jogador: " + str(ponto), True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        janela.blit(texto_pontuacao, (largura // 2 - texto_pontuacao.get_width() // 2, altura // 2 - texto_pontuacao.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pontos = 0  # Reseta a pontuação
                    return
                if event.key == pygame.K_h:
                    mostrarHistorico(historico_pontos)
                
                      

def mostrarHistorico(historico):
    global historico_pontos

    janela.fill((0, 0, 0))
    fonte = pygame.font.Font(None, 74)
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
    fonteMsg = pygame.font.SysFont('Haettenschweiler', 80 , False , False)
    msg = f'VOCÊ VAI MORRER'
    msg_for = fonteMsg.render(msg,False,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
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
    fonte2 = pygame.font.SysFont('Haettenschweiler', 80 , False , False)
    fimDeJogo = f'Para a loucura até a eternidade'
    fimDeJogo_for = fonte2.render(fimDeJogo,True,(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
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
                    psicodelia()  
        pygame.display.update()
        pygame.time.delay(40)

def psicodelia():
    global psy   
    global xHero
    global yHero
    global tamanhoxHero
    global tamanhoyHero
    global pause
    global posicoesAleatoriasY
    global posicoesAleatoriasX
    velZombie = 2
    velHero = 5
    while True:
        janela.fill((0,0,0))
        hero = pygame.draw.rect(janela, (255, 255, 255), (xHero, yHero, tamanhoxHero, tamanhoyHero))
        for pos in retangulos:
            if pos[0] < xHero:
                pos[0] += velZombie  # Move o retângulo para a direita
            if pos[0] > xHero:
                pos[0] -= velZombie  # Move o retângulo para a esquerda
            if pos[1] < yHero:
                pos[1] += velZombie # Move o retângulo para baixo
            if pos[1] >yHero:
                pos[1] -= velZombie # Move o retângulo para cima
        
            x = pygame.draw.rect(janela,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(pos[0],pos[1] ,20,60))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    mostrar_pause()
                if event.key == pygame.K_l:
                    pygame.quit()
                    sys.exit()   
        
        if xHero > posicoesAleatoriasX:
            posicoesAleatoriasX += velZombie
        elif xHero < posicoesAleatoriasX:
            posicoesAleatoriasX -= velZombie
        if yHero > posicoesAleatoriasY:
            posicoesAleatoriasY += velZombie
        elif yHero < posicoesAleatoriasY:
            posicoesAleatoriasY -= velZombie
        if hero.colliderect(x):
            loucura(janela)


        fps.tick(60)
        pygame.display.update()        

def loucura(janela,tempo_duracao =5):
    global xHero
    global yHero
    global pause
    fim_efeito = pygame.time.get_ticks() + tempo_duracao
    largura, altura = janela.get_size()
    max_raio = math.hypot(largura, altura) / 2
    while  pygame.time.get_ticks() < fim_efeito:
        janela.fill((random.randint(140,255),random.randint(0,255),random.randint(0,255)))
        fonte = pygame.font.SysFont('Haettenschweiler', 80 , False , False)
        msg = f'Acho que não estamos mais aqui'
        msg_for = fonte.render(msg,True,(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        janela.blit(msg_for,(largura//2 -400,altura//2 - 50))
        hero = pygame.draw.rect(janela, (255, 255, 255), (xHero, yHero, tamanhoxHero, tamanhoyHero))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    mostrar_pause()
        keys = pygame.key.get_pressed()
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

        for i in range(3):  # quantidade de retângulos
            largura_ret = random.randint(50, 100)
            altura_ret = random.randint(50, 100)
            x = random.randint(0, largura - largura_ret)
            y = random.randint(0, altura - altura_ret)
            cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pygame.draw.rect(janela, cor, (x, y, largura_ret, altura_ret), 5) 
        for i in range(10):
            raio = (pygame.time.get_ticks() % 500) + (i * 20)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            cor = (r, g, b)
            pygame.draw.circle(janela, cor, (largura // 2, altura // 2), int(raio % max_raio), 5)
                  
       
        fps.tick(60)
        pygame.display.update()        


mostrar_menu()
pygame.mixer.music.load(game_music)
pygame.mixer.music.play(-1)
while rodando:
    
    global hero
    janela.fill((0, 0, 0))
    hero = pygame.draw.rect(janela, (255, 255, 255), (xHero, yHero, tamanhoxHero, tamanhoyHero))
    zombie = pygame.draw.rect(janela, (0, 255, 0), (xZombie, yZombie, 40, 60))
    zumbiNovo = pygame.draw.rect(janela,(255,100,0),(xZombieNovo,yZombieNovo,40,70))
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                direcionador = 1
            if event.key == pygame.K_2:
                direcionador = 2
            if event.key == pygame.K_3:
                direcionador = 3
            if event.key == pygame.K_4:
                direcionador = 4
            if event.key == pygame.K_ESCAPE:
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
        projetil = pygame.draw.rect(janela, (255, 255, 0), (xProjetil, yProjetil, 30, 8))
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
            pontos += 1.5
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
        zumbiAzul = pygame.draw.rect(janela, (0, 0, 255), (posicoesAleatoriasX, posicoesAleatoriasY, 40, 80))
        atirador = pygame.draw.rect(janela,(255,0,0),(posAtiradorX,posAtiradorY,tamanhoxHero,tamanhoyHero)) 
   
                
            
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
            pontos += 0.5

        if projetil_ativo and projetil.colliderect(zumbiAzul):
            pontos += 2
            historico_pontos.append(pontos)
            zombie_death.play()
            posicoesAleatoriasX = randint(10,1080)
            posicoesAleatoriasY = randint(10,200)
            if pontos in[10,50,90]: 
                efeito_psicodelico()
                efeito_ondas_psicodelicas(janela)
        if pontos >= 200:
            mostrandoFim() 
    mover_atirador()
    atirar_inimigo()
    atualizar_projeteis()
    verificar_colisao_hero(projeteis_atirador, xHero, yHero, tamanhoxHero, tamanhoyHero, pontos)            
                         
    
    fonte = pygame.font.Font(None, 35)
    texto_pontos = fonte.render("Pontos: " + str(pontos), True, (255,255,255))
    
    janela.blit(texto_pontos, (50, 50))

    fps.tick(60)
    pygame.display.update()
    