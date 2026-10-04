import math

import pygame


pygame.init()

running = True

LARGURA = 400
ALTURA = 600
MAX_SCORE = 7

FONTE_PLACAR = pygame.font.SysFont("Arial", 40, bold=True)

rx_ia, ry_ia = 175, 20  # Fica na altura Y=20
speed_ia = 190
ia_score = 0

px, py = 200, 596
rx, ry = 175, 580
player_score = 0

speed = 250
speed_x = 0
speed_y = speed

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("AI hockey!")

clock = pygame.time.Clock()

def detect_collisions(raquete, bola):
    angulo = 0
    if raquete.colliderect(bola):
        raquete_centro_x = raquete.centerx
        metade_largura = raquete.width / 2
        pos = (bola.centerx - raquete_centro_x) / metade_largura
        pos = max(-1.0, min(1.0, pos))
        
        angulo = pos * (math.pi / 2.25)
        return True, angulo
    return False, angulo

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT] and rx>=1:
        rx -= 5
    if teclas[pygame.K_RIGHT]and rx + 50 <= LARGURA - 2:
        rx += 5

    center_ia = rx_ia + 25
    if px > center_ia + 4:
        rx_ia += speed_ia * dt
    elif px < center_ia - 4:
        rx_ia -= speed_ia * dt

    # Restrição para a raquete da IA não sair das paredes laterais
    if rx_ia < 1:
        rx_ia = 1
    if rx_ia + 50 > LARGURA - 2:
        rx_ia = LARGURA - 52

    TELA.fill((125, 62, 250))
    campo = pygame.draw.rect(
        TELA, (250,74,43), (0, 0, LARGURA, ALTURA), width=2
        )
    linha = pygame.draw.line(
        TELA, (250,74,43), (0,ALTURA/2), (LARGURA, ALTURA/2), width=2
        )
    trave1 = pygame.draw.rect(TELA, (0,174, 43), (150, 0, 100, 5), width=2)
    trave2 = pygame.draw.rect(
        TELA, (0,174, 43), (150, ALTURA - 5, 100, 5), width=2
        )

    texto_ia = FONTE_PLACAR.render(str(ia_score), True, (250, 74, 43))
    texto_player = FONTE_PLACAR.render(str(player_score), True, (250, 74, 43))
    
    # Desenha os textos na tela usando coordenadas (X, Y) perto da linha de centro
    TELA.blit(texto_ia, (LARGURA // 2 - 10, ALTURA // 2 - 60))      # Placar da IA acima do meio
    TELA.blit(texto_player, (LARGURA // 2 - 10, ALTURA // 2 + 20))
    
    px += speed_x * dt
    py += speed_y * dt
    
        # ========================================================
    # LOGICA DE GOL E RICOCHETE NO FUNDO (TETO / CHÃO)
    # ========================================================
    
    # --- 1. VERIFICAÇÃO NO TOPO (ZONA DA IA) ---
    if py <= 6:
        # Ponto de colisão horizontal da bola (eixo X)
        # Verifica se está DENTRO do intervalo da trave (X entre 150 e 250)
        if 150 <= px <= 250:
            print("GOL DO JOGADOR!")
            player_score += 1
            if player_score == MAX_SCORE:
                running = False
                break
            
            # Sistema de Reset: Bola volta ao centro indo em direção a quem sofreu o gol
            px, py = 200, 300
            speed_x = 0
            speed_y = -speed  # Vai para cima (em direção à IA)
        else:
            # Caso contrário: A bola atingiu a parede cinza/roxa fora da trave -> RICOCHETEIA
            py = 6
            speed_y = -speed_y

    # --- 2. VERIFICAÇÃO NA BASE (ZONA DO JOGADOR) ---
    if py >= 594:
        # Verifica se está DENTRO do intervalo da trave (X entre 150 e 250)
        if 150 <= px <= 250:
            print("GOL DA IA!")
            ia_score += 1
            if ia_score == MAX_SCORE:
                running = False
                break
            
            # Sistema de Reset: Bola volta ao centro indo em direção a quem sofreu o gol
            px, py = 200, 300
            speed_x = 0
            speed_y = speed   # Vai para baixo (em direção ao Jogador)
        else:
            # Caso contrário: A bola atingiu o fundo fora da trave -> RICOCHETEIA
            py = 594
            speed_y = -speed_y

    if px <= 6:
        px = 6
        speed_x = -speed_x
    if px >= 394:
        px = 394
        speed_x = -speed_x

    bola = pygame.draw.circle(TELA, (255,0,0), (int(px), py), 6)
    raquete = pygame.draw.rect(
        TELA, (0,0,0), (rx, ry, 50, 5), width=0, border_radius=2
        )
    ia = pygame.draw.rect(
        TELA, (176,254,32), (int(rx_ia), ry_ia, 50, 5), width=0, border_radius=2
        )

    colide_player, angulo_player = detect_collisions(raquete, bola)
    if colide_player:
        py = ry - 7
        speed_x = speed * math.sin(angulo_player)
        speed_y = -speed * math.cos(angulo_player)

    colide_ia, angulo_ia = detect_collisions(ia, bola)
    if colide_ia:
        py = ry_ia + 10 + 7
        speed_x = speed * math.sin(angulo_ia)
        speed_y = speed * math.cos(angulo_ia)
        
    pygame.display.flip()
    

pygame.quit()

