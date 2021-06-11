import random                               #to generate raandom numbers
import sys                                  #to control exit command
from typing import Mapping                                  
import pygame                               #library for making of a game
from pygame.locals import *                 #basic pygame imports




# setting up the globaL variables
FPS = 32                                    #frames per second
SCREENWIDTH = 500
SCREENHEIGHT = 700
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) 
GROUNDY= SCREENHEIGHT * 0.8    
GAME_IMAGES = {}
GAME_AUDIO = {}
PLAYER = "media//images//bird_fly.png"
BACKGROUND = "media//images//bg_img.png"
PIPE = "media//images//pipe.png"



#-----------------------------------------------------------WELCOME SCREEN----------------------------------------------------------------#



def welcome_screen():

    # defining position via coordinates 
    messagex = int((SCREENWIDTH - GAME_IMAGES['message'].get_height())/1.1)
    messagey = int(SCREENHEIGHT*0.20)
    basex = 0
    
    while True:
        for event in pygame.event.get():                # getting access to all events of pygame

            # if user presses close icon or escape, the game should be stopped
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            else:
                SCREEN.blit(GAME_IMAGES['background'], (0, 0))                      # takes coordinates & images                
                SCREEN.blit(GAME_IMAGES['message'], (messagex, messagey))   
                SCREEN.blit(GAME_IMAGES['base'], (basex, GROUNDY))   
                pygame.display.update()                                             # important command becuase without executing this....program will not shift to the next screen
                fpsclock.tick(FPS)                                                  # controlling or finally setting the fps rate in the program



#----------------------------------------------------------------MAIN GAME----------------------------------------------------------------#



def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/5)
    basex = 0
    game_overx = int((SCREENWIDTH - GAME_IMAGES['over'].get_height())/2.5)
    game_overy = int(SCREENHEIGHT/4.5)
    

    # creating two pipes
    Pipe1 = getRandomPipe()
    Pipe2 = getRandomPipe()


    # making of a list of upper pipes that will contain two upper pipes i.e. one from the list Pipe1 & second from the list Pipe2
    upperPipes = [
        {'x' : SCREENWIDTH + 200, 'y' : Pipe1[0]['y']},
        {'x' : SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y' : Pipe2[0]['y']},
    ]


    # making of a list of lower pipes that will contain two lower pipes i.e. one from the list Pipe1 & second from the list Pipe2
    lowerPipes = [
        {'x' : SCREENWIDTH + 200, 'y' : Pipe1[1]['y']},
        {'x' : SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y' : Pipe2[1]['y']}, 
    ]


    pipeVelo_X = -4                               # setting a velocity to move the pipe & (-) assigned because pipe will move in left direction along -x axis
    playerVelo_Y = -9                             # to fly the player down & (-) assigned because player will fly along -y axis
    playerMin_Y = -8                              # the minimum limit the player can fly down
    playerMax_Y = 10                              # the maximum limit the player can fly up
    playerAcc_Y = 1                               # givimg an acceleration while flying
    playerFlapAcc = -8                            # velocity while flapping
    PlayerFlapped = False                         # it will become true when bird will flap

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN or (event.key == K_SPACE and event.key == K_UP):
                if playery >0:
                    playerVelo_Y = playerFlapAcc
                    PlayerFlapped = True
                    GAME_AUDIO['wing'].play()
                

        
        crashTest = is_collide(playerx, playery, upperPipes, lowerPipes)                # it will return true if the player will crash
        if crashTest:
            return


        # checking for scores
        PlayerMidPos = playerx + GAME_IMAGES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_IMAGES['pipe'][0].get_width()/2
            if pipeMidPos <= PlayerMidPos < pipeMidPos + 4:
                score+=1
                print(f"Your score is {score}")
                GAME_AUDIO['point'].play()


        if playerVelo_Y < playerMax_Y and not PlayerFlapped:            # if player's y velocity is less than its max velocity and bird is not flapping
            playerVelo_Y+=playerAcc_Y                                   # adding acceleration to the y velocity

        
        if PlayerFlapped:
            PlayerFlapped = False                                       # it means if user is pressing up key continuously then the value of flap will be true but if user released the up key then the value will become false
        playerHeight = GAME_IMAGES['player'].get_height()
        playery = playery + min(playerVelo_Y, GROUNDY - playery - playerHeight )                # minimum can be zero or negative


        # moving pipes to the left direction
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelo_X                                # velocity is set to -4 (above code) so whenever it will increment, the value will become negative and it will move to the left
            lowerPipe['x'] += pipeVelo_X


        # adding a new pipe when the previous one is about to leave the screen
        if len(upperPipes) > 0 and 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])


        # removing the pipe after it lefts the screen
        if len(upperPipes) > 0 and upperPipes[0]['x'] < -GAME_IMAGES['pipe'][0].get_width():         # if the upperpipes value becomes less than the pipe width
            upperPipes.pop(0)
            lowerPipes.pop(0)


        # displaying our objects to the screen
        SCREEN.blit(GAME_IMAGES['background'], (0,0))

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_IMAGES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_IMAGES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_IMAGES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_IMAGES['player'], (playerx, playery))

        myDgits = [int(x) for x in list(str (score))]
        width = 0
        
        for digit in myDgits:
            width += GAME_IMAGES['numbers'][digit].get_width()    
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDgits:
            SCREEN.blit(GAME_IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12 ))
            Xoffset += GAME_IMAGES['numbers'][digit].get_width()                        # blitting after 1st digit4

        if is_collide(playerx, playery, upperPipes, lowerPipes):
            SCREEN.blit(GAME_IMAGES['over'], (game_overx, game_overy))
        
        pygame.display.update()
        fpsclock.tick(FPS)
        


#----------------------------------------------------------------RANDOM PIPE---------------------------------------------------------------#



def getRandomPipe():
    # generating poitions of pipe to display on the screen
    pipeHeight = GAME_IMAGES['pipe'][0].get_height()                # getting the height of pipe
    offset = SCREENHEIGHT/3                                         # setting a particular distance that should be in the screen
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_IMAGES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENHEIGHT + 12
    y1 = pipeHeight - y2 + offset                                     
    pipe = [ 
        {'x' : pipeX, 'y' : -y1},                                   # (-) because this is for the upper pipe
        {'x' : pipeX, 'y' : y2}                                     #  lower pipe
    ]

    return pipe



#----------------------------------------------------------------IS COLLIDE---------------------------------------------------------------#



def is_collide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY -65 or playery < 0:                    # means when the playery value becomes negative
        GAME_AUDIO['die'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_IMAGES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_IMAGES['pipe'][0].get_width()):            # simply means when the player stucks in the height of pipe, it will crash
            GAME_AUDIO['die'].play()
            return True


    for pipe in lowerPipes:
        if (playery + GAME_IMAGES['player'].get_height() > pipe['y']) and abs (playerx - pipe['x']) < GAME_IMAGES['pipe'][0].get_width():
            GAME_AUDIO['die'].play()
            return True

    return False



#--------------------------------------------------------------MAIN FUNCTION--------------------------------------------------------------#



if __name__ == "__main__":
    pygame.init()                           # initializes all modules of pygame
    fpsclock = pygame.time.Clock()          
    pygame.display.set_caption("Flappy Bird by A_S")
    # now making the dictionary key contain tuple values
    GAME_IMAGES['numbers'] = (
        pygame.image.load("media//images//0.png").convert_alpha(),            # convert alpha is used for fast rendering of images
        pygame.image.load("media//images//1.png").convert_alpha(),
        pygame.image.load("media//images//2.png").convert_alpha(),
        pygame.image.load("media//images//3.png").convert_alpha(),
        pygame.image.load("media//images//4.png").convert_alpha(),
        pygame.image.load("media//images//5.png").convert_alpha(),
        pygame.image.load("media//images//6.png").convert_alpha(),
        pygame.image.load("media//images//7.png").convert_alpha(),
        pygame.image.load("media//images//8.png").convert_alpha(),
        pygame.image.load("media//images//9.png").convert_alpha()
    )


    GAME_IMAGES['base'] = pygame.image.load("media//images//base_img.png").convert_alpha()
    GAME_IMAGES['message'] = pygame.image.load("media//images//msg.png").convert_alpha()
    GAME_IMAGES['over'] = pygame.image.load("media//images//over.png").convert_alpha()
    GAME_IMAGES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),     #flips the image
        pygame.image.load(PIPE).convert_alpha()
    )

    GAME_AUDIO['die'] = pygame.mixer.Sound("media//audio//die.wav")
    GAME_AUDIO['hit'] = pygame.mixer.Sound("media//audio//hit.wav")
    GAME_AUDIO['point'] = pygame.mixer.Sound("media//audio//point.wav")
    GAME_AUDIO['swoosh'] = pygame.mixer.Sound("media//audio//swoosh.wav")
    GAME_AUDIO['wing'] = pygame.mixer.Sound("media//audio//wing.wav")

    GAME_IMAGES['background'] = pygame.image.load(BACKGROUND).convert()         # not used alpha because we don't need to run background image
    GAME_IMAGES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcome_screen()
        mainGame()
    
