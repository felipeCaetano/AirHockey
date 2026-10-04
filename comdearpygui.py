import pygame
import dearpygui.dearpygui as dpg

# --- CONFIGURAÇÃO DO DEAR PYGUI ---
dpg.create_context()
dpg.create_viewport(title="Painel de Controle", width=300, height=200)
dpg.setup_dearpygui()

# Variável de configuração compartilhada
config = {"bola_speed": 250}

# Função que o botão do Dear PyGui vai chamar
def mudar_velocidade(sender, app_data):
    config["bola_speed"] = dpg.get_value(sender)

with dpg.window(label="Configurações do Jogo"):
    dpg.add_slider_int(label="Velocidade da Bola", default_value=250, min_value=100, max_value=600, callback=mudar_velocidade)

dpg.show_viewport()

# --- CONFIGURAÇÃO DO PYGAME ---
pygame.init()
LARGURA, ALTURA = 400, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Janela do Pygame")
clock = pygame.time.Clock()
running = True

# --- LOOP INTEGRADO ---
while running and dpg.is_dearpygui_running():
    dt = clock.tick(60) / 1000.0
    
    # Eventos do Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lógica do Jogo usando os dados do Dear PyGui
    velocidade_atual = config["bola_speed"]
    
    # Desenho do Pygame
    TELA.fill((125, 62, 250))
    pygame.draw.circle(TELA, (255, 0, 0), (200, 300), 20) # Bola estática de teste
    pygame.display.flip()
    
    # --- O SEGREDO: Atualiza o Dear PyGui a cada frame do Pygame ---
    dpg.render_dearpygui_frame()

# Limpeza final
pygame.quit()
dpg.destroy_context()
