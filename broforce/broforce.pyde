


class Creature:
    def __init__(self,x,y,r,g):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.vx = 0
        self.vy = 0
        
    def gravity(self):
        if self.y + self.r//2  >= self.g:
            self.vy = 0
        else:
            self.vy += 0.2
            if self.y + self.r//2 + self.vy > self.g:
                self.vy = self.g - (self.y+self.r//2)
                
        
    def update(self):
        self.gravity()
        
        self.x += self.vx
        self.y += self.vy
        print(self.x,self.y,self.r,self.g,self.vy)
        
    def display(self):
        self.update()
        
        

a = Creature(100,100,100,400)
                
def setup():
    size(500,500)
    background(255)

def draw():
    background(255)
    stroke(0)
    line(0,a.g,500,a.g)
    
    a.display()
    noFill()
    stroke(255,0,0)
    ellipse(a.x,a.y,a.r,a.r)
    
    
    
    
        
    
