import pygame
import sys
import random
import os

# Constants
WIDTH, HEIGHT = 1280, 720
CIRCLE_RADIUS = 28
CIRCLE_SPEED = 13
ARROW_LENGTH = 100
ARROW_SPEED = 14
SPAWN_PROBABILITY = 0.185

# Initialize Pygame
pygame.init()

# Load images and set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Pygame Project")

background_image = pygame.image.load("game_background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

player_image = pygame.image.load("player0.png")
player_image = pygame.transform.scale(player_image, (2 * CIRCLE_RADIUS, 2 * CIRCLE_RADIUS))

arrow_image = pygame.image.load("arrow.png")
arrow_image = pygame.transform.scale(arrow_image, (ARROW_LENGTH, ARROW_LENGTH))

# Sound
sound = pygame.mixer.Sound('gayyyy_sound.mp3')
sound.set_volume(1)

# Classes
class Circle:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.hitbox = pygame.Rect(self.x - CIRCLE_RADIUS, self.y - CIRCLE_RADIUS, 2 * CIRCLE_RADIUS, 2 * CIRCLE_RADIUS)

    def move(self, keys):
        if keys[pygame.K_a] and self.x > CIRCLE_RADIUS:
            self.x -= CIRCLE_SPEED
        if keys[pygame.K_d] and self.x < WIDTH - CIRCLE_RADIUS:
            self.x += CIRCLE_SPEED
        if keys[pygame.K_w] and self.y > CIRCLE_RADIUS:
            self.y -= CIRCLE_SPEED
        if keys[pygame.K_s] and self.y < HEIGHT - CIRCLE_RADIUS:
            self.y += CIRCLE_SPEED
        self.hitbox.topleft = (self.x - CIRCLE_RADIUS, self.y - CIRCLE_RADIUS)

    def draw(self):
        screen.blit(player_image, (self.x - CIRCLE_RADIUS, self.y - CIRCLE_RADIUS))

class Arrow:
    def __init__(self):
        self.x = 0
        self.y = random.randint(0, HEIGHT)
        self.image = arrow_image
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (self.x, self.y - self.image_rect.height // 2)
        self.colliding = False

    def move(self):
        self.x += ARROW_SPEED
        self.image_rect.topleft = (self.x, self.y - self.image_rect.height // 2)

    def draw(self):
        screen.blit(self.image, self.image_rect)

    def check_collision(self, circle):
        if self.colliding:
            return False

        distance = ((self.x - circle.x) ** 2 + (self.y - circle.y) ** 2) ** 0.5
        if distance < (CIRCLE_RADIUS + ARROW_LENGTH / 2):
            self.colliding = True
            return True
        return False

# Initialize game variables
player_circle = Circle()
arrows = []
game_over = False
score = 0
high_score = 0
start_time = 0

if os.path.isfile("highscore.txt"):
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())

options_menu = False
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            options_menu = not options_menu

    if not options_menu:
        keys = pygame.key.get_pressed()

        if start_time == 0:
            start_time = pygame.time.get_ticks()
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        if random.random() < SPAWN_PROBABILITY:
            arrows.append(Arrow())

        for arrow in arrows[:]:
            arrow.move()
            if arrow.x > WIDTH:
                arrows.remove(arrow)

        for arrow in arrows:
            if arrow.check_collision(player_circle):
                game_over = True
                break

        score = elapsed_time

        if score > high_score:
            high_score = score

    screen.blit(background_image, (0, 0))

    for arrow in arrows:
        arrow.draw()

    player_circle.move(keys)
    player_circle.draw()

    font = pygame.font.Font(None, 36)
    text = font.render(f"Time: {elapsed_time} seconds", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    font = pygame.font.Font(None, 24)
    text = font.render(f"Score: {score}   High Score: {high_score}", True, (0, 0, 0))
    screen.blit(text, (10, 40))

    if options_menu:
        font = pygame.font.Font(None, 48)
        text = font.render("OPTIONS", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        font = pygame.font.Font(None, 36)
        text = font.render("Press ESC to resume", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(60)

    if game_over:
        font = pygame.font.Font(None, 72)
        text = font.render("YOU LOSE", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        sound.play()
        pygame.display.flip()

        with open("highscore.txt", "w") as file:
            file.write(str(high_score))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        options_menu = not options_menu
                    elif options_menu and event.key == pygame.K_r:
                        options_menu = False
                        game_over = False
                        arrows = []
                        start_time = pygame.time.get_ticks()
                        elapsed_time = 0
                        score = 0
                    elif options_menu and event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
