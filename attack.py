import pygame

class Attack(pygame.sprite.Sprite):
    def __init__(self, position, speed, screenHeight):
        super().__init__()  # Initialize the parent class
        # Create a rectangular surface for the attack
        self.image = pygame.Surface((4, 15))  # Width: 4 pixels, Height: 15 pixels
        self.image.fill((255, 0, 0))  # Fill the surface with a yellow color
        self.rect = self.image.get_rect()  # Get the rectangle that defines the surface's position
        self.rect.center = position  # Set the center of the attack to the specified position
        self.speed = speed  # Set the speed of the attack
        self.screenHeight = screenHeight  # Store the screen height for boundary checking

    def update(self):
        # Move the attack upwards based on its speed
        self.rect.y -= self.speed
        
        # Check if the attack is out of bounds (above the screen or below)
        if self.rect.y > self.screenHeight + 15 or self.rect.y < 0:
            self.kill()  # Remove the attack from all groups and free memory