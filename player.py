import pygame
from attack import Attack  

class Player(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight, screenOffset):
        super().__init__()  # Initialize the parent class
        # Initialize screen dimensions and offset
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.screenOffset = screenOffset
        
        # Load player image and set its position
        self.image = pygame.image.load("Graphics/player.png")
        self.rect = self.image.get_rect()  
        self.rect.midbottom = ((self.screenWidth + self.screenOffset) / 2, self.screenHeight)
        
        # Set player movement speed and initialize attack-related variables
        self.speed = 6
        self.attackGroup = pygame.sprite.Group()  # Group for player's attacks
        self.attackReady = True  # Flag to check if attack can be made
        self.attackTime = 0  # Time of last attack
        self.attackDelay = 300  # Delay between attacks (milliseconds)
        self.attackSound = pygame.mixer.Sound("Sounds/attack.ogg")  # Load attack sound

    def getInput(self):
        # Capture player input for movement and attack
        input = pygame.key.get_pressed()
        
        # Move player right
        if input[pygame.K_RIGHT]:
            self.rect.x += self.speed
        # Move player left
        if input[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # Attack when spacebar is pressed and attack is ready
        if input[pygame.K_SPACE] and self.attackReady:
            self.attackReady = False  # Set attack to not ready
            attack = Attack((self.rect.center), 5, self.screenHeight)  # Create attack instance
            self.attackGroup.add(attack)  # Add attack to attack group
            self.attackTime = pygame.time.get_ticks()  # Record the attack time
            self.attackSound.play()  # Play attack sound

    def update(self):
        # Update player state
        self.getInput()  # Get current input
        self.moveLimits()  # Check and enforce movement limits
        self.attackGroup.update()  # Update all attacks
        self.attackLimits()  # Check attack readiness

    def moveLimits(self):
        # Prevent player from moving outside screen boundaries
        if self.rect.right > self.screenWidth:
            self.rect.right = self.screenWidth  # Lock to right edge
        if self.rect.left < self.screenOffset:
            self.rect.left = self.screenOffset  # Lock to left edge

    def attackLimits(self):
        # Check if enough time has passed since the last attack
        if not self.attackReady:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.attackTime >= self.attackDelay:
                self.attackReady = True  # Allow new attack

    def restart(self):
        # Reset player position and attack group for a new game
        self.rect = self.image.get_rect()  
        self.rect.midbottom = ((self.screenWidth + self.screenOffset) / 2, self.screenHeight)
        self.attackGroup.empty()  # Clear all existing attacks
