import pygame

class Structure(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Initialize the parent class
        # Create a small surface for the structure
        self.image = pygame.Surface((3, 3))  # Width: 3 pixels, Height: 3 pixels
        self.image.fill((255, 0, 0))  # Fill the surface with a yellow color
        self.rect = self.image.get_rect()  # Get the rectangle that defines the structure's position
        self.rect.topleft = (x, y)  # Set the structure's position

# Define a grid layout where 1s represent solid structures and 0s represent empty spaces
grid = [
    [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
    [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]
]

class Barriers(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Initialize the parent class
        self.structureGroup = pygame.sprite.Group()  # Group to hold all structure parts
        
        # Loop through the grid to create structures based on its layout
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column] == 1:  # Check if the grid cell is solid
                    positionX = x + column * 3  # Calculate the x position for the structure
                    positionY = y + row * 3      # Calculate the y position for the structure
                    structure = Structure(positionX, positionY)  # Create a new structure
                    self.structureGroup.add(structure)  # Add the structure to the group
