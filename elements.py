# Imports
import pygame, random
from textwrap import wrap
from player import Player  
from structure import Barriers  
from structure import grid  
from enemy import Enemy  
from attack import Attack  
from enemy import bonusEnemy  
from bubble import BubbleEffect

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
        # Create bubble group
        self.bubbleGroup = pygame.sprite.GroupSingle()
        self.createBubble ()
        # Set initial game state variables
        self.lives = 3
        self.endNotReached = True
        self.points = 0
        self.highScore = 0
        self.level = 1
        self.enemySpeed = 1.0
        # Load high score and sounds
        self.loadHighScore()
        self.destroySound = pygame.mixer.Sound("Sounds/destroy.ogg")
        self.levelSound = pygame.mixer.Sound("Sounds/level.ogg")
        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)  # Loop background music
        # Define Ocean Facts
        self.ocean_facts = [
            "While oil spills garner significant media attention, they account for only 12% of oceanic oil pollution",
            "Road, river and drainage runoff contributes 2-3 times more oil contamination than spills",
            "Annual plastic waste in oceans: 12 million metric tons (equivalent to 100,000+ blue whales)",
            "Five major garbage patches exist globally; the Great Pacific Garbage Patch contains ~1.8 trillion pieces",
            "Indonesia and India are the largest contributors to ocean plastic pollution",
            "Projections indicate ocean plastic may outweigh fish biomass by 2050",
            "Approximately 14 million metric tons of debris rests on the seafloor",
            "Synthetic clothing releases 700,000+ microfibers per wash, with estimates of 4 billion microfibers per square kilometer in oceans",
            "Agricultural nutrient runoff creates oxygen-depleted \"dead zones\" causing mass marine life die-offs",
            "Ocean life dead zones increased from 146 in 2004 to 400+ in 2008",
            "The largest recorded ocean lifedead zone (2017) in the Gulf of Mexico approached the size of New Jersey",
            "Ocean acidification threatens shellfish populations and industry",
            "Maritime noise pollution damages invertebrates crucial to marine food chains",
            "70% of ocean debris sinks, making cleanup extremely challenging",
            "Microplastic degradation releases harmful chemicals and enters the food chain",
            "Oceans contain 97% of Earth's water and cover 71% of the planet",
            "Phytoplankton produces 50-80% of Earth's oxygen",
            "Oceans absorb 90% of human-generated heat and 30% of carbon dioxide emissions",
            "Marine ecosystems provide vital food resources and pharmaceutical compounds"
        ]

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

    def createBubble(self):
        # create bubble for bubble group
        bubble = BubbleEffect(self.screenWidth, self.screenHeight)
        self.bubbleGroup.add(bubble)

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
        # Check if all non-bonus enemies are defated to trigger level up
        if len(self.enemyGroup) == 0: 
            self.levelup()

    def levelup(self):
        # play sound, increase level and difficulty, reset state
        self.levelSound.play()
        self.level += 1
        self.enemySpeed *= 1.25 # Increase enemy speed by 15%
        self.createEnemies() # Recreate enemies for new level
        self.lives = 3 # Resets lives back to 3 each level
        self.barriers = self.createBarriers() # Recreats the barriers for new level 

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
        self.bubbleGroup.empty() # Clear all bubbles
        self.playerGroup.sprite.restart()  # Reset player
        self.enemyGroup.empty()  # Clear enemies
        self.enemyAttackGroup.empty()  # Clear enemy attacks
        self.createEnemies()  # Create new enemies
        self.bonusEnemyGroup.empty()  # Clear bonus enemies
        self.barriers = self.createBarriers()
        self.points = 0  # Reset points
        self.level = 1 # Reset level
        self.enemySpeed = 1.0 # reset enemy speed

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

    def get_next_fact(self):
        # return random ocean fact
        return random.choice(self.ocean_facts)
