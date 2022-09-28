import random # for generating random events in the game
import sys # for exiting the program or file
import pygame # Basic pygame functions
from pygame.locals import *

#Global variables for the game
FPS=32 # Rendering no. of images per second
SCREENWIDTH=289 # Screen dimensions based on trials and error
SCREENHEIGHT=511
GROUNDY= SCREENHEIGHT * 0.8 #80% of the screen(depending on prefere
#Initialize the screen taking the dimensions as arguments
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GAME_SPRITES={}  #Images that are going to be rendered in the game
GAME_SOUNDS={}  # Sounds that are going to be played throughout the game
PLAYER='gallery/sprites/bird.png'
BACKGROUND='gallery/sprites/background.png'
PIPE='gallery/sprites/pipe.png'

def WelcomeScreen():
    '''Shows the Welcome screen message for the game'''
    playerx= int(SCREENWIDTH/5) # X position of the player which is 1/5th of the screen width
    playery= int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex= int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey= int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        #pygame event gives us all the user interactions
        for event in pygame.event.get():
            # if user clicks the cross button, close the game
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if user clicks space or up arrow key, start game
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))        
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))        
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))        
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))        
                pygame.display.update()  #this function is necessary to update the display screen
                FPSCLOCK.tick(FPS)  #Controls the fps and maintains it. doesnt let it exceed the argument value
    
def isCollide(playerx,playery,Upperpipes,Lowerpipes):
    if playery >  GROUNDY - 25 or playery<0:
        GAME_SOUNDS['Hit'].play()
        return True

    for pipe in Upperpipes:
        pipeheight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeheight + pipe['y'] and abs(playerx-pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['Hit'].play()
            return True
    for pipe in Lowerpipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx-pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['Hit'].play()
            return True
def MainGame():
    score = 0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENWIDTH/2)
    basex= 0

    #Create 2 pipes for blitting on screen
    newpipe1= getRandomPipe()
    newpipe2= getRandomPipe()

    #upper pipes list
    Upperpipes=[ {'x':SCREENWIDTH+200,'y':newpipe1[0]['y']},
                 {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newpipe2[0]['y']},
    ]

    #lower pipes list
    Lowerpipes=[ {'x':SCREENWIDTH+200,'y':newpipe1[1]['y']},
                 {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newpipe2[1]['y']}
    ]

    #Velocity for pipe dictating how quickly the pipes show up
    PipeVelX= -4  # how fast the pipe is moving
    PlayerVely = -9 # speed with which the player is moving
    PlayerMaxVely = 10 # max limit 
    PlayerMinVely = -8 # min limit
    PlayerAccY = 1 # accelartion of the player

    PLayerAccV= -8 # velocity of the player while flapping 
    PlayerFlapped = False #It is true only when the bird is flapping
    #Main game loop
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key== K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type== KEYDOWN and (event.key==K_SPACE or event.key== K_UP):
                if playery > 0: # means if player in screen
                    PlayerVely = PLayerAccV
                    PlayerFlapped = True
                    GAME_SOUNDS['Wing'].play()

        crashTest = isCollide(playerx,playery,Upperpipes,Lowerpipes)
        # This function will return true when the player crashes or falls
        if crashTest:
            return

        # Check for score (tackling score- when to add score)
        PlayerMidPos = playerx + GAME_SPRITES['player'].get_width()/2                
        for pipe in Upperpipes:
            PipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if PipeMidPos<=PlayerMidPos < PipeMidPos + 4:
                score +=1
                print(f"Your score is{score}")
                GAME_SOUNDS['Point'].play
        if PlayerVely<PlayerMaxVely and not PlayerFlapped:
            PlayerVely += PlayerAccY
        if PlayerFlapped:
            PlayerFlapped=False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery= playery + min(PlayerVely,GROUNDY - playery - playerHeight)    


        #move pipes to the life
        for Upperpipe , Lowerpipe in zip(Upperpipes,Lowerpipes):
            Upperpipe['x']+=PipeVelX    
            Lowerpipe['x']+=PipeVelX    
        
        #Adding a new pipe befpre first pipe exits the screen from left
        if 0<Upperpipes[0]['x']<5:
            newpipe=getRandomPipe()
            Upperpipes.append(newpipe[0])
            Lowerpipes.append(newpipe[1])
        #if pipe is out of th screen remove it 
        if Upperpipes[0]['x']< -GAME_SPRITES['pipe'][0].get_width():
            Upperpipes.pop(0)
            Lowerpipes.pop(0)

        #Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        for Upperpipe , Lowerpipe in zip(Upperpipes,Lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (Upperpipe['x'],Upperpipe['y']))  
            SCREEN.blit(GAME_SPRITES['pipe'][1], (Lowerpipe['x'],Lowerpipe['y']))  
        SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        myDigits = [int(x) for x in list(str(score))] # gives back a list of the digits of the score
        width = 0  # width of the numbers(Score) taken up for blitting
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2  #gives us center

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))    
            Xoffset+= GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def getRandomPipe():
    """ Generating random positions of 2 pipes for blitting on screen. 1 straight(Bottom) and 1 rotated(Top)"""
    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3 #pipe height cant be less than this
    y2 = offset + random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipex= SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [ {'x': pipex, 'y':-y1}  #upperpipe thats why y is minus
             ,{'x':pipex,'y':y2}]    #lower pipe
    
    return pipe

if __name__ == "__main__":
    #main funnction for the game from where the game/code initializes
    pygame.init() # initializes all pygame modules
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption(' My Flappy Bird')
    GAME_SPRITES['numbers']=(
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),  #Convertalpha optimizes the image for the game by blitting it faster
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    GAME_SPRITES['message']=pygame.image.load('gallery/sprites/msg.png').convert_alpha()
    GAME_SPRITES['base']=pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe']=(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()) 
        #transform rotate functions rotats the given image based on the passed argument
    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()

    #GAME SOUNDS
    GAME_SOUNDS['Die']=pygame.mixer.Sound('gallery/audio/Die.mp3')
    GAME_SOUNDS['Swoosh']=pygame.mixer.Sound('gallery/audio/Swoosh.mp3')
    GAME_SOUNDS['Point']=pygame.mixer.Sound('gallery/audio/Point.mp3')
    GAME_SOUNDS['Hit']=pygame.mixer.Sound('gallery/audio/Hit.mp3')
    GAME_SOUNDS['Wing']=pygame.mixer.Sound('gallery/audio/Wing.mp3')

    while True:
        WelcomeScreen() #Shows the welcome screen unless the player presses a button
        MainGame()   # This is the main function of the game that defines it
