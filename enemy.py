# Imports
import pygame, random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()  # Initialize the parent class
        self.type = type  # Store the type of the enemy
        # Load the corresponding enemy image based on its type
        filePath = f"Graphics/enemy_{type}.png"
        self.image = pygame.image.load(filePath)
        self.rect = self.image.get_rect()  # Get the rectangle that defines the enemy's position
        self.rect.topleft = (x, y)  # Set the enemy's position to the specified coordinates

    def update(self, direction):
        # Move the enemy horizontally based on the given direction
        self.rect.x += direction

class bonusEnemy(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenOffset):
        super().__init__()  # Initialize the parent class
        self.screenWidth = screenWidth  # Store screen width
        self.screenOffset = screenOffset  # Store screen offset
        # Load the bonus enemy image
        self.image = pygame.image.load("Graphics/bonus.png")
        
        # Randomly position the bonus enemy on the left or right side of the screen
        x = random.choice([self.screenOffset / 2, self.screenWidth + self.screenOffset - self.image.get_width()])
        
        # Set speed based on the position chosen
        if x == self.screenOffset / 2:
            self.speed = 3  # Move right
        else:
            self.speed = -3  # Move left
            
        self.rect = self.image.get_rect()  # Get the rectangle that defines the bonus enemy's position
        self.rect.topleft = (x, 90)  # Set the initial vertical position

    def update(self):
        # Move the bonus enemy horizontally based on its speed
        self.rect.x += self.speed
        
        # Remove the bonus enemy if it moves off-screen
        if self.rect.right > self.screenWidth + self.screenOffset:
            self.kill()  # Remove the bonus enemy from all groups and free memory
        elif self.rect.left < self.screenOffset / 2:
            self.kill()  # Remove if it moves past the left side of the screen
            