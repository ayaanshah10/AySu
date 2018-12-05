


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
        
        # if self.x >= g.w // 2:
        #     g.x += self.vx
        
        # if self.x-self.r < 0:
        #     self.x = self.r
        

a = Creature(100,100,100,400)
rambo = Rambo(100,100,100,400)                
def setup():
    size(500,500)
    background(255)

def draw():
    background(255)
    stroke(0)
    line(0,a.g,500,a.g)
    
    rambo.display()
    noFill()
    stroke(255,0,0)
    ellipse(rambo.x,rambo.y,rambo.r,rambo.r)
    
def keyPressed():
    if keyCode == LEFT:
        rambo.keyHandler[LEFT] = True
    elif keyCode == RIGHT:
        rambo.keyHandler[RIGHT] = True
    elif keyCode == UP:
        rambo.keyHandler[UP] = True
    elif keyCode == 80:
        if rambo.pause:
            rambo.pause = False
        else:
            rambo.pause = True
        
def keyReleased():
    if keyCode == LEFT:
        rambo.keyHandler[LEFT] = False
    elif keyCode == RIGHT:
        rambo.keyHandler[RIGHT] = False
    elif keyCode == UP:
        rambo.keyHandler[UP] = False    
    
        
    
