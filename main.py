pip install pygame

import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Doodle Jump')

# Set up game clock for FPS
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Doodler class
class Doodler(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity_y = 0
        self.is_jumping = False
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        
        # Apply gravity
        self.velocity_y += 1
        self.rect.y += self.velocity_y
        
        # Collision with the ground
        if self.rect.y >= SCREEN_HEIGHT - 50:
            self.rect.y = SCREEN_HEIGHT - 50
            self.velocity_y = 0
            self.is_jumping = False
        
        # Prevent going off-screen horizontally
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - 50:
            self.rect.x = SCREEN_WIDTH - 50
    
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -15
            self.is_jumping = True

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -20)
            self.rect.x = random.randint(0, SCREEN_WIDTH - 100)

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Create player (doodler)
player = Doodler()
all_sprites.add(player)

# Create platforms
for i in range(10):
    platform = Platform(random.randint(0, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100))
    all_sprites.add(platform)
    platforms.add(platform)

# Game loop
running = True
while running:
    # Set FPS
    clock.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # Update all sprites
    all_sprites.update()

    # Check for collisions with platforms
    if pygame.sprite.spritecollide(player, platforms, False):
        player.velocity_y = -10

    # Fill screen with white background
    screen.fill(WHITE)

    # Draw all sprites
    all_sprites.draw(screen)

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()