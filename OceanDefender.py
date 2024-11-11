import pygame, sys, random
from attack import Attack  # Import Attack class for handling player attacks
from elements import Elements  # Import Elements class for game elements

pygame.init()  # Initialize all imported Pygame modules

# Set display dimensions and offset
displayWidth = 750
displayHeight = 700
displayOffset = 50

# Define colors using RGB tuples
colorYellow = (255, 0, 0)

# Load fonts and create text surfaces for UI elements
font = pygame.font.Font("Font/monogram.ttf", 40)
levelSurface = font.render("LEVEL 01", False, colorYellow)
gameOverSurface = font.render("GAME OVER", False, colorYellow)
pointsSurface = font.render("SCORE", False, colorYellow)
highscoreSurface = font.render("HIGH SCORE", False, colorYellow)

# Load background image
background = pygame.image.load("Graphics/background.jpg")
background = pygame.transform.scale(background, (displayWidth + displayOffset, displayHeight + 2 * displayOffset))

# Set up the display window
screen = pygame.display.set_mode((displayWidth + displayOffset, displayHeight + 2 * displayOffset))
pygame.display.set_caption("Ocean Defender")  # Set the window title

# Create a clock object to manage frame rate
clock = pygame.time.Clock()

# Initialize the game elements
elements = Elements(displayWidth, displayHeight, displayOffset)

# Set up custom events for attack and bonus creation
attackEvent = pygame.USEREVENT
pygame.time.set_timer(attackEvent, 300)  # Trigger attack events every 300 milliseconds

bonusEvent = pygame.USEREVENT + 1
pygame.time.set_timer(bonusEvent, random.randint(4000, 8000))  # Random interval for bonus creation

while True:
    # Event checking loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Handle window close event
            pygame.quit()  # Uninitialize all Pygame modules
            sys.exit()  # Exit the program

        # Handle attack event if game is ongoing
        if event.type == attackEvent and elements.endNotReached:
            elements.enemyAttack()  # Call method to handle enemy attacks

        # Handle bonus event if game is ongoing
        if event.type == bonusEvent and elements.endNotReached:
            elements.createBonus()  # Call method to create bonus enemy
            # Reset bonus event timer with a new random interval
            pygame.time.set_timer(bonusEvent, random.randint(4000, 8000))

        # Check for player inputs
        inputs = pygame.key.get_pressed()
        if inputs[pygame.K_SPACE] and not elements.endNotReached:  # Restart game if space is pressed
            elements.restart()

    # Game logic updates if game is ongoing
    if elements.endNotReached:
        elements.playerGroup.update()  # Update player state
        elements.moveEnemies()  # Move enemies
        elements.enemyAttackGroup.update()  # Update enemy attack group
        elements.bonusEnemyGroup.update()  # Update bonus enemies
        elements.collisionsCheck()  # Check for collisions

    # Draw Background
    screen.blit(background, (0, 0))

    # UI Drawing
    pygame.draw.rect(screen, colorYellow, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)  # Draw border
    pygame.draw.line(screen, colorYellow, (25, 730), (775, 730), 3)  # Draw score line

    # Display level or game over text based on game state
    if elements.endNotReached:
        screen.blit(levelSurface, (570, 740, 50, 50))
    else:
        screen.blit(gameOverSurface, (570, 740, 50, 50))

    # Display player lives
    positionX = 50
    for live in range(elements.lives):
        screen.blit(elements.playerGroup.sprite.image, (positionX, 745))  # Draw each life
        positionX += 50

    # Display score
    screen.blit(pointsSurface, (50, 15, 50, 50))
    formattedPoints = str(elements.points).zfill(5)  # Format points to 5 digits
    pointsValueSurface = font.render(formattedPoints, False, colorYellow)  # Render score text
    screen.blit(pointsValueSurface, (50, 40, 50, 50))

    # Display high score
    screen.blit(highscoreSurface, (550, 15, 50, 50))
    formattedHighscore = str(elements.highScore).zfill(5)  # Format high score to 5 digits
    highscoreValueSurface = font.render(formattedHighscore, False, colorYellow)  # Render high score text
    screen.blit(highscoreValueSurface, (625, 40, 50, 50))

    # Draw game elements on the screen
    elements.playerGroup.draw(screen)  # Draw player
    elements.playerGroup.sprite.attackGroup.draw(screen)  # Draw player attacks
    for barrier in elements.barriers:
        barrier.structureGroup.draw(screen)  # Draw barriers
    elements.enemyGroup.draw(screen)  # Draw enemies
    elements.enemyAttackGroup.draw(screen)  # Draw enemy attacks
    elements.bonusEnemyGroup.draw(screen)  # Draw bonus enemies

    # Update the display
    pygame.display.update()
    clock.tick(60)  # Cap the frame rate at 60 FPS
