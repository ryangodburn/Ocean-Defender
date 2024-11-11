import pygame, random
from player import Player  
from structure import Barriers  
from structure import grid  
from enemy import Enemy  
from attack import Attack  
from enemy import bonusEnemy  

class Elements:
    def __init__(self, screenWidth, screenHeight, screenOffset):
        # Initialize screen dimensions and offsets
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.screenOffset = screenOffset
        
        # Create player group and add player instance
        self.playerGroup = pygame.sprite.GroupSingle()
        self.playerGroup.add(Player(self.screenWidth, self.screenHeight, self.screenOffset))
        
        # Create barriers and enemy groups
        self.barriers = self.createBarriers()
        self.enemyGroup = pygame.sprite.Group()
        self.createEnemies()
        
        # Initialize enemy movement direction and attack groups
        self.enemyDirection = 1
        self.enemyAttackGroup = pygame.sprite.Group()
        self.bonusEnemyGroup = pygame.sprite.GroupSingle()
        
        # Set initial game state variables
        self.lives = 3
        self.endNotReached = True
        self.points = 0
        self.highScore = 0
        
        # Load high score and sounds
        self.loadHighScore()
        self.destroySound = pygame.mixer.Sound("Sounds/destroy.ogg")
        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)  # Loop background music

    def createBarriers(self):
        # Calculate barrier width and gap based on screen dimensions
        barrierWidth = len(grid[0] * 3)
        barrierGap = (self.screenWidth + self.screenOffset - (4 * barrierWidth)) / 5
        barriers = []
        
        # Create and position barriers
        for i in range(4):
            offsetX = (i + 1) * barrierGap + i * barrierWidth
            barrier = Barriers(offsetX, self.screenHeight - 100)  # Position barriers at the bottom
            barriers.append(barrier)
        return barriers

    def createEnemies(self):
        # Create enemies in a grid formation
        for row in range(5):
            for column in range(11):
                positionX = 75 + column * 55
                positionY = 110 + row * 55
                
                # Assign enemy types based on row
                if row == 0:
                    enemyType = 3  
                elif row in (1, 2):
                    enemyType = 2  
                else:
                    enemyType = 1  
                
                # Create and add enemy to the enemy group
                enemy = Enemy(enemyType, positionX + self.screenOffset / 2, positionY)
                self.enemyGroup.add(enemy)

    def moveEnemies(self):
        # Update enemy positions and check for boundary collisions
        self.enemyGroup.update(self.enemyDirection)
        enemySprites = self.enemyGroup.sprites()
        
        for enemy in enemySprites:
            # Change direction if enemy hits the right boundary
            if enemy.rect.right >= self.screenWidth + self.screenOffset / 2:
                self.enemyDirection = -1
                self.moveEnemiesDown(2)  # Move enemies down
            # Change direction if enemy hits the left boundary
            elif enemy.rect.left <= self.screenOffset / 2:
                self.enemyDirection = 1
                self.moveEnemiesDown(2)  # Move enemies down

    def moveEnemiesDown(self, distance):
        # Move all enemies down by a specified distance
        if self.enemyGroup:
            for enemy in self.enemyGroup.sprites():
                enemy.rect.y += distance

    def enemyAttack(self):
        # Randomly select an enemy to attack
        if self.enemyGroup.sprites():
            randomEnemy = random.choice(self.enemyGroup.sprites())
            attackSprite = Attack(randomEnemy.rect.center, -6, self.screenHeight)  # Create attack
            self.enemyAttackGroup.add(attackSprite)  # Add attack to the attack group

    def createBonus(self):
        # Create a bonus enemy and add it to the bonus group
        self.bonusEnemyGroup.add(bonusEnemy(self.screenWidth, self.screenOffset))

    def collisionsCheck(self):
        # Check for collisions between player attacks and enemies
        if self.playerGroup.sprite.attackGroup:
            for attackSprite in self.playerGroup.sprite.attackGroup:
                enemyHit = pygame.sprite.spritecollide(attackSprite, self.enemyGroup, True)
                if enemyHit:
                    self.destroySound.play()  # Play destroy sound
                    for enemy in enemyHit:
                        self.points += enemy.type * 100  # Increment points based on enemy type
                        self.checkHighScore()  # Check for new high score
                        attackSprite.kill()  # Remove attack sprite
                
                # Check collision with bonus enemy
                if pygame.sprite.spritecollide(attackSprite, self.bonusEnemyGroup, True):
                    self.destroySound.play()
                    self.points += 500  # Add bonus points
                    self.checkHighScore()
                    attackSprite.kill()
                
                # Check collision with barriers
                for barrierSprite in self.barriers:
                    if pygame.sprite.spritecollide(attackSprite, barrierSprite.structureGroup, True):
                        attackSprite.kill()

        # Check for collisions between enemy attacks and player
        if self.enemyAttackGroup:
            for attackSprite in self.enemyAttackGroup:
                if pygame.sprite.spritecollide(attackSprite, self.playerGroup, False):
                    attackSprite.kill()  # Remove enemy attack on hit
                    self.lives -= 1  # Decrease player lives
                    self.destroySound.play()
                    if self.lives == 0:
                        self.endGame()  # End game if no lives left

                # Check collision with barriers
                for barrierSprite in self.barriers:
                    if pygame.sprite.spritecollide(attackSprite, barrierSprite.structureGroup, True):
                        attackSprite.kill()

        # Check for enemy collisions with barriers and player
        if self.enemyGroup:
            for enemy in self.enemyGroup:
                for barrierSprite in self.barriers:
                    pygame.sprite.spritecollide(enemy, barrierSprite.structureGroup, True)  # Remove enemy if hits barrier

                if pygame.sprite.spritecollide(enemy, self.playerGroup, False):
                    self.endGame()  # End game if enemy collides with player

    def endGame(self):
        # Set end game state
        self.endNotReached = False

    def restart(self):
        # Reset game state for a new game
        self.endNotReached = True
        self.lives = 3
        self.playerGroup.sprite.restart()  # Reset player
        self.enemyGroup.empty()  # Clear enemies
        self.enemyAttackGroup.empty()  # Clear enemy attacks
        self.createEnemies()  # Create new enemies
        self.bonusEnemyGroup.empty()  # Clear bonus enemies
        self.barriers = self.createBarriers()
        self.points = 0  # Reset points

    def checkHighScore(self):
        # Check and update high score
        if self.points > self.highScore:
            self.highScore = self.points
        with open("highscore.txt", "w") as file:
            file.write(str(self.highScore))  # Save new high score

    def loadHighScore(self):
        # Load high score from file, if it exists
        try:
            with open("highscore.txt", "r") as file:
                self.highScore = int(file.read())
        except FileNotFoundError:
            self.highScore = 0  # Default high score if file not found
