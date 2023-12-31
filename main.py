import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox

# CUBES - rectangles which snake is build from.
class cube(object):
    rows = [32, 24] # rows[0] = number of columns on board, rows[1] = number of rows on  board
    #   creen resolution (w = width, h = height)
    w = 800
    h = 600 

    def __init__(self, start, dirnx = 1, dirny = 0, color = (255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes = False):
        disx = self.w // self.rows[0]           #  width of cube

        disy = self.h // self.rows[1]           # height of cube
        drawPositionX = self.pos[0] * disx      # start horizontal drawing pos for cube
        drawPositionY = self.pos[1] * disy      # start vertical drawing pos for cube 

        pygame.draw.rect(surface, self.color, (drawPositionX, drawPositionY, disx, disy))       # draw rectangle
        
        if eyes:        # snake eyes
            centre = disx / 2
            radius = 3
            eye1 = (drawPositionX+centre+(radius*2), drawPositionY+8)
            eye2 = (drawPositionX+centre-(radius*2), drawPositionY+8)
            
            pygame.draw.circle(surface, (0, 255, 0), eye1, radius)
            pygame.draw.circle(surface, (0, 255, 0), eye2, radius)

class snake(object):
    body = []
    turns = {}
    
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1 
    
    def move(self):
        for event in pygame.event.get():        # events --> keyboard, mouse click 
            
            if event.type == pygame.QUIT:       # exit game window if 'X' preessed on app window
                exit()

            keys = pygame.key.get_pressed()

            for key in keys:    # sets keyboard keys for moving snake: [W, S, A, D] or [UP, DOWN, LEFT, RIGHT]

                if keys[pygame.K_DOWN] or keys[pygame.K_s]:     
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
               
                elif keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                
                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
               
                elif keys[pygame.K_RIGHT]  or keys[pygame.K_d]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        
        for i,c in enumerate(self.body):
            p = c.pos[:]
        
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                
                if i == len(self.body)-1:
                    self.turns.pop(p)
           
            else:       # sets where snake will appear if cross screen border 
                if c.dirnx ==-1 and c.pos[0] <= 0: c.pos = (c.rows[0]-1, c.pos[1])

                elif c.dirnx ==1 and c.pos[0] >= c.rows[0]-1: c.pos = (0, c.pos[1])

                elif c.dirny ==1 and c.pos[1] >= c.rows[1]-1: c.pos = (c.pos[0], 0)

                elif c.dirny ==-1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows[1]-1)

                else: c.move (c.dirnx, c.dirny)
        

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self,):     # sets snakes' new tail element position after eating snack
        tail = self.body[-1] 
        dx, dy = tail.dirnx, tail.dirny
       
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
      
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
      
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
      
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        
    
    def draw(self, surface):
        for i, c in enumerate(self.body):
      
            if i  == 0:
                c.draw(surface, True)
      
            else:
                c.draw(surface)

# SETS DRAW GRID PARAMETERS
def drawGrid (w, h, rows, surface):
    wSizeBtween = WIDTH // rows[0]
    hSizeBtween = HEIGHT // rows[1]
    x = 0
    y = 0
    
    for lines in range(rows[0]):        # draw a vertical grid lines 
        x = x + wSizeBtween
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, h)) 
    
    for lines in range(rows[1]):        # draw horizontal grid lines
        y = y + hSizeBtween
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

def redrawWindow(surface):
    global WIDTH, HEIGHT, rows,s , snack
   
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(WIDTH, HEIGHT,  rows, surface)
    pygame.display.update()
    
def randomSnack(rows, item):        # sets snack position
    positions = item.body
    xlen = rows[0]
    ylen = rows[1]

    while True:
        x = random.randrange(xlen)
        y = random.randrange(ylen)   
        
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:      # anonymus function compares element (z) position to (x,y) from item body 
            continue
        else:
            break
    return (x,y)
  


def message_box(subject, content):      # message_box popup after win or lose
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
    
def main():
    global WIDTH, HEIGHT, rows ,s, snack
    WIDTH = 800
    HEIGHT = 600
    rows = [32, 24]     # number of rows horizontal [0] and vertical [1]
    win = pygame.display.set_mode((WIDTH, HEIGHT))      # set a window resolution
    pygame.display.set_caption("SNAKE TRY TO REACH")     # set a display heading  
    s = snake((0, 255, 255),(10,10)) # defines colour of snake , and start position
    snack = cube(randomSnack(rows, s), color = (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    clock = pygame.time.Clock()     # sets time clock of app
    run = True
    
    
    while run:
        pygame.time.delay(100)       
        clock.tick(20)
        s.move() 
        
        if len(s.body) == 100:
            print('Score: ', len(s.body))
            message_box('You WON!', f"Score: {len(s.body)}  Play again..!")
            s.reset((10,10))
            break
        
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color = (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        
        for x in range(len(s.body)): 
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', f"Score: {len(s.body)} Play again..!")
                s.reset((10,10))
                break

        redrawWindow(win)
  
main()

