import pygame
import random
import math

#initialise pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800, 600))

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#Background
background = pygame.image.load("background.png")

#Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 50

def player(x,y):
    screen.blit(playerImg, (x,y)) #blit means to draw

#Enemy
enemyImg = []
enemyX = []
enemyY = []
num_of_enemies = 6
enemyX_change = [50]
enemyY_change = [0]

for i in range(num_of_enemies): 
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(64,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)


def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

#Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480  #i.e y position of spaceship
bulletX_change = 0
bulletY_change = 50
bullet_state = "ready" 
# Ready- bullet can't be seen on the screen
# Fire - bullet is currently moving on the screen

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

#Scored
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

def showscore(x,y):
    score = font.render("Score: " + str(score_value),True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    text = pygame.font.Font('freesansbold.ttf', 64)
    msg = text.render("GAME OVER!", True, (255,0,0))
    screen.blit(msg, (210,250))

#Game Loop
running = True
while running:
    #Fill in the RGB values of background
    screen.fill((0,0,0))
    #background
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #if keystroke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -50
            if event.key == pygame.K_RIGHT:
                playerX_change = 50
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    fire_bullet(playerX,bulletY)
                    bulletX = playerX
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        


    #Checking for boundaries
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    #Enemy movement
    for i in range(num_of_enemies):
        #Gameover
        if enemyY[i] >= 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]   
        if enemyX[i] < 0:
            enemyX[i] = 0
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX[i] = 736
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        
        #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value+=1
            enemyX[i] = random.randint(64,736)
            enemyY[i] = random.randint(50,150)

        
        enemy(enemyX[i],enemyY[i],i)
    
    showscore(textX,textY)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change 

    

    player(playerX, playerY)
    pygame.display.update()