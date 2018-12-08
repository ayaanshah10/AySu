import os
path = os.getcwd()

def detectcollision(x1,y1,w1,h1,x2,y2,w2,h2):
        if (x2+w2>=x1>=x2 and y2+h2>=y1>=y2): 
            return True
        elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1>=y2): 
            return True
        elif (x2+w2>=x1>=x2 and y2+h2>=y1+h1>=y2): 
            return True
        elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1+h1>=y2): 
            return True
        else: 
            return False

# def collision(a,b):
#     if a.x >= b.x and a.x <= b.x + b.w:
#         a.y + a.h > b.y: # checking collision with ground
#             True
#     False

class Creature:
    def __init__(self,x,y,w,h,img,pw,ph,F):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.F = F
        self.pw = pw
        self.ph = ph
        self.vx = 0 #velocity horizontally
        self.vy = 0 #velocity vertically
        self.dir = 1
        self.img = loadImage(path+"/images/"+img)
        
    def gravity(self):
        self.vy += 0.2
    
    def update(self):
        self.gravity()
        
        self.x += self.vx #present location will be updated to present location + velocity
        self.y += self.vy
        
    def display(self):
        self.update() #displays the update
        
class Rambo(Creature): #inheriting from creature
    def __init__(self,x,y,w,h,img,pw,ph,F):
        Creature.__init__(self,x,y,w,h,img,pw,ph,F)
        self.keyHandler={LEFT:False, RIGHT:False, UP:False} #movement
        self.img=loadImage(path+"/images/rambo.png")
        self.f = 0
    def update(self, blocks):
        self.gravity()
        if self.keyHandler[LEFT]:
            self.vx = -5
            self.dir = -1
        elif self.keyHandler[RIGHT]:
            self.vx = 5
            self.dir = 1
        else:
            self.vx = 0
        
        
        if self.keyHandler[UP] :
            for i in blocks:
                if detectcollision(self.x,self.y,self.w,self.h,i.x,i.y,i.w,i.h):
                     self.vy = -7
                    
            
            #, check if i collide with rambo - then up, else nothing
            
          
        self.x += self.vx #present location will be updated to present location + velocity
        self.y += self.vy
        
        if self.x >= g.w // 2: #center him
            g.x += self.vx
    
    def display(self, blocks):
        self.update(blocks)
        
        if self.vx != 0 and self.vy == 0:
            self.f = (self.f+0.3)%self.F
        
        image(self.img,self.x,self.y,self.w,self.h,int(self.f)*self.w//2,0,int(self.f+1)*self.w//2,self.h)
        
        
class Skeletons(Creature):
    def __init__(self,x,y,w,h,x1,x2,img,pw,ph,F):
       Creature.__init__(self,x,y,w,h,img,pw,ph,F)
       self.vx = 2
       self.x1 = x1
       self.x2 = x2
       self.img = loadImage(path+"/images/gunda.png")
    def update(self):
        self.gravity()
        
        if self.x > self.x2 :
            self.vx = -2
            self.dir = -1
        elif self.x < self.x1:
            self.vx = 2
        self.dir = 1
        
        self.x += self.vx
        self.y += self.vy
            
    def display(self):
        self.update()
        rect(self.x,self.y,self.w,self.h)

class Block:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(path+"/images/ground.png")
            
    def display(self):
        image(self.img,self.x-g.x,self.y)
        
class Game:
    def __init__ (self,w,h):
        self.w=w
        self.h=h
        self.x = 0
        self.frames = 0
        
        self.rambo = Rambo(100,100,100,100,"rambo.png",50,6,10) #Calling Rambo
        
        self.enemies1=[]
        for i in range(1):
            self.enemies1.append(Skeletons(300+i*100,50,35,35,300,900,"gunda.png",11,22,5))
        
        self.blocks = []
        for i in range(13):
            self.blocks.append(Block(0+i*128,585,128,128))
    
    def update(self):
        for i in self.blocks:
            #print("self.rambo.x,self.rambo.y,self.rambo.w,self.rambo.h,i.x,i.y,i.w,i.h",self.rambo.x,self.rambo.y,self.rambo.w,self.rambo.h,i.x,i.y,i.w,i.h)
            if detectcollision(self.rambo.x,self.rambo.y,self.rambo.w,self.rambo.h,i.x,i.y,i.w,i.h):
                self.rambo.y = i.y - self.rambo.h
                self.rambo.vy = 0
                
        for i in self.blocks:
            for r in self.enemies1:
                #print("r.x,r.y,r.w,r.h,i.x,i.y,i.w,i.h",r.x,r.y,r.w,r.h,i.x,i.y,i.w,i.h)
                if detectcollision(r.x,r.y,r.w,r.h,i.x,i.y,i.w,i.h):
                    r.y = i.y - r.h
                    r.vy = 0
                
                
                        

    def display(self):
        self.update()
        for b in self.blocks:
            b.display()
            
        
        
g = Game(1280,720)  

              
def setup():
    size(g.w,g.h)
    background(255)

def draw():
    background(255)
    g.display()
    
    g.rambo.display(g.blocks)
    
    noFill() 
    stroke(255,0,0)
    rect(g.rambo.x-g.x,g.rambo.y,g.rambo.w,g.rambo.h) #placeholder for rambo
    
    noFill() 
    stroke(0,255,0)
    for skelly in g.enemies1:
        skelly.display()
    
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
    

    
    
        
    
