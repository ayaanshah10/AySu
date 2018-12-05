


class Creature:
    def __init__(self,x,y,r,g):
        self.x = x
        self.y = y
        self.r = r
        self.g = g #ground
        self.vx = 0 #velocity horizontally
        self.vy = 0 #velocity vertically
        self.dir = 1
        
    def gravity(self):
        if self.y + self.r//2  >= self.g: # we are using r//2 because r is diameter
            self.vy = 0
        else:
            self.vy += 0.2
            if self.y + self.r//2 + self.vy > self.g:
                self.vy = self.g - (self.y+self.r//2)
    
    def update(self):
        self.gravity()
        
        self.x += self.vx #present location will be updated to present location + velocity
        self.y += self.vy

        
    def display(self):
        self.update() #displays the update
        
class Rambo(Creature): #inheriting from creature
    def __init__(self,x,y,r,g):
        Creature.__init__(self,x,y,r,g)
        self.keyHandler={LEFT:False, RIGHT:False, UP:False} #movement
    
    def update(self):
        self.gravity()
        if self.keyHandler[LEFT]:
            self.vx = -5
            self.dir = -1
        elif self.keyHandler[RIGHT]:
            self.vx = 5
            self.dir = 1
        else:
            self.vx = 0
        
        if self.keyHandler[UP] and self.y+self.r//2 == self.g:
            self.vy = -7 
          
        
        self.x += self.vx #present location will be updated to present location + velocity
        self.y += self.vy
        
class Game:
    def __init__ (self,w,h,g):
        self.w=w
        self.h=h
        self.g=g
        self.x = 0
        self.frames = 0
        
        self.rambo = Rambo(100,100,100,self.g) #Calling Rambo
        


g = Game(1280,720,585)                
def setup():
    size(g.w,g.h)
    background(255)

def draw():
    background(255)
    stroke(0)
    line(0,g.g,g.w,g.g)
    
    g.rambo.display()
    noFill()
    stroke(255,0,0)
    ellipse(g.rambo.x,g.rambo.y,g.rambo.r,g.rambo.r)
    
def keyPressed():
    if keyCode == LEFT:
        g.rambo.keyHandler[LEFT] = True
    elif keyCode == RIGHT:
        g.rambo.keyHandler[RIGHT] = True
    elif keyCode == UP:
        g.rambo.keyHandler[UP] = True
    elif keyCode == 80:
        if g.rambo.pause:
            g.rambo.pause = False
        else:
            g.rambo.pause = True
        
def keyReleased():
    if keyCode == LEFT:
        g.rambo.keyHandler[LEFT] = False
    elif keyCode == RIGHT:
        g.rambo.keyHandler[RIGHT] = False
    elif keyCode == UP:
        g.rambo.keyHandler[UP] = False    
    
        
    
