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
            return  False

class Creature:
    def __init__(self,x,y,w,h,img,F):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.F = F
        self.f = 0
        #self.pw = pw
        #self.ph = ph
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
    def __init__(self,x,y,w,h,img,F):
        Creature.__init__(self,x,y,w,h,img,F)
        self.keyHandler={LEFT:False, RIGHT:False, UP:False, 32:False} #movement
        self.img=loadImage(path+"/images/rambo.png")
        self.blockBullet = 0
        
    def update(self, blocks):
        if self.blockBullet > 0:
            self.blockBullet -= 1
            
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
            
        self.x += self.vx #present location will be updated to present location + velocity
        self.y += self.vy
        
        if self.x >= g.w // 2: #center him
            g.x += self.vx
        
        
        #don't let him jump from below a platform
        for b in g.blocks:
            if b.x <= self.x and self.x <= b.x + b.w:
                if b.y <= self.y:
                    if self.y <= b.y + b.h + 30 and self.y >= b.y + b.h :
                        self.vy = 7
                            
                                
        if self.keyHandler[32] and self.blockBullet == 0 and self.dir == 1:
            self.blockBullet = 60
            g.bullets.append(Bullet(self.x+self.w-g.x,self.y+(self.h)/8,10,10,self.x+self.w-g.x+300,self.x+self.w-g.x-300))
        elif self.keyHandler[32] and self.blockBullet == 0 and self.dir == -1:
            self.blockBullet = 60
            g.bullets.append(Bullet(self.x+-g.x,self.y+(self.h)/8,10,10,self.x+self.w-g.x+300,self.x+self.w-g.x-300))
            
    def display(self, blocks):
        self.update(blocks)
        
        if self.vx != 0: #self.vy == 0:
            self.f = (self.f+0.3)%self.F
        
        if self.dir > 0:
            image(self.img,self.x-g.x,self.y,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x-g.x,self.y,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)
        
class Skeletons(Creature):
    def __init__(self,x,y,w,h,x1,x2,img,F):
       Creature.__init__(self,x,y,w,h,img,F)
       self.vx = 2
       self.x1 = x1
       self.x2 = x2
       self.img = loadImage(path+"/images/Zombie1.png")
    def update(self):
        self.gravity()
        
        if self.x > self.x2 :
            self.vx = -2
            self.dir = 1
        elif self.x < self.x1:
            self.vx = 2
            self.dir = -1
        
        self.x += self.vx
        self.y += self.vy
            
    def display(self):
        self.update()
        
        if self.vx != 0: #self.vy == 0:
            self.f = (self.f+0.05)%self.F
            
        if self.dir > 0:
            image(self.img,self.x-g.x,self.y,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x-g.x,self.y,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)
        
        
    
class Block:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(path+"/images/ground.png")
            
    def display(self):
        image(self.img,self.x-g.x,self.y)

class Bullet:
    def __init__(self,x,y,w,h,x1,x2): #x1 is the limit of the bullet. I dont want it to go endlessly  
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x1 = x1
        self.x2 = x2
        
        if g.rambo.dir == 1:
            self.vx = 7 
           
        elif g.rambo.dir == -1:
            self.vx = -7 
        
    def update(self):
        self.x += self.vx
        
        if self.x > self.x1:
            for i in g.bullets:
                g.bullets.remove(i)
        
        if self.x < self.x2:
            for i in g.bullets:
                g.bullets.remove(i)
        
    def display(self):
        self.update()
        
        noFill()
        stroke(255,0,0)
        rect(self.x,self.y,self.w,self.h)   
        
        for e in g.enemies1:
            if detectcollision(self.x- g.x,self.y,self.w,self.h,e.x,e.y,e.w,e.h):
                g.enemies1.remove(e)
                del e
                for i in g.bullets:
                    g.bullets.remove(i)
        
        print(self.x)
        for b in g.blocks:
            if detectcollision(self.x,self.y,self.w,self.h,b.x-g.x,b.y,b.w,b.h):
                g.blocks.remove(b)
                del b
                for i in g.bullets:
                    g.bullets.remove(i) 
                
        
class Game:
    def __init__ (self,w,h):
        self.w=w
        self.h=h
        self.x = 0
        self.frames = 0
        self.rambo = Rambo(100,100,98,130,"rambo.png",10) #Calling Rambo
        self.bgImgs = []
        for i in range(3,0,-1):
            self.bgImgs.append(loadImage(path+"/images/layer_0"+str(i)+".png"))
        
        #create enemies
        self.enemies1=[]
        for i in range(1):
            self.enemies1.append(Skeletons(300+i*100,50,236,246,300,900,"Zombie1.png",6))
        
        
        #create blocks
        self.blocks = []
        #base ground
        for i in range(10):
            self.blocks.append(Block(0+i*64,649,64,64))
        for i in range(17):
            self.blocks.append(Block(940+i*64,649,64,64))
        for i in range(5):
            self.blocks.append(Block(2328+i*64,649,64,64))
        for i in range(20):
            self.blocks.append(Block(2948+i*64,649,64,64))    
            
        # for i in range(10):
        #     self.blocks.append(Block(1200+i*64-self.x,585,64,64))
        # for i in range(7):
        #     self.blocks.append(Block(1264+i*64-self.x,521,64,64))
        # for i in range(6):
        #     self.blocks.append(Block(1264+i*64-self.x,457,64,64))
        # # for i in range(7):
        # #     self.blocks.append(Block(2000+i*64-self.x,457,64,64))
        
        #in the air blocks
        for i in range(10):
            self.blocks.append(Block(3500+i*64,393,64,10))
            
        
        self.bullets = []
                
    def update(self):
        for i in self.blocks:
            if detectcollision(self.rambo.x,self.rambo.y,self.rambo.w,self.rambo.h,i.x,i.y,i.w,i.h):
                self.rambo.y = i.y - self.rambo.h
                self.rambo.vy = 0
                
        for i in self.blocks:
            for r in self.enemies1:
                if detectcollision(r.x,r.y,r.w,r.h,i.x,i.y,i.w,i.h):
                    r.y = i.y - r.h
                    r.vy = 0                

    def display(self):
        self.frames += 1
        
        cnt = 3
        for img in self.bgImgs:
            # image(img,0-self.x,0)
            if cnt == 3:
                x = (self.x//2)%self.w
            elif cnt == 2:
                x = (self.x//3)%self.w
            elif cnt == 1:
                x = (self.x//2)%self.w
            else:
                x = (self.x)%self.w
            
            image (img,0,0,self.w-x,self.h,x,0,self.w,self.h)
            
            cnt -= 1
        g.rambo.display(self.blocks)
        self.update()
        for b in self.blocks:
            b.display()
            
        for i in self.enemies1:
            i.display()
            
        for b in self.bullets:
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
    elif keyCode == 32:
        g.rambo.keyHandler[32] = True
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
    elif keyCode == 32:
        g.rambo.keyHandler[32] = False

    
    
        
    
