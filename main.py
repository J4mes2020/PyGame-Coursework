import random
import sys
import runpy
import time

import pygame

#Setting values for the game to use

playerTouch = False
AITouch = False
counter = 0
player_x = 0
player_y = 0
player_score = 0
ai_score = 0
mainMenuActive = True
optionsOpen = False


def playerHitbox(): # Defining the function for the player collisions
    global width
    global player
    global playerTouch
    global player_x

    if player.left <= 0:
        player.left = 0

    if player.right >= width:
        player.right = width

    # Checks if player is colliding with the obstacle if so it makes the player touch value true
    if player.colliderect(leftObstacle) or player.colliderect(rightObstacle):
        playerTouch = True


def aiHitbox(): #Function defined to detect if the AI hits something
    global width
    global aiPlayer
    global AITouch

    if aiPlayer.left <= 0:
        aiPlayer.left = 0

    if aiPlayer.right >= width:
        aiPlayer.right = width


        # Checks if AI is colliding with the obstacle if so it makes the AI touch value true
    if aiPlayer.colliderect(leftObstacle) or aiPlayer.colliderect(rightObstacle):
        AITouch = True


def aiMovement():

    if not AITouch:

        if aiPlayer.left <= leftObstacle.right:
            aiPlayer.left += 7

        if aiPlayer.right >= rightObstacle.left:
            aiPlayer.right -= 7


def runGame(): # The main function used to run the game which includes the player movement and events
    global player_x
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN: # Event for pressing the key down
            if event.key == pygame.K_RIGHT:
                player_x += 7

            if event.key == pygame.K_LEFT:
                player_x -= 7

        if event.type == pygame.KEYUP:  # Event for pressing the key up
            if event.key == pygame.K_RIGHT:
                player_x -= 7

            if event.key == pygame.K_LEFT:
                player_x += 7

    if not mainMenuActive:
        aiMovement() # The function which allows the ai to move
        playerHitbox() # Calls the function to see if the player has contacted with anything
        aiHitbox() # Calls the function to see if the AI has contacted with anything

        player.x += player_x
        player.y += player_y

        screen.blit(background, [0, 0]) # Update the screen

        reset()# Function used to reset the obstacles and increase the level difficulty

        # pygame.draw.shape(where, color, object)
        screen.blit(playerImage, player)
        screen.blit(aiImage, aiPlayer)
        renderTextUnderPlayer(player, aiPlayer)

        p_text = score_font.render("Player Score: " + str(player_score), False, Score)
        screen.blit(p_text, (15, 15))

        a_text = score_font.render("AI Score: " + str(ai_score), False, Score)
        screen.blit(a_text, (width - 130, 15))


        # Once reset this function will move the images to make sure the collisions line up
        moveObstacle(cloud1, cloud3, cloud4, cloud5, cloud6, cloud7, cloud8)
        deadCheck(player) # Checks if the player is dead


def mainMenu(): # This function is used to display the main menu and which loads the game
    global mainMenuActive
    global optionsOpen, ai_score, AITouch, playerTouch, player_score

    buttonOutline = pygame.image.load("assets/buttonOutline.png").convert()
    buttonOutlineHover = pygame.image.load("assets/buttonOutlineHover.png").convert()
    myName = buttonFont.render("© OdionWolf", True, darkBlurple)
    myName.set_alpha(30)

    miscFont = pygame.font.Font('assets/ansley-black.ttf', 10)
    schoolProject = miscFont.render("A project for the royal school", True, darkBlurple)
    schoolProject.set_alpha(150)

    startGameFont = buttonFont.render("Start Game", True, blurple)
    optionsFont = buttonFont.render("Options", True, blurple)
    closeGameFont = buttonFont.render("Close Game", True, blurple)

    mousePos = pygame.mouse.get_pos()

    screen.blit(mainMenuBackground, [0, 0])
    screen.blit(buttonOutline, startGame)
    screen.blit(buttonOutline, options)
    screen.blit(buttonOutline, closeGame)
    screen.blit(schoolProject, (0, height - schoolProject.get_height()))
    screen.blit(myName, (width - myName.get_width() - 10, height - myName.get_height() - 10))
    screen.blit(startGameFont, (startGame.width / 1.02, startGame.centery + startGameFont.get_height() - 29))
    screen.blit(optionsFont, (options.width / 0.95, options.centery + optionsFont.get_height() - 29))
    screen.blit(closeGameFont, (closeGame.width / 1.02, closeGame.centery + closeGameFont.get_height() - 29))

    if mainMenuActive:
        if startGame.collidepoint(mousePos):
            screen.blit(buttonOutlineHover, startGame)
            screen.blit(startGameFont, (startGame.width / 1.02, startGame.centery + startGameFont.get_height() - 29))

            if pygame.mouse.get_pressed()[0]:
                mainMenuActive = False
                pygame.mixer.music.pause()
                pygame.mixer.Sound.play(start_game_sound)
                pygame.mixer.Sound.set_volume(start_game_sound, 0.05)
                pygame.mixer.music.play(1)
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.load("music/active-game.wav")
                pygame.mixer.music.play(-1)

        if options.collidepoint(mousePos):

            screen.blit(buttonOutlineHover, options)
            screen.blit(optionsFont, (options.width / 0.95, options.centery + optionsFont.get_height() - 29))

            if pygame.mouse.get_pressed()[0]:
                optionsOpen = True

        if closeGame.collidepoint(mousePos):

            screen.blit(buttonOutlineHover, closeGame)
            screen.blit(closeGameFont, (closeGame.width / 1.02, closeGame.centery + closeGameFont.get_height() - 29))

            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()


def renderTextUnderPlayer(Player, AIPlayer):

    playerFonts = pygame.font.Font('assets/ansley-black.ttf', 12)
    playerText = playerFonts.render("Player", True, darkBlurple)
    aiText = playerFonts.render("AI", True, darkBlurple)
    aiText.set_alpha(50)

    screen.blit(playerText, ((Player.x + playerText.get_width() /4) - 16 , Player.centery + 40))
    screen.blit(aiText, ((AIPlayer.x + playerText.get_width() /2) - 8 , AIPlayer.centery + 40))






def deathMenu(): # If the player dies then this function will overlay a menu saying game over
    global mainMenuActive
    if not mainMenuActive:

        deathMenuScreen = pygame.display.set_mode((width, height))

        buttonOutline = pygame.image.load("assets/buttonOutline.png").convert()

        backtoMainMenuFont = buttonFont.render("Main Menu", True, blurple)
        gameOver = deadFont.render("GAME OVER", True, blurple)

        mousePos = pygame.mouse.get_pos()

        deathMenuScreen.blit(mainMenuBackground, [0, 0])

        deathMenuScreen.blit(buttonOutline, backToMainMenuButton)
        deathMenuScreen.blit(gameOver, (
            screen.get_width() / 2 - backtoMainMenuFont.get_width() / 2 - 270,
            backtoMainMenuFont.get_height() / 2 + 100))

        if backToMainMenuButton.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0]:
                runpy.run_path('main.py')
                sys.exit()

        deathMenuScreen.blit(backtoMainMenuFont, (
            backToMainMenuButton.width, backToMainMenuButton.centery + backtoMainMenuFont.get_height() - 30))

        pygame.display.update()


def optionsMenu(): # Creates the options menu
    global optionsOpen
    global startGame, options, closeGame

    returnBox = pygame.Rect(width / 2.55, height - 100, 200, 85)
    controlOutline = pygame.image.load("assets/controlButtons.png").convert()
    returnButton = pygame.image.load("assets/returnButton.png").convert()
    returnButtonHover = pygame.image.load("assets/returnButtonHover.png").convert()
    bFont = pygame.font.Font('assets/ansley-black.ttf', 100)
    cFont = pygame.font.Font('assets/ansley-black.ttf', 17)
    rFont = pygame.font.Font('assets/ansley-black.ttf', 32)
    headerFont = pygame.font.Font('assets/ansley-black.ttf', 40)
    leftControls = pygame.Rect(width / 2 - 100, height / 4, 80, 80)
    leftFont = bFont.render("<", True, blurple)
    controls = headerFont.render("Controls", True, blurple)
    returnFont = rFont.render("Return", True, blurple)
    credit = cFont.render("Made by James Lawrence", True, blurple)
    rightControls = pygame.Rect(width / 2 + 25, height / 4, 80, 80)
    rightFont = bFont.render(">", True, blurple)
    screen.blit(mainMenuBackground, [0, 0])
    screen.blit(returnButton, returnBox)
    screen.blit(controlOutline, leftControls)
    screen.blit(controlOutline, rightControls)

    mousePos = pygame.mouse.get_pos()
    if returnBox.collidepoint(mousePos):

        screen.blit(returnButtonHover, returnBox)
        screen.blit(returnFont, (screen.get_width() / 2.5, height - 70))

        if pygame.mouse.get_pressed()[0]:
            optionsOpen = False

    screen.blit(controls, (width / 2 - controls.get_width() / 2 + 10, leftControls.centery - 100))
    screen.blit(leftFont, (leftControls.centerx - 15, leftControls.centery - 40))
    screen.blit(rightFont, (rightControls.centerx - 15, rightControls.centery - 40))
    screen.blit(credit, (screen.get_width() / 3.2, height - 130))
    screen.blit(returnFont, (screen.get_width() / 2.5, height - 70))


def reset(): #Resets the obstacles and randomises their spawn
    global player_score, leftObstacle, rightObstacle, ai_score

    if leftObstacle.top >= height:

        if player_score < 3:

            minGap = player.width * 3
            maxGap = width - minGap
            randomLength = random.uniform(0, width - maxGap)
            gap = random.uniform(minGap, maxGap)

            leftObstacle = pygame.Rect(0, 0, randomLength, 100)
            rightObstacle = pygame.Rect(leftObstacle.right + gap, 0, width, 100)

            print(gap)

        leftObstacle.top = 0
        rightObstacle.top = 0

        if not playerTouch:
            player_score += 1

        if not AITouch:
            ai_score += 1

        #pygame.time.wait(300)


def deadCheck(player): # Checks if the player is dead and handles if they are
    global player_x
    global AITouch

    if AITouch == True and playerTouch == True:
        deathMenu()

    if playerTouch:
        player_x = 0
        if player.width >= 0:
            player.width -= 1
            player.height -= 1

            AITouch = True

    else:
        leftObstacle.move_ip(0, obstacleSpeed)
        rightObstacle.move_ip(0, obstacleSpeed)

    if AITouch:
        if aiPlayer.width >= 0:
            aiPlayer.width -= 1
            aiPlayer.height -= 1


def moveObstacle(cloud1, cloud3, cloud4, cloud5, cloud6, cloud7, cloud8): # Responsible for overlaying the images

    if leftObstacle.width <= 240:
        cloud1 = pygame.transform.scale(cloud1, (leftObstacle.width, 100))
        screen.blit(cloud1, leftObstacle)
    elif leftObstacle.width <= 360:
        cloud3 = pygame.transform.scale(cloud3, (leftObstacle.width, 100))
        screen.blit(cloud3, leftObstacle)
    elif leftObstacle.width <= 480:
        cloud4 = pygame.transform.scale(cloud4, (leftObstacle.width, 100))
        screen.blit(cloud4, leftObstacle)
    elif leftObstacle.width <= 600:
        cloud5 = pygame.transform.scale(cloud5, (leftObstacle.width, 100))
        screen.blit(cloud5, leftObstacle)
    elif leftObstacle.width <= 720:
        cloud6 = pygame.transform.scale(cloud6, (leftObstacle.width, 100))
        screen.blit(cloud6, leftObstacle)
    elif leftObstacle.width <= 840:
        cloud7 = pygame.transform.scale(cloud7, (leftObstacle.width, 100))
        screen.blit(cloud7, leftObstacle)
    elif leftObstacle.width <= 960:
        cloud8 = pygame.transform.scale(cloud8, (leftObstacle.width, 100))
        screen.blit(cloud8, leftObstacle)

    if rightObstacle.width <= 240:
        screen.blit(cloud1, rightObstacle)
    elif rightObstacle.width <= 360:
        screen.blit(cloud3, rightObstacle)
    elif rightObstacle.width <= 480:
        screen.blit(cloud4, rightObstacle)
    elif rightObstacle.width <= 600:
        screen.blit(cloud5, rightObstacle)
    elif rightObstacle.width <= 720:
        screen.blit(cloud6, rightObstacle)
    elif rightObstacle.width <= 840:
        screen.blit(cloud7, rightObstacle)
    elif rightObstacle.width <= 960:
        screen.blit(cloud8, rightObstacle)

    # pygame.display.update()


pygame.init()
obstacleSpeed = 3
clock = pygame.time.Clock()

# COLORS

white = (255, 255, 255)
green = (22, 191, 0)
red = (242, 62, 46)
blue = (110, 94, 255)
aiColor = (237, 158, 0, 100)
gray = (130, 130, 130)
Score = (48, 237, 5)
blurple = (114, 137, 218)
darkBlurple = (78, 93, 148)
burpleBlack = (35, 39, 42)

# window

width = 960
height = 540
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Avoid Clouds!')
background = pygame.image.load("assets/bg.png").convert()
mainMenuBackground = pygame.image.load("assets/mainmenubg.png").convert()

# Game Rectangles pygame.rect(x,y,width,height)
player = pygame.Rect(width / 2 - 35, height - 105, 70, 70)
maxGapSize = 400
minGapSize = player.width
aiPlayer = pygame.Rect(width / 2, height - 105, 70, 70)
randomLength = random.uniform(0, width - maxGapSize)
gapBetweenObjects = random.uniform(minGapSize, maxGapSize)
leftObstacle = pygame.Rect(0, 0, randomLength, 100)
rightObstacle = pygame.Rect(randomLength + gapBetweenObjects, 0, width, 100)
playerImage = pygame.image.load("assets/player.png").convert()
aiImage = pygame.image.load("assets/aiplayer.png").convert()
aiImage.set_alpha(50)
cloud1 = pygame.image.load("assets/clouds/cloud1.png").convert()
cloud3 = pygame.image.load("assets/clouds/cloud3.png").convert()
cloud4 = pygame.image.load("assets/clouds/cloud4.png").convert()
cloud5 = pygame.image.load("assets/clouds/cloud5.png").convert()
cloud6 = pygame.image.load("assets/clouds/cloud6.png").convert()
cloud7 = pygame.image.load("assets/clouds/cloud7.png").convert()
cloud8 = pygame.image.load("assets/clouds/cloud8.png").convert()
score_font = pygame.font.Font('freesansbold.ttf', 20)
startGame = pygame.Rect(width / 2 - 200, height / 2.4 - 100, 400, 85)
options = pygame.Rect(width / 2 - 200, height / 2.4, 400, 85)
closeGame = pygame.Rect(width / 2 - 200, height / 2.4 + 100, 400, 85)
backToMainMenuButton = pygame.Rect(width / 2 - 200, height / 2.4 + 170, 400, 85)
buttonOutline = pygame.image.load("assets/buttonOutline.png").convert()
buttonFont = pygame.font.Font('assets/ansley-black.ttf', 20)
deadFont = pygame.font.Font('assets/ansley-black.ttf', 80)

# Music
start_game_sound = pygame.mixer.Sound("music/start-game.wav")
pygame.mixer.music.load("music/active-game-background.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
# Continous loop


while True:

    runGame()

    if mainMenuActive:
        mainMenu()

    if optionsOpen:
        optionsMenu()

    pygame.display.flip()
    clock.tick(60)
