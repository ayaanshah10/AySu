add_library('minim')

import os
path = os.getcwd()
player = Minim(this)

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
        self.kill = player.loadFile(path+"/sounds/shoot.mp3")
        self.explode = player.loadFile(path+"/sounds/blast.mp3")
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
        
        #colliding with enemy
        for i in g.enemies1:
            if detectcollision(self.x,self.y,self.w,self.h,i.x,i.y,i.w,i.h):
                g.__init__(1280,720)
        
        #don't let him jump from below a platform
        for b in g.blocks:
            if b.x <= self.x and self.x <= b.x + b.w:
                if b.y <= self.y:
                    if self.y <= b.y + b.h + 30 and self.y >= b.y + b.h :
                        self.vy = 7
                                                        
        if self.keyHandler[32] and self.blockBullet == 0 and self.dir == 1:
            self.blockBullet = 60
            g.bullets.append(Bullet(self.x+self.w-g.x,self.y+(self.h)/8,10,10,self.x+self.w-g.x+300,self.x+self.w-g.x-300))
            self.kill.rewind()
            self.kill.play()
        elif self.keyHandler[32] and self.blockBullet == 0 and self.dir == -1:
            self.blockBullet = 60
            g.bullets.append(Bullet(self.x+-g.x,self.y+(self.h)/8,10,10,self.x+self.w-g.x+300,self.x+self.w-g.x-300))
            self.kill.rewind()
            self.kill.play()
            
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
       self.vx = 1
       self.x1 = x1
       self.x2 = x2
       self.img = loadImage(path+"/images/Zombie1.png")
    
    def update(self):
        self.gravity()
        
        #make them smart
        if self.x - g.rambo.x <= 300 and self.x - g.rambo.x > 0 and g.rambo.y >= self.y and g.rambo.y <= self.y + self.h:
            self.vx = -3
            self.dir = 1
        
        if g.rambo.x-self.x <= 300 and g.rambo.x-self.x > 0 and g.rambo.y >= self.y and g.rambo.y <= self.y + self.h: 
            self.vx = 3
            self.dir = -1
            
        if self.x > self.x2 :
            self.vx = -1
            self.dir = 1
        elif self.x < self.x1:
            self.vx = 1
            self.dir = -1
        
        self.x += self.vx
        self.y += self.vy
            
    def display(self):
        self.update()
        
        if self.vx != 0:
            self.f = (self.f+0.05)%self.F
            
        if self.dir > 0:
            stroke(255,0,0)
            rect(self.x-g.x,self.y,self.w,self.h)
            image(self.img,self.x-g.x,self.y,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        elif self.dir < 0:
            stroke(255,0,0)
            rect(self.x-g.x,self.y,self.w,self.h)
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
        self.img = loadImage(path+"/images/bullet.png")
        self.hit = player.loadFile(path+"/sounds/zombiehit.mp3")
        self.whit = player.loadFile(path+"/sounds/hit.mp3")
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
        #rect(self.x,self.y,self.w,self.h)   
        image(self.img,self.x,self.y,self.w,self.h)        
        for e in g.enemies1:
            if detectcollision(self.x,self.y,self.w,self.h,e.x-g.x,e.y,e.w,e.h):
                self.hit.rewind()
                self.hit.play()
                g.enemies1.remove(e)
                del e
                for i in g.bullets:
                    g.bullets.remove(i)
        
        for b in g.blocks:
            if detectcollision(self.x,self.y,self.w,self.h,b.x-g.x,b.y,b.w,b.h):
                self.whit.rewind()
                self.whit.play()
                g.blocks.remove(b)
                del b
                for i in g.bullets:
                    g.bullets.remove(i)
                    
           
class Bomb:
    def __init__(self,x,y,w,h,b):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.b = b
    
    def triggered(self):
        delenemies = [] 
        for i in g.enemies1:
            if (self.x - i.x <= self.b and self.x - i.x >= 0) or (i.x - (self.x + self.w) <= self.b and i.x - self.x >= 0):
                if (self.y - i.y <= self.b and self.y - i.y >= 0) or (i.y - (self.y + self.h) <= self.b and i.y - (self.y + self.h) >= 0):
                    delenemies.append(i)
        
        newenemies = []
        for i in g.enemies1:
            if i not in delenemies:
                newenemies.append(i)
        
            g.enemies1 = newenemies
                
        delblocks = []            
        for i in g.blocks:
            if (self.x - i.x <= self.b and self.x - i.x >= 0) or (i.x - (self.x + self.w) <= self.b and i.x - self.x >= 0):
                if (self.y - i.y <= self.b and self.y - i.y >= 0) or (i.y - (self.y + self.h) <= self.b and i.y - (self.y + self.h) >= 0):
                    delblocks.append(i)
        
        newblocks = []
        for i in g.blocks:
            if i not in delblocks:
                newblocks.append(i)
                                        
        g.blocks = newblocks
    
                        
        #kills Rambo
        
        # if (self.x - g.rambo.x <= self.b and self.x - g.rambo.x >= 0) or (g.rambo.x - (self.x + self.w) <= self.b and g.rambo.x - self.x >= 0):
        #         if (self.y - g.rambo.y <= self.b and self.y - g.rambo.y >= 0) or (g.rambo.y - (self.y + self.h) <= self.b and g.rambo.y - (self.y + self.h) >= 0):
        #             if self.active:
        #                  g.__init__(1280,720)
                
                                
class Shootbomb(Bomb):
    def __init__(self,x,y,w,h,b):
        Bomb.__init__(self,x,y,w,h,b)
        self.active = True
        self.active = True
        self.timer = 999999
        self.finished2 = False
        self.explode = player.loadFile(path+"/sounds/blast.mp3")

    def triggerbomb(self):
        for i in g.bullets:
            if detectcollision(i.x,i.y,i.w,i.h,self.x-g.x,self.y,self.w,self.h):
                self.triggered()
                self.explode.rewind()
                self.explode.play()
                self.active = False
                self.timer = millis()    
        
        for bomb in g.bulletbombs:
            if not bomb.active:
                g.bulletbombs.remove(bomb)
                del bomb
    
    def display(self):
        self.triggerbomb()
        
        if not self.active:
            print(millis()-self.timer, self.finished2)
            if millis()-self.timer < 2000:
                image(loadImage(path+"/images/bombexplosion.png"),self.x-g.x-80,self.y-70,250,250)
                
            else: 
                self.finished2 = True
                
        if self.finished2:
            print("done")
            g.bulletbombs.remove(self)
        
        stroke(0,255,0)
        rect(self.x-g.x,self.y,self.w,self.h)
        image(loadImage(path+"/images/bombcrate.png"),self.x-g.x,self.y,self.w,self.h)
        
class Triggerbomb(Bomb):
    def __init__(self,x,y,w,h,b,x1,y1):
        Bomb.__init__(self,x,y,w,h,b)
        self.x1 = x1
        self.y1 = y1
        self.active = True
        self.timer = 999999
        self.finished = False
        self.explode = player.loadFile(path+"/sounds/blast.mp3")

    
    def triggerbomb(self):
        if (self.x - g.rambo.x <= self.x1 and self.x - g.rambo.x >= 0) or (g.rambo.x - (self.x + self.w) <= self.x1 and g.rambo.x - (self.x + self.w) >= 0):
            if (self.y - g.rambo.y <= self.y1 and self.y - g.rambo.y >= 0) or (g.rambo.y - (self.y + self.h) <= self.y1 and g.rambo.y - (self.y + self.h) >= 0):
                self.triggered()
                self.explode.rewind()
                self.explode.play()
                self.active = False
                self.timer = millis()        
                    
    def display(self):
        self.triggerbomb()
        
        if not self.active:
            print(millis()-self.timer, self.finished)
            if millis()-self.timer < 1000:
                image(loadImage(path+"/images/bombexplosion.png"),self.x-g.x-80,self.y-70,250,250)
                
            else: 
                self.finished = True
                
        if self.finished:
            print("done")
            g.triggerbombs.remove(self)
            # del self
        
        stroke(255,0,0)
        rect(self.x-g.x,self.y,self.w,self.h)
        image(loadImage(path+"/images/Triggerbomb.png"),self.x-g.x,self.y,self.w,self.h)

class Spikes:
    def __init__ (self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vy = 0
        
    def gravity(self):
        self.vy += 0.5
    
    def update(self):
        if g.rambo.x >= self.x - 200 and g.rambo.x <= self.x + self.w:
            self.gravity()
    
        self.y += self.vy
        
        if detectcollision(self.x,self.y,self.h,self.w,g.rambo.x,g.rambo.y,g.rambo.w,g.rambo.h):
            print('yeah')
            g.__init__(1280,720)
    
    def display(self):
        self.update()
        stroke(0,0,255)    
        #rect(self.x,self.y,self.w,self.h) 
        image(loadImage(path+"/images/spikes.png"),self.x-g.x,self.y,self.w,self.h)           

class Winobject:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def update(self):
        if detectcollision(g.rambo.x,g.rambo.y,g.rambo.w,g.rambo.h,self.x,self.y,self.w,self.h):
            print('You won')
            g.state = "win"
            
    def display(self):
        self.update()
        stroke(255,0,0)
        rect(self.x - g.x, self.y, self.w, self.h)
        image(loadImage(path+"/images/helicopter.png"),self.x - g.x, self.y, self.w, self.h)
class Game:
    def __init__ (self,w,h):
        self.w=w
        self.h=h
        self.x = 0
        self.frames = 0
        self.rambo = Rambo(100,100,98,130,"rambo.png",10) #Calling Rambo
        self.music = player.loadFile(path+"/sounds/gameplay.mp3")
        self.music.rewind()
        self.music.play()
        self.bgImgs = []
        self.state = "play" 
        for i in range(3,0,-1):
            self.bgImgs.append(loadImage(path+"/images/layer_0"+str(i)+".png"))
        self.blockEnemy = 0
        self.count = 0
        
        self.winner = Winobject(9028,250,640,320)
        
        #create enemies
        self.enemies1=[]
        for i in range(4):
            self.enemies1.append(Skeletons(1000+(i**2)*100,50,149,246,1000,2000,"Zombie1.png",5))
    
        self.enemies1.append(Skeletons(2584,50,149,246,2392,2584,"Zombie1.png",5))
        
        for i in range(2):
            self.enemies1.append(Skeletons(4484+(i**2)*100,276,149,246,4484,4996,"Zombie1.png",5))
         
        for i in range(2):
            self.enemies1.append(Skeletons(5956+(i**2)*100,276,149,246,5828,6596,"Zombie1.png",5))
            
        for i in range(2):
            self.enemies1.append(Skeletons(6020+(i**2)*100,403,149,246,5828,6596,"Zombie1.png",5))
        
        self.enemies1.append(Skeletons(7044,211,149,246,7044,7172,"Zombie1.png",5))
                    
        #create blocks
        self.blocks = []
        #base ground
        for i in range(10):
            self.blocks.append(Block(i*64,649,64,64))
        for i in range(17):
            self.blocks.append(Block(940+i*64,649,64,64))
        for i in range(5):
            self.blocks.append(Block(2328+i*64,649,64,64))
        for i in range(20):
            self.blocks.append(Block(2948+i*64,649,64,64))
        for i in range(55):
            self.blocks.append(Block(5252+i*64,649,64,64))
            
            
                
        #building    
        for i in range(4):
            self.blocks.append(Block(2392+i*64-self.x,585,64,64))
        for i in range(4):
            self.blocks.append(Block(2392+i*64-self.x,521,64,64))
        
        
        for i in range(4):
            self.blocks.append(Block(7044+i*64-self.x,585,64,64))
        for i in range(4):
            self.blocks.append(Block(7044+i*64-self.x,521,64,64))
        for i in range(3):
            self.blocks.append(Block(7044+i*64-self.x,457,64,64))
        
        
         #in the air blocks
        for i in range(10):
            self.blocks.append(Block(3500+i*64,393,64,64))
        
        for i in range(8):
            self.blocks.append(Block(4420+i*64,201,64,64))
            
        for i in range(7):
            self.blocks.append(Block(5124+i*64,201,64,64))
            
        for i in range(13):
            self.blocks.append(Block(4356+i*64,521,64,64))
            
        for i in range(15):
            self.blocks.append(Block(5828+i*64,329,64,64))
        
        for i in range(2):
            self.blocks.append(Block(4996+i*64,201,64,64))
            
        for i in range(4):
            self.blocks.append(Block(6916+i*64,105,64,64))
            
        for i in range(4):
            self.blocks.append(Block(8772+i*64,201,64,64))
                
        # vertical blocks
        for i in range(2):
            self.blocks.append(Block(5124,457+(-i)*64,64,64))
            
        for i in range(7):
            self.blocks.append(Block(8772,649+(-i)*64,64,64))
            
        
        
        self.triggerbombs = []
        # triggerbombs
        self.triggerbombs.append(Triggerbomb(3820,585,64,64,128,128,128))
        
        self.triggerbombs.append(Triggerbomb(4740,457,64,64,128,128,128))
        
        self.triggerbombs.append(Triggerbomb(7108,41,64,64,128,128,128))
        
        self.bulletbombs = []
        #bullet bombs
        self.bulletbombs.append(Shootbomb(4484,73,128,128,128))
        
        self.bulletbombs.append(Shootbomb(6020,201,128,128,128))
        
        #spikes
        self.spikes = []
        for s in range(5):
            self.spikes.append(Spikes(5956+(2*s)*64,393,64,64)) 
            
        for s in range(2):
            self.spikes.append(Spikes(5316+(2*s)*64,265,64,64)) 
            
        for s in range(2):
            self.spikes.append(Spikes(6916+(2*s)*64,169,64,64))
            
                
                            
        self.bullets = []
                
    def update(self):
        
        #enemies from doors
        self.count += 1
        if self.count%300 == 0:
            self.enemies1.append(Skeletons(3500,50,149,246,3100,3900,"Zombie1.png",5))
            
        if self.count%450 == 0:
            self.enemies1.append(Skeletons(5956,84,149,246,5828,6788,"Zombie1.png",5))
            
        if self.count%700 == 0:
            self.enemies1.append(Skeletons(7684,403,149,246,7044,8324,"Zombie1.png",5))
        
        if self.count%700 == 0:
            self.enemies1.append(Skeletons(8004,403,149,246,7684,8772,"Zombie1.png",5))
        
                        
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
        
        if self.state == "play":
        
            self.frames += 1
            
            # for i in self.bombs:
            #     if i.active == False:
            #         image(loadImage(path+"/images/bombexplosion.png"),self.x-g.x,self.y,self.w,self.h)
            
            cnt = 3
            for img in self.bgImgs:
                # image(img,0-self.x,0)
                if cnt == 3:
                    x = (self.x//3)%self.w
                elif cnt == 2:
                    x = (self.x//2)%self.w
                elif cnt == 1:
                    x = (self.x//2)%self.w
                else:
                    x = (self.x)%self.w
                
                image (img,0,0,self.w-x,self.h,x,0,self.w,self.h)
                image (img,self.w-x,0,x,self.h,0,0,x,self.h)
                cnt -= 1
            
            image(loadImage(path+"/images/door.png"),3500-g.x,200,250,250)
            g.rambo.display(self.blocks)
            self.update()
            for b in self.blocks:
                b.display()
                
            for i in self.enemies1:
                i.display()
                
            for b in self.bullets:
                b.display()
            
            for b in self.bulletbombs:
                b.display()
                
            for b in self.triggerbombs:
                b.display()
            
            for s in self.spikes:
                s.display()
            
            self.winner.display()
            # for bomb in self.bombs:
            #     if not bomb.active:
            #         print("inactive")
            #         if millis() - bomb.timer<500:
                        
            #             image(loadImage(path+"/images/bombexplosion.png"),bomb.x-self.x,bomb.y,bomb.w,bomb.h)
            #         else:
            #             self.bombs.remove(bomb)
            #             del bomb
            
        else:
            background(255)
            #rect(100, 100, 100, 100)
            image(loadImage(path+"/images/win.png"),100,100, 958, 826)
            
        
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

    
    
        
    
