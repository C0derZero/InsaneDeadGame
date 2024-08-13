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

#largura = 1900
#altura = 1080
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
janela = pygame.display.set_mode((largura, altura), FULLSCREEN)
velZombie = 4
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
atirando = False
tempo_projetil = 0  # Variável para controlar o tempo entre os disparos
intervalo_disparo = 500  # Intervalo de tempo entre disparos em milissegundos
verificador = 0
#pygame.mixer.music.play(-1)
def mostrar_menu():
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)
    global velZombie
    global velHero
    while True:
        janela.fill((0, 0, 0))
        fonte = pygame.font.Font(None, 40)
        fonte1 = pygame.font.Font(None,100)
        name = pygame.font.Font(None,20)
        marca = pygame.font.Font(None,25)
        marca_nome = marca.render("®",True,(255,0,0))
        apresentar_nome = fonte1.render("INSANE DEAD",True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        mostre_name = name.render("Made by DaviZero",True,(0,0,255))
        texto_menu = fonte.render("Pressione 1 para Fácil, 2 para Médio, 3 para Difícil", True, (255, 255, 255))
        janela.blit(apresentar_nome, (largura/2 - apresentar_nome.get_width()//2, altura/2 - apresentar_nome.get_height()))
        janela.blit(texto_menu, (largura//2 - texto_menu.get_width()//2, altura -300 - texto_menu.get_height()//2))
        janela.blit(mostre_name, (largura -660 - texto_menu.get_width()//2, altura - 400- texto_menu.get_height()))
        janela.blit(marca_nome, (largura -360 - texto_menu.get_width()//2, altura/2- texto_menu.get_height()))
        for i in range(3):  # quantidade de retângulos
            largura_ret = random.randint(50, 100)
            altura_ret = random.randint(50, 100)
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
                    return
                if event.key == pygame.K_2:
                    velZombie = 4.6  # Velocidade dos zumbis para a dificuldade Médio
                    return
                if event.key == pygame.K_3:
                    velZombie = 6.5  # Velocidade dos zumbis para a dificuldade Difícil
                    velHero = 15
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def mostrar_pause():
    global pontos
    global historico_pontos
    while pause:
        janela.fill((0, 0, 0))
        fonte = pygame.font.Font(None, 74)
        texto_pause = fonte.render("Jogo Pausado. Pressione ESC para continuar.", True, (255, 255, 255))
        janela.blit(texto_pause, (largura//2 - texto_pause.get_width()//2, altura//2 - texto_pause.get_height()//2))
        pygame.display.update()

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

def pontuacao(ponto):
    global pontos  
    while True:
        janela.fill((0, 0, 0))
        fonte = pygame.font.Font(None, 74)
        texto_pontuacao = fonte.render("Pontuação do jogador: " + str(ponto), True, (255, 255, 255))
        janela.blit(texto_pontuacao, (largura // 2 - texto_pontuacao.get_width() // 2, altura // 2 - texto_pontuacao.get_height() // 2))
        pygame.display.update()
        
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
    global verificador
    verificador +=1
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
                    pygame.quit()
                    sys.exit()   
        pygame.display.update()
        pygame.time.delay(40)


            
mostrar_menu()
pygame.mixer.music.load(game_music)
pygame.mixer.music.play(-1)
while rodando:
    
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
    
    if keys[pygame.K_p] and not projetil_ativo:
        projetil_som.play()
        projetil_ativo = True
        xProjetil = xHero + 1
        yProjetil = yHero + 1
        direcao_projetil = direcionador  # impedir o controle do projétil após disparo

    if projetil_ativo:
        if direcao_projetil == 1:
            xProjetil -= velocidade_projetil
            if xProjetil < 0:  # Se o projétil sair da tela
                projetil_ativo = False
        if direcao_projetil == 2:
            xProjetil += velocidade_projetil
            if xProjetil > largura:  # Se o projétil sair da tela
                projetil_ativo = False
        if direcao_projetil == 3:
            yProjetil -= velocidade_projetil
            if yProjetil < 0:  # Se o projétil sair da tela
                projetil_ativo = False
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
            

    # movimentação do zumbi em relação ao player
    if xHero > xZombie:
        xZombie += velZombie - 1
    elif xHero < xZombie:
        xZombie -= velZombie - 1
    if yHero > yZombie:
        yZombie += velZombie - 1
    elif yHero < yZombie:
        yZombie -= velZombie - 1
    
    if xHero > posicoesAleatoriasX:
        posicoesAleatoriasX += velZombie
    elif xHero < posicoesAleatoriasX:
        posicoesAleatoriasX -= velZombie
    if yHero > posicoesAleatoriasY:
        posicoesAleatoriasY += velZombie
    elif yHero < posicoesAleatoriasY:
        posicoesAleatoriasY -= velZombie

    if xHero > posAtiradorX:
        posAtiradorX += velZombie - 0.4
    elif xHero < posAtiradorX:
        posAtiradorX -= velZombie - 0.4
    if yHero > posAtiradorY:
        posAtiradorY += velZombie - 0.1
    elif yHero < posAtiradorY:
        posAtiradorY -= velZombie  - 0.1                 
      
    if xHero > xZombieNovo:
        xZombieNovo += velZombie
    elif xHero < xZombieNovo:
        xZombieNovo -= velZombie
    if yHero > yZombieNovo:
        yZombieNovo += velZombie
    elif yHero < yZombieNovo:
        yZombieNovo -= velZombie    

    if hero.colliderect(zombie):
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
        #disparar_projeteis()
            
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
    
    fonte = pygame.font.Font(None, 35)
    texto_pontos = fonte.render("Pontos: " + str(pontos), True, (255, 255, 255))
    janela.blit(texto_pontos, (50, 50))

    fps.tick(60)
    pygame.display.update()
