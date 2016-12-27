#Imports
import pygame,sys,random,math
from random import randint
from pygame.locals import *


#A firework    
class Firework(pygame.sprite.Sprite):

    #Init function
    def __init__(self,location,size,angle,color,timer,density):
        pygame.sprite.Sprite.__init__(self)
        
        self.location = location
        self.velocity = [math.sin(float(angle))*3,
                    -math.cos(float(angle))*3]
        self.size = size
        
        self.color = color
        print color
        self.image = pygame.surface.Surface((size,size))
        self.image.fill(color)
        
        self.angle = float(angle)

        self.ps = []

        self.timer = timer
        self.density = density

    def explode(self,exp):
        if exp == "NORMAL":
            for i in range(self.density):
                particle = Particle(self.location[:],[0,0.05],self.size,random.randint(0,360),self.color,random.randint(70,80))
                self.ps.append(particle)
              
    #Update and render
    def update(self):

        self.timer -= 0.5

        if self.ps:
            for p in self.ps:
                p.update()
            return

        if self.timer <= 0:
            self.explode("NORMAL")
            return

        if self.location[0] < 0 or self.location[0] > screen.get_width() or self.location[1] < 0 or self.location[1] > screen.get_height():
            return             

        self.location[0] += self.velocity[0]
        self.location[1] += self.velocity[1]
        
        screen.blit(self.image,self.location)

class Particle(pygame.sprite.Sprite):

    #Init function
    def __init__(self,location,acceleration,size,angle,color,death):
        pygame.sprite.Sprite.__init__(self)
         
        self.location = location
        self.velocity = [math.sin(float(angle))*3,
                    -math.cos(float(angle))*3]
        self.acceleration = acceleration
        self.size = size
        
        self.color = color
        self.image = pygame.surface.Surface((size,size))
        self.image.fill(color)
        
        self.angle = float(angle)
        self.life = 0
        self.death = death
 
    #Update and render
    def update(self):

        self.life += 1

        if self.life >= self.death:
            return

        if self.location[0] < 0 or self.location[0] > screen.get_width() or self.location[1] < 0 or self.location[1] > screen.get_height():
            return

        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        self.location[0] += self.velocity[0]
        self.location[1] += self.velocity[1]
        
        screen.blit(self.image,self.location)


#Random rgb color
def randcolor():
    return [random.randint(128,255),random.randint(0,255),random.randint(0,255)]

#Find in a list
def locate(item,listx):
    for i in range(0,len(listx)):
        if listx[i] == item:
            return i


def checkQuit():
    for event in pygame.event.get():
        if event.type == QUIT:  
            pygame.quit()
            sys.exit()

#Inits
pygame.init()

#A clock object for keeping track of fps
clock = pygame.time.Clock()

#The font used on the panel. 18 pixels high
font = pygame.font.Font("freesansbold.ttf",18)
TEXTCOLOR = (255,255,255)

#Set up the screen
screen = pygame.display.set_mode((1024,640))
pygame.display.set_caption("FWSIM Clone")

#List[s] of colors
COLORS = [[255,255,255], #White
          [255,64,0],    #Red
          [255,128,0],   #Orange
          [255,204,0],   #Yellow-orange
          [192,255,0],   #Yellow-green
          [64,255,0],    #Bright green
          [0,255,128],   #Sea green
          [0,255,255],   #Aqua
          [0,128,255],   #Turquoise
          [0,48,255],    #Bright blue
          [128,0,255],   #Indigo
          [255,54,155],   #Pink
          [255,0,0]]     #Red

REDWHITEBLUE = [[255,255,255], #White
                [255,64,0],    #Red
                [0,48,255]]    #Bright blue


#Parse the FWML

clock.tick()
        
fwml = open("Sample.fwml","r")

lines = fwml.readlines()

fwml.close()

colorpalette = lines[0]
if colorpalette == "SPECTRUM        \n":
    colorpalette = COLORS
elif colorpalette == "REDWHITEBLUE    \n":
    colorpalette = REDWHITEBLUE

ticks = []
for line in lines[1:]:
    ticks.append(int(line[0:4]))

timers = []
for line in lines[1:]:
    timers.append(int(line[5:8]))

locations = []
for line in lines[1:]:
    locations.append([int(randint(0,950)),
                      int(640)])

sizes = []
for line in lines[1:]:
    sizes.append(int(line[19:22]))
    
angles = []
for line in lines[1:]:
    angles.append(int(line[23:26]))
    
colors = []
for line in lines[1:]:
    colors.append(int(line[27:30]))

densities = []
for line in lines[1:]:
    densities.append(int(line[31:34]))

fireworks = []
phase = 0

loadtime = clock.tick()
print("Loading time: " + str(loadtime) + " Milliseconds")

print locations
x_pos = 200
y_pos = 525

#london pictures
eye = pygame.image.load('london_eye.png')
eye = pygame.transform.scale(eye,(300,300))
ben = pygame.image.load('bigben.png')
ben = pygame.transform.scale(ben,(40,200))
bridge = pygame.image.load('bridge.png')
bridge = pygame.transform.scale(bridge,(200,200))
themes = pygame.image.load('themes.png')
themes = pygame.transform.scale(themes,(120,120))
banner = pygame.image.load('banner.jpg')
banner = pygame.transform.scale(banner,(100,50))
wall = pygame.image.load('wall3.png')
wall = pygame.transform.scale(wall,(50,100))

#grass
grass = pygame.image.load('grass.png')
grass = pygame.transform.scale(grass,(230,100))

player = pygame.image.load('sprite1.png')
counter = 0
stepsAnimation = 0
direction = 2
while True:

    screen.fill((0,0,0))
    checkQuit()

    if x_pos <900:
        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            stepsAnimation += 1
            if stepsAnimation %8 == 0:
                counter = (counter + 1) % 4    #because 4 steps animation

        if keys[pygame.K_RIGHT]:
            direction = 2
            if (y_pos>=475.5 and y_pos<515.5 and x_pos>686 and x_pos<695) or (y_pos>558.5 and x_pos>808 and x_pos<820):
                print 3
            else:
                x_pos += 1.5
            #print x_pos
        if keys[pygame.K_LEFT]:
            direction = 1
            if x_pos > 0:
                x_pos -= 1.5
            #print x_pos
        if keys[pygame.K_UP]:
            direction = 3
            if y_pos > 475.5:
                y_pos -= 1.5
            #print y_pos
        if keys[pygame.K_DOWN]:
            direction = 0
            if y_pos < 577.5:
                y_pos += 1.5
            #print y_pos
    else:  
        if phase in ticks:
            index = locate(phase,ticks)
            if(colors[index]==11):
                fw = Firework(locations[index],sizes[index],angles[index],colorpalette[colors[index]],timers[index],densities[index])
            else:
                fw = Firework(locations[index],sizes[index],angles[index],colorpalette[randint(0,12)],timers[index],densities[index])
            fireworks.append(fw)

        for fw in fireworks:
            fw.update()
        
        phase += 1
        clock.tick(100)

    #grass rectangle
    pygame.draw.rect(screen, [40,183,24], (0,550,1200,500), 0)

    
    screen.blit(eye,(150,250))
    screen.blit(ben,(330,350))
    screen.blit(bridge,(0,350))
    

    y_grass=450
    while y_grass < 570:
        x_grass = 0
        while x_grass < 1000:
            screen.blit(grass,(x_grass,y_grass))
            x_grass += 200
        y_grass += 20

    screen.blit(wall,(710,470))
    pygame.draw.lines(screen, [131,92,59], False, [(750,570),(750,450),(850,450)], 3)
    if x_pos >=900:
        screen.blit(player,(x_pos,y_pos),((192/4)*0,(256/4)*3,192/4,256/4))
    else:
        screen.blit(player,(x_pos,y_pos),((192/4)*counter,(256/4)*direction,192/4,256/4))
    pygame.draw.lines(screen, [131,92,59], False, [(850,450),(850,600)], 3)
    screen.blit(wall,(840,550))
    #screen.blit(themes,(60,520))
    screen.blit(banner,(750,450))
    

    pygame.display.update()
    

        

    

    
