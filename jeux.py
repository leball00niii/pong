import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Raquettes
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
player1 = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Balle
BALL_SIZE = 15
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
ball_speed_x = 5
ball_speed_y = 5

# Vitesse des joueurs
paddle_speed = 7

# Score
score1 = 0
score2 = 0
font = pygame.font.SysFont(None, 50)

# Boucle principale
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)  # 60 FPS

    # Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Contrôles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= paddle_speed
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += paddle_speed
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= paddle_speed
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += paddle_speed

    # Déplacement de la balle
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Collisions
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1

    # Score
    if ball.left <= 0:
        score2 += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1

    if ball.right >= WIDTH:
        score1 += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1

    # Affichage
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    score_text = font.render(f"{score1}    {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - 50, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
