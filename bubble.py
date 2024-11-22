# Imports
import pygame, random

class BubbleEffect(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight):
        super().__init__() # Initialize the parent class
        self.image = pygame.image.load("Graphics/bubble.png") # Load the bubble image
        self.screenWidth = screenWidth # Store screen width
        self.screenHeight = screenHeight # Store screen height
        
        # randomizes the size of the bubble
        bubblesize = random.randint(20,50)
        self.image = pygame.transform.scale(self.image,(bubblesize,bubblesize))
        
        x = random.randint(0, self.screenWidth) # Select random position along the bottom of the screen

        speed = random.randint(1,3)
        self.speed = speed # Sets the speed based on the size of the bubble

        self.rect = self.image.get_rect() # Get the rectangle that defines the bubbles position
        self.rect.topleft = (x, self.screenHeight+100) # Set the initial position

    def update(self):
        self.rect.y -= self.speed  # Move up
        if self.rect.bottom < 0:  # Remove sprite if it moves off screen
            self.kill()