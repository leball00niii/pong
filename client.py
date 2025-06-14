import pygame
import socket
import pickle
import threading

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

paddle_y = 250
player_id = None
game_state = {}

# Connexion au serveur
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))
player_id = pickle.loads(client.recv(1024))

def receive():
    global game_state
    while True:
        try:
            game_state = pickle.loads(client.recv(4096))
        except:
            break

threading.Thread(target=receive, daemon=True).start()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle_y > 0:
        paddle_y -= 7
    if keys[pygame.K_DOWN] and paddle_y < HEIGHT - 100:
        paddle_y += 7

    # Envoie au serveur
    try:
        client.send(pickle.dumps(paddle_y))
    except:
        pass

    # Dessine le jeu
    if game_state:
        pygame.draw.rect(screen, WHITE, (50, game_state["paddles"].get(0, 0), 10, 100))
        pygame.draw.rect(screen, WHITE, (740, game_state["paddles"].get(1, 0), 10, 100))
        pygame.draw.ellipse(screen, WHITE, (*game_state["ball"], 15, 15))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
client.close()
