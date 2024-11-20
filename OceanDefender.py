import pygame, sys, random
from attack import Attack  # Import Attack class for handling player attacks
from elements import Elements  # Import Elements class for game elements
from enum import Enum

pygame.init()  # Initialize all imported Pygame modules

# Set display dimensions and offset
displayWidth = 750
displayHeight = 700
displayOffset = 50

# Define colors using RGB tuples
colorMain = (255, 255, 255)

# Define game states
GAME_STATE_START = 'start'
GAME_STATE_PLAYING = 'playing'
GAME_STATE_GAME_OVER = 'game_over'
current_game_state = GAME_STATE_START

# Load fonts and create text surfaces for UI elements
font = pygame.font.Font("Font/monogram.ttf", 40)
title_font = pygame.font.Font("Font/monogram.ttf", 80)

titleSurface = title_font.render("OCEAN DEFENDER", False, colorMain)
startInstructionSurface = font.render("Press SPACE to Start", False, colorMain)
controlsLeftSurface = font.render("LEFT ARROW - Move Left", False, colorMain)
controlsRightSurface = font.render("RIGHT ARROW - Move Right", False, colorMain)
controlsShootSurface = font.render("SPACE - Shoot", False, colorMain)
quitSurface = font.render("ESC - Quit",False, colorMain)
levelSurface = font.render("LEVEL 01", False, colorMain)
gameOverSurface = font.render("GAME OVER", False, colorMain)
pointsSurface = font.render("SCORE", False, colorMain)
highscoreSurface = font.render("HIGH SCORE", False, colorMain)

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

def draw_start_screen():
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, colorMain, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)

    # Draw title and instructions
    screen.blit(titleSurface, (displayWidth//2 - titleSurface.get_width()//2, 200))
    screen.blit(startInstructionSurface, (displayWidth//2 - startInstructionSurface.get_width()//2, 400))

    # Draw controls
    screen.blit(controlsLeftSurface, (displayWidth//2 - controlsLeftSurface.get_width()//2, 500))
    screen.blit(controlsRightSurface, (displayWidth//2 - controlsRightSurface.get_width()//2, 550))
    screen.blit(controlsShootSurface, (displayWidth//2 - controlsShootSurface.get_width()//2, 600))
    screen.blit(quitSurface,(displayWidth//2 - quitSurface.get_width()//2, 700))

def Quit():
    pygame.quit()  # Uninitialize all Pygame modules
    sys.exit()  # Exit the program

while True:
    # Event checking loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Handle window close event
            Quit()

        # Handle attack event if game is ongoing
        if event.type == attackEvent and current_game_state == GAME_STATE_PLAYING and elements.endNotReached:
            elements.enemyAttack()  # Call method to handle enemy attacks

        # Handle bonus event if game is ongoing
        if event.type == bonusEvent and current_game_state == GAME_STATE_PLAYING and elements.endNotReached:
            elements.createBonus()  # Call method to create bonus enemy
            # Reset bonus event timer with a new random interval
            pygame.time.set_timer(bonusEvent, random.randint(4000, 8000))

        # Check for player inputs
        inputs = pygame.key.get_pressed()
        if inputs[pygame.K_SPACE] and current_game_state == GAME_STATE_START:  # Start game if space is pressed
            current_game_state = GAME_STATE_PLAYING
            elements.restart()
        if inputs[pygame.K_SPACE] and current_game_state == GAME_STATE_GAME_OVER:
            current_game_state = GAME_STATE_START

        if inputs[pygame.K_ESCAPE] and current_game_state == GAME_STATE_START: # Quits game is ESC is pressed on start menu
            Quit()

    # Game logic updates if game is ongoing
    if elements.endNotReached and current_game_state == GAME_STATE_PLAYING:
        elements.playerGroup.update()  # Update player state
        elements.moveEnemies()  # Move enemies
        elements.enemyAttackGroup.update()  # Update enemy attack group
        elements.bonusEnemyGroup.update()  # Update bonus enemies
        elements.collisionsCheck()  # Check for collisions
 
    # Draw Background
    screen.blit(background, (0, 0))

    if current_game_state == GAME_STATE_START:
        draw_start_screen()
    
    if current_game_state == GAME_STATE_PLAYING:
        # UI Drawing
        pygame.draw.rect(screen, colorMain, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)  # Draw border
        pygame.draw.line(screen, colorMain, (25, 730), (775, 730), 3)  # Draw score line

        # Display level or game over text based on game state
        if elements.endNotReached:
            screen.blit(levelSurface, (570, 740, 50, 50))
        else:
            screen.blit(gameOverSurface, (570, 740, 50, 50))

        # Dynamically update and display the level text
        levelText = f"LEVEL {str(elements.level).zfill(2)}"
        levelSurface = font.render(levelText, False, colorMain)

        # Display player lives
        positionX = 50
        for live in range(elements.lives):
            screen.blit(elements.playerGroup.sprite.image, (positionX, 745))  # Draw each life
            positionX += 50

        # Display score
        screen.blit(pointsSurface, (50, 15, 50, 50))
        formattedPoints = str(elements.points).zfill(5)  # Format points to 5 digits
        pointsValueSurface = font.render(formattedPoints, False, colorMain)  # Render score text
        screen.blit(pointsValueSurface, (50, 40, 50, 50))

        # Display high score
        screen.blit(highscoreSurface, (550, 15, 50, 50))
        formattedHighscore = str(elements.highScore).zfill(5)  # Format high score to 5 digits
        highscoreValueSurface = font.render(formattedHighscore, False, colorMain)  # Render high score text
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
