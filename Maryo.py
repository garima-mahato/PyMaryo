#import modules

import pygame,random,sys
from pygame.locals import*
pygame.init()

window_height=600
window_width=1200

fps=25
level=0
addnewflamerate=20

white=(255,255,255)
black=(0,0,0)

#creating object classes

class dragon:

    global firerect,cactusrect,imagerect,Canvas
    up=False
    down=True
    velocity=15

    def __init__(self):
        self.image=load_image('image/dragon.png')
        self.imagerect=self.image.get_rect()
        self.imagerect.top=window_height/2
        self.imagerect.right=window_width
        self.life=10

    def update(self):
        if(self.imagerect.top<cactusrect.bottom):
            self.up=False
            self.down=True
        if(self.imagerect.bottom>firerect.top):
            self.down=False
            self.up=True
        if(self.down):
            self.imagerect.bottom+=self.velocity
        if(self.up):
            self.imagerect.top-=self.velocity
        Canvas.blit(self.image,self.imagerect)

    def return_height(self):
        return self.imagerect.top

class flames:
    global Canvas
    flamespeed=20

    def __init__(self):
        self.image=load_image('image/fireball.png')
        self.imagerect=self.image.get_rect()
        self.height = Dragon.return_height() + 20
        self.surface = pygame.transform.scale(self.image, (20,20))
        self.imagerect = pygame.Rect(window_width - 106, self.height, 20, 20)

    def update(self):
        self.imagerect.left-=self.flamespeed

    def collision(self):
        if self.imagerect.left <= 0:
            return True
        else:
            return False

class weapon:
    global Canvas
    flamespeed=40

    def __init__(self):
        self.image=load_image('image/fireball.png')
        self.imagerect=self.image.get_rect()
        self.height = player.return_height()  + 20
        self.width = player.return_width()
        self.surface = pygame.transform.scale(self.image, (20,20))
        self.imagerect = pygame.Rect(self.width , self.height, 20, 20)

    def update(self):
        self.imagerect.right+=self.flamespeed

    def collision(self):
        if self.imagerect.right >= window_width:
            return True
        else:
            return False
            

class maryo:
    global moveup,movedown,gravity,cactusrect,firerect,Canvas,moveright,moveleft,hit
    speed=10                     
    downspeed=20                 

    def __init__(self):
        self.image=load_image('image/maryo.png')
        self.imagerect=self.image.get_rect()
        self.imagerect.topleft=(50,window_height/2)
        self.score=0

    def update(self):
        if(moveup and(self.imagerect.top > cactusrect.bottom)):
            self.imagerect.top-=self.speed
            self.score+=1

        if(movedown and(self.imagerect.bottom < firerect.top)):
            self.imagerect.bottom+=self.downspeed
            self.score+=1

        if(gravity and(self.imagerect.bottom < firerect.top)):
            self.imagerect.bottom+=self.speed

        if(moveleft and(self.imagerect.left > 0)):
            self.imagerect.left-=self.speed
            self.score+=1

        if(moveright and(self.imagerect.right < window_width)):
            self.imagerect.right+=self.speed
            self.score+=1

       

    def return_height(self):
        return self.imagerect.top

    def return_width(self):
        return self.imagerect.right

#helper functions

def terminate():                  #to end program
    pygame.quit()
    sys.exit()

def waitforkey():                 #to detect key press
    while True:                   #to wait for user to start
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                terminate()
            if event.type==pygame.KEYDOWN:  #to terminate if user presses escape key
                if event.key==pygame.K_ESCAPE:
                    terminate()
                return

def flamehitsmario(playerrect,flame_list):  #to check if flame has hit mario or not
    for f in flame_list:
        if playerrect.colliderect(f.imagerect):
            return True
        return False

def dragonhitsmario(playerrect,dragonrect):
    if playerrect.colliderect(dragonrect):
        return True
    return False

def weaponhitsdragon(Dragonrect,w):  #to check if weapon has hit dragon or not
    if Dragonrect.colliderect(w.imagerect):
        return True
    else:
        return False

def drawtext(text,font,surface,x,y):         #to display text on screen
    textobj=font.render(text,1,white)
    textrect=textobj.get_rect()
    textrect.topleft=(x,y)
    surface.blit(textobj,textrect)

def check_level(score):       #to check the level
    global window_height,level,cactusrect,firerect
    if score in range(0,250):
        level = 1
        firerect.top = window_height - 50
        cactusrect.bottom = 50
    elif score in range(250, 500):
        firerect.top = window_height - 100
        cactusrect.bottom = 100
        level = 2
    elif score in range(500,750):
        level = 3
        firerect.top = window_height-150
        cactusrect.bottom = 150
    elif score in range(750,1000):
        level = 4
        firerect.top = window_height - 200
        cactusrect.bottom = 200
        
def load_image(imagename):      #to load images
    return pygame.image.load(imagename)

def savegame(score,topscore,level,playerrect):
    fo=open('game.txt','w')
    txt=str(score)+' '+str(topscore)+' '+str(level)+' '+str(playerrect.left)+' '+str(playerrect.top)
    fo.write(txt)
    fo.close()

def loadgame():
    fo=open('game.txt','r')
    txt=fo.read()+' '
    fo.close()
    list=[]
    j=0
    s=''
    for i in txt:
        if i != ' ':
            s=s+i
        else:
            list.append(s)
            s=''
            j=j+1
    return list
        
#resource handling

mainClock=pygame.time.Clock()
Canvas=pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Maryo')

font=pygame.font.SysFont(None,48)
scorefont=pygame.font.SysFont(None,30)

fireimage=load_image('image/fire_bricks.png')
firerect=fireimage.get_rect()

cactusimage=load_image('image/cactus_bricks.png')
cactusrect=cactusimage.get_rect()


startimage=load_image('image/start.png')
startimagerect=startimage.get_rect()
startimagerect.centerx=window_width/2
startimagerect.centery=window_height/2

endimage=load_image('image/end.png')
endimagerect=endimage.get_rect()
endimagerect.centerx=window_width/2
endimagerect.centery=window_height/2

pygame.mixer.music.load('music/mario_theme.wav')
gameover=pygame.mixer.Sound('music/mario_dies.wav')

#start screen
drawtext('Mario',font,Canvas,(window_width/3),(window_height/3))
Canvas.blit(startimage,startimagerect)
pygame.display.update()

#initialize the game

waitforkey()
topscore=0




while True:
    Dragon=dragon()
    flame_list=[]     #create a list of the flames
    weapon_list=[]
    l=[]
    player=maryo()
    moveup=movedown=gravity=moveleft=moveright=hit=False
    flameaddcounter=0

    gameover.stop()
    pygame.mixer.music.play(-1,0.0)   #play the music

#main game loop

    while True:    #begin the loop
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            
            if event.type==KEYDOWN:
                if event.key==K_UP:
                    movedown = False
                    moveup = True
                    gravity = False
                    moveleft = False
                    moveright = False
                if event.key==K_DOWN:
                    movedown = True
                    moveup = False
                    gravity = False
                    moveleft = False
                    moveright = False
                if event.key==K_LEFT:
                    movedown = False
                    moveup = False
                    gravity = False
                    moveleft = True
                    moveright = False
                if event.key==K_RIGHT:
                    movedown = False
                    moveup = False
                    gravity = False
                    moveleft = False
                    moveright = True
                if event.key==K_h:
                    hit=True
                if event.key==K_s:
                    savegame(player.score,topscore,level,player.imagerect)
                if event.key==K_l:
                    l=loadgame()

            if event.type==KEYUP:
                if event.key==K_UP:
                    moveup=False
                    gravity=True
                if event.key==K_DOWN:
                    movedown=False
                    gravity=True
                if event.key==K_LEFT:
                    moveleft=False
                    gravity=True
                if event.key==K_RIGHT:
                    moveright=False
                    gravity=True
                if event.key==K_h:
                    hit=False
                if event.key==K_s:
                    terminate()
                if event.key==K_l:
                    player.score=int(l[0])
                    topscore=int(l[1])
                    level=int(l[2])
                    player.imagerect.topleft=(int(l[3]),int(l[4]))
                if event.key==K_ESCAPE:
                    terminate()
        
        flameaddcounter+=1
        check_level(player.score)

        if flameaddcounter == addnewflamerate:     #condition to create flame
            flameaddcounter=0
            newflame=flames()
            flame_list.append(newflame)

        for f in flame_list:
            flames.update(f)

        for f in flame_list:
            if f.collision()== True:                                #condition to remove flame
                flame_list.remove(f)                                #remove flame

        if hit and (len(weapon_list) == 0):
            newweapon=weapon()
            weapon_list.append(newweapon)

        for w in weapon_list:
            weapon.update(w)

        for w in weapon_list:
            if w.collision()== True:                                #condition to remove flame
                weapon_list.remove(w)

        player.update()
        Dragon.update()

        Canvas.fill(black)        #fill up the screen!
        Canvas.blit(fireimage,firerect)
        Canvas.blit(cactusimage,cactusrect)
        Canvas.blit(player.image,player.imagerect)
        Canvas.blit(Dragon.image,Dragon.imagerect)

        #display score
        drawtext('Score : %s | Top score : %s | Level : %s' %(player.score, topscore, level), scorefont, Canvas, 350, cactusrect.bottom + 10)
        drawtext('Press H to hit the dragon | Press S to save the game | Press L to load the saved game', scorefont, Canvas, 100, cactusrect.bottom + 40)

        for f in flame_list:
            Canvas.blit(f.surface,f.imagerect)

        for w in weapon_list:
            Canvas.blit(w.surface,w.imagerect)

        for w in weapon_list:
            if weaponhitsdragon(Dragon.imagerect,w):
                player.score+=1
                Dragon.life-=1
            if Dragon.life <= 0:
                drawtext('You Win' , font, Canvas, 600, 300)
                pygame.display.update()
                break
            
        if Dragon.life <= 0:
            drawtext('You Win' , font, Canvas, 600, 300)
            pygame.display.update()
            break

        if flamehitsmario(player.imagerect,flame_list):
            if player.score > topscore:
                topscore = player.score
            break

        if dragonhitsmario(player.imagerect,Dragon.imagerect):
            if player.score > topscore:
                topscore = player.score
            break
        
        if ((player.imagerect.top <= cactusrect.bottom) or (player.imagerect.bottom >= firerect.top)):
            if player.score > topscore:
                topscore = player.score
            break

        pygame.display.update()

        mainClock.tick(fps)

    #play game over music
    pygame.mixer.music.stop()
    gameover.play()
    #display end image.
    if Dragon.life <= 0:
        drawtext('You Win' , font, Canvas, 600, 300)
        pygame.display.update()
    Canvas.blit(endimage,endimagerect)
    pygame.display.update()
    waitforkey()                
    
    
