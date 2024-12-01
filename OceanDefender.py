# Imports
import pygame, sys, random
from textwrap import wrap
from attack import Attack
from elements import Elements

# Start Pygame
pygame.init()
# Display settings
displayWidth = 750
displayHeight = 700
displayOffset = 50
colorMain = (255, 255, 255)
# Game states
GAME_STATE_START = 'start'
GAME_STATE_PLAYING = 'playing'
GAME_STATE_GAME_OVER = 'game_over'
current_game_state = GAME_STATE_START
# Load fonts
font = pygame.font.Font("Font/monogram.ttf", 40)
title_font = pygame.font.Font("Font/monogram.ttf", 80)
game_over_font = pygame.font.Font("Font/monogram.ttf", 100)
# UI text surfaces
titleSurface = title_font.render("OCEAN DEFENDER", False, colorMain)
startInstructionSurface = font.render("Press SPACE to Start", False, colorMain)
controlsLeftSurface = font.render("LEFT ARROW - Move Left", False, colorMain)
controlsRightSurface = font.render("RIGHT ARROW - Move Right", False, colorMain)
controlsShootSurface = font.render("SPACE - Shoot", False, colorMain)
quitSurface = font.render("ESC - Quit", False, colorMain)
gameOverSurface = game_over_font.render("GAME OVER", False, colorMain)
returnToMenuSurface = font.render("Press SPACE to return to menu", False, colorMain)
# Load and scale background image
background = pygame.image.load("Graphics/background.jpg")
background = pygame.transform.scale(background, (displayWidth + displayOffset, displayHeight + 2 * displayOffset))
# Setup display window
screen = pygame.display.set_mode((displayWidth + displayOffset, displayHeight + 2 * displayOffset))
pygame.display.set_caption("Ocean Defender")
clock = pygame.time.Clock()
# Initialize game elements
elements = Elements(displayWidth, displayHeight, displayOffset)
# Setup custom events for attacks, bonuses, and bubbles
attackEvent = pygame.USEREVENT
pygame.time.set_timer(attackEvent, 300)
bonusEvent = pygame.USEREVENT + 1
pygame.time.set_timer(bonusEvent, random.randint(4000, 8000))
bubbleEvent = pygame.USEREVENT + 2
pygame.time.set_timer(bubbleEvent, 1000)

def draw_start_screen():
    # Draw the start screen with game title and control instructions.
    screen.blit(background, (0, 0)) # Draw the background image at the top-left corner of the screen
    pygame.draw.rect(screen, colorMain, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60) # Draw a rounded rectangle as a border around the game area
    screen.blit(titleSurface, (displayWidth//2 - titleSurface.get_width()//2 + displayOffset//2, 200)) # Draw the game title at the top center
    screen.blit(startInstructionSurface, (displayWidth//2 - startInstructionSurface.get_width()//2 + displayOffset//2, 400)) # Draw the start instruction text below the title
    screen.blit(controlsLeftSurface, (displayWidth//2 - controlsLeftSurface.get_width()//2 + displayOffset//2, 500)) # Draw the "move left" control instruction
    screen.blit(controlsRightSurface, (displayWidth//2 - controlsRightSurface.get_width()//2 + displayOffset//2, 550)) # Draw the "move right" control instruction
    screen.blit(controlsShootSurface, (displayWidth//2 - controlsShootSurface.get_width()//2 + displayOffset//2, 600)) # Draw the "shoot" control instruction
    screen.blit(quitSurface, (displayWidth//2 - quitSurface.get_width()//2 + displayOffset//2, 700)) # Draw the "quit" instruction at the bottom center

def draw_game_over_screen():
    # Draw the game over screen with final score, high score, and ocean facts.
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, colorMain, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    # Display GAME OVER text
    screen.blit(gameOverSurface, (displayWidth//2 - gameOverSurface.get_width()//2, 200))
    # Display final score
    scoreSurface = font.render(f"SCORE: {str(elements.points).zfill(5)}", False, colorMain)
    screen.blit(scoreSurface, (displayWidth//2 - scoreSurface.get_width()//2, 350))    
    # Display high score
    highscoreSurface = font.render(f"HIGH SCORE: {str(elements.highScore).zfill(5)}", False, colorMain)
    screen.blit(highscoreSurface, (displayWidth//2 - highscoreSurface.get_width()//2, 400))    
    # Display "Did you know..." text and ocean fact
    didYouKnowSurface = font.render("Did you know...", False, colorMain)
    screen.blit(didYouKnowSurface, (displayWidth//2 - didYouKnowSurface.get_width()//2 + displayOffset//2, 500))
    # Display ocean fact
    wrapped_lines = wrap(fact, width=50)  # Wrap text to fit screen
    y_position = 550
    for line in wrapped_lines:
        fact_surface = font.render(line, False, colorMain)
        screen.blit(fact_surface, (displayWidth//2 - fact_surface.get_width()//2 + displayOffset//2, y_position))
        y_position += 35    
    # Display return to menu instruction
    screen.blit(returnToMenuSurface, (displayWidth//2 - returnToMenuSurface.get_width()//2, y_position + 35))

def Quit():
    # Quit the game and close the window.
    pygame.quit()
    sys.exit()
    
while True:
    # Game Loop

    for event in pygame.event.get():
        # Event Controller
        # Quit if quit event
        if event.type == pygame.QUIT:
            Quit()
        # Handle attack event
        if event.type == attackEvent and current_game_state == GAME_STATE_PLAYING and elements.endNotReached:
            elements.enemyAttack()
        # Handle bonus event
        if event.type == bonusEvent and current_game_state == GAME_STATE_PLAYING and elements.endNotReached:
            elements.createBonus()
            pygame.time.set_timer(bonusEvent, random.randint(4000, 8000))        
        # Handle bubble event
        if event.type == bubbleEvent:
            elements.createBubble()
            pygame.time.set_timer(bubbleEvent, random.randint(6000, 10000))
        # Take Inputs
        inputs = pygame.key.get_pressed()
        # Handle space key press for starting or resetting game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if current_game_state == GAME_STATE_START:
                current_game_state = GAME_STATE_PLAYING
                elements.restart()
            elif current_game_state == GAME_STATE_GAME_OVER:
                current_game_state = GAME_STATE_START
                elements.bubbleGroup.empty()
        # Handle escape key press for quitting the game from start state
        if inputs[pygame.K_ESCAPE] and current_game_state == GAME_STATE_START:
            Quit()
    
    if current_game_state == GAME_STATE_PLAYING: # Check if the game is in the playing state
        if elements.endNotReached: # Check if the game hasn't ended
            elements.playerGroup.update() # Update player's position and state
            elements.moveEnemies() # Move enemy characters
            elements.enemyAttackGroup.update() # Update enemy attack status
            elements.bonusEnemyGroup.update() # Update bonus enemy status
            elements.collisionsCheck() # Check for collisions between player, enemies, and attacks
            elements.bubbleGroup.update() # Update bubbles
        else:
            fact = elements.get_next_fact() # Get the next fact to display
            current_game_state = GAME_STATE_GAME_OVER # Change the game state to game over

    screen.blit(background, (0, 0)) # Draw the background image on the screen

    if current_game_state == GAME_STATE_START:
        # State Controller
        # Display start screen
        draw_start_screen()
        elements.bubbleGroup.update()
        elements.bubbleGroup.draw(screen)
    elif current_game_state == GAME_STATE_PLAYING:
        # Draw game UI and elements
        pygame.draw.rect(screen, colorMain, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
        pygame.draw.line(screen, colorMain, (25, 730), (775, 730), 3)
        # Display level
        levelText = f"LEVEL {str(elements.level).zfill(2)}"
        levelSurface = font.render(levelText, False, colorMain)
        screen.blit(levelSurface, (570, 740))
        # Display lives
        positionX = 50
        for live in range(elements.lives):
            screen.blit(elements.playerGroup.sprite.image, (positionX, 745))
            positionX += 50
        # Display scores
        screen.blit(font.render("SCORE", False, colorMain), (50, 15))
        screen.blit(font.render(str(elements.points).zfill(5), False, colorMain), (50, 40))
        screen.blit(font.render("HIGH SCORE", False, colorMain), (550, 15))
        screen.blit(font.render(str(elements.highScore).zfill(5), False, colorMain), (625, 40))
        # Draw game elements
        elements.playerGroup.draw(screen)
        elements.playerGroup.sprite.attackGroup.draw(screen)
        for barrier in elements.barriers:
            barrier.structureGroup.draw(screen)
        elements.enemyGroup.draw(screen)
        elements.enemyAttackGroup.draw(screen)
        elements.bonusEnemyGroup.draw(screen)
        elements.bubbleGroup.draw(screen)
    elif current_game_state == GAME_STATE_GAME_OVER:
        # Display game over screen
        draw_game_over_screen()
        elements.bubbleGroup.update()
        elements.bubbleGroup.draw(screen)
    
    # Update game
    pygame.display.update()
    clock.tick(60)
