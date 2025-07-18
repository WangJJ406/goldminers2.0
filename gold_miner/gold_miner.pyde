add_library('minim')
import os
import random
import math

RESOLUTION_W = 995
RESOLUTION_H = 722
player = Minim(this)
PATH = os.getcwd()
global bombImg
# def setup():
#     size(RESOLUTION_W, RESOLUTION_H)
def setup():
    global game,gameEnd,winPlayer,hookSpd,loopState,timer
    size(RESOLUTION_W, RESOLUTION_H)
    bombImg = loadImage(PATH + "/images/bomb.png")
    gameEnd= False
    loopState=True
    winPlayer=0
    hookSpd=2.5
    timer=millis()/1000+60
def mouseClicked():
    if not loopState:
        game.reset();
def draw():
    global gameEnd,loopState
    if loopState:
        #end of game display
        if gameEnd:
            # background(255)
            fill(0,100)
            noStroke()
            rectMode(CENTER)
            rect(width/2,height/2,450,240,20)
            fill(255)
            textSize(50)
            textAlign(CENTER,CENTER)
            if winPlayer>-1:
                text("player"+str(winPlayer)+" win!",width/2,height/2)
            else :
                text("Game tie",width/2,height/2)
            loopState=False
        elif not gameEnd:
            noStroke()
            game.display()
            game.update()
    
class Game:
    def __init__(self):
        self.backgroundImg = loadImage(PATH + "/images/background2.png")
        self.bombImg = loadImage(PATH + "/images/bomb.png")
        self.goldSmallImg = loadImage(PATH + "/images/gold_small.png")
        self.goldMidImg = loadImage(PATH + "/images/gold_mid.png")
        self.goldBigImg = loadImage(PATH + "/images/gold_big.png")
        self.stoneImg1 = loadImage(PATH + "/images/stone1.png")
        self.stoneImg2 = loadImage(PATH + "/images/stone2.png")
        self.minerImg1 = loadImage(PATH + "/images/miner.png")
        self.minerImg2 = loadImage(PATH + "/images/miner2.png")
        self.hookImg = loadImage(PATH + "/images/hook.png")
        self.golds = []
        self.stones = []
        self.miner1 = Miner(450, 38, 0.5, self.minerImg1)
        self.miner2 = Miner(450, 613, 0.5, self.minerImg2)
        self.hook1 = Hook(500, 76, self.miner1, 1)
        self.hook2 = Hook(500, 640, self.miner2, -1)
        self.rope1 = Rope(500, 76, self.miner1)
        self.rope2 = Rope(500, 640, self.miner2)
        self.bomb1 = Bomb(0, 0, "spare", self.rope1)
        self.bomb2 = Bomb(0, 0, "spare", self.rope2)
        self.generateGolds()
        self.generateStones()
        self.frameCount = 0
        self.score1 = 0  
        self.score2 = 0 
        # self.bomb_sound = player.loadFile(PATH + "/sounds/bomb.mp3")
        self.bg_sound = player.loadFile(PATH + "/sounds/background.mp3")
        self.bg_sound.loop()

    def reset(self):
        global gameEnd,loopState,timer
        timer=millis()/1000+60
        self.golds = []
        self.stones = []
        self.miner1 = Miner(450, 38, 0.5, self.minerImg1)
        self.miner2 = Miner(450, 613, 0.5, self.minerImg2)
        self.hook1 = Hook(500, 76, self.miner1, 1)
        self.hook2 = Hook(500, 640, self.miner2, -1)
        self.rope1 = Rope(500, 76, self.miner1)
        self.rope2 = Rope(500, 640, self.miner2)
        self.bomb1 = Bomb(0, 0, "spare", self.rope1)
        self.bomb2 = Bomb(0, 0, "spare", self.rope2)
        self.generateGolds()
        self.generateStones()
        self.frameCount = 0
        self.score1 = 0  
        self.score2 = 0 
        gameEnd= False
        loopState=True
    def update(self):
        global gameEnd,winPlayer
        self.frameCount += 1
        self.hook1.update(self.frameCount * self.hook1.rotation_speed / 1.5, self.bomb1.state)
        self.hook2.update(self.frameCount * self.hook2.rotation_speed / 1.5, self.bomb1.state)
        self.rope1.update(self.hook1.x, self.hook1.y)
        self.rope2.update(self.hook2.x, self.hook2.y)
        self.update_hook_and_rope()
        self.miner1.move()
        self.miner2.move()
        self.bomb1.move_with_rope(self.hook1.x, self.hook1.y)
        self.bomb2.move_with_rope(self.hook2.x, self.hook2.y)
        
        #end of game display
        if  dist(self.hook1.x, self.hook1.y,self.miner2.x+50,self.miner2.y+50)<66:
            gameEnd=True
            winPlayer=1
        if  dist(self.hook2.x, self.hook2.y,self.miner1.x+50,self.miner1.y+50)<66:

            gameEnd=True
            winPlayer=2
        # Check if bomb1 is placed and if it's close enough to hook2
        if  self.bomb1.state=="placed" and dist(self.hook2.x, self.hook2.y,self.bomb1.x,self.bomb1.y)<47:
            # self.bomb_sound.play()
            gameEnd=True
            winPlayer=1
        # Check if bomb2 is placed and if it's close enough to hook1
        if  self.bomb2.state=="placed" and dist(self.hook1.x, self.hook1.y,self.bomb2.x,self.bomb2.y)<47:
            # self.bomb_sound.play()
            gameEnd=True
            winPlayer=2
        
        # Check if the time limit of the game is reached
        if timer-millis()/1000 <=0:
            gameEnd=True
            # Determine the winning player based on scores
            if self.score1>self.score2:
                winPlayer=1
            elif self.score1<self.score2:
                winPlayer=2
            else:
                winPlayer=-1


    def update_hook_and_rope(self):
    # Update hook and rope 1
        if self.hook1.hook_state == 'down':
            # If hook1 is down, extend its length
            self.hook1.length += hookSpd
            # Check if hook1 is out of bounds, if so, retract it
            if self.hook1.length > 600 or self.hook1.x > 985 or self.hook1.x < 10 or self.hook1.y > 600:
                self.hook1.hook_state = 'retract'
        elif self.hook1.hook_state == 'retract' or self.hook1.hook_state == 'retract_after_place':  
            if not self.hook1.hooked_item:
                # If hook1 is not hooked, retract it
                self.hook1.length -= hookSpd
            else:
                # If hook1 is hooked, retract it with the speed of the hooked item
                self.hook1.length -= self.hook1.hooked_item.spd
            if self.hook1.length <= 100:
                # If hook1 retracts to its minimum length, set its state to spare
                self.hook1.hook_state = 'spare'
                # If bomb1 is in placing state, set it to placed and prepare hook1 for retraction after placing
                if self.bomb1.state == "placing":
                    self.bomb1.state = "placed"
                    self.hook1.hook_state = 'retract_after_place'
                if self.hook1.hooked_item:
                    # If hook1 is hooked to an item, end the item's action and unhook it
                    self.hook1.hooked_item.end = True
                    self.hook1.hooked_item = None
        elif self.bomb1.state == "placing":
            # If bomb1 is in placing state, set hook1 to retract
            self.hook1.hook_state = 'retract'
            
        # update hook and rope 2 
        print(self.hook2.hook_state,self.bomb2.state)
        if self.hook2.hook_state == 'down':
            self.hook2.length += hookSpd
            if self.hook2.length > 600 or self.hook2.x > 985 or self.hook2.x < 10 or self.hook2.y > 600:
                self.hook2.hook_state = 'retract'
        elif self.hook2.hook_state == 'retract'or self.hook2.hook_state == 'retract_after_place':  
            if  not self.hook2.hooked_item:
                self.hook2.length -= hookSpd
            else :
                self.hook2.length -=self.hook2.hooked_item.spd        
            if self.hook2.length <= 100:
                self.hook2.hook_state = 'spare'
                if self.bomb2.state == "placing":
                    self.bomb2.state = "placed"
                    self.hook2.hook_state = 'retract_after_place' 
                if self.hook2.hooked_item:
                    self.hook2.hooked_item.end=True
                    self.hook2.hooked_item = None
                    
        elif self.bomb2.state == "placing":
            self.hook2.hook_state = 'retract'                          

    def generateGolds(self):
    # Generate gold
        while len(self.golds) < 8:
            # Randomize
            size = random.randint(1, 3)
            x = random.randint(50, RESOLUTION_W - 100)
            y = random.randint(150, RESOLUTION_H - 200)
            # Create a new gold item
            new_gold = Item(x, y, size, "gold")
            # Check if the new gold item overlaps with existing items (gold or stones)
            if not new_gold.is_overlapping(self.golds + self.stones, 50):
                # Add the new gold item to the list of gold items
                self.golds.append(new_gold)

    def generateStones(self):
        # Generate stone
        while len(self.stones) < 5:
            # Randomize
            type = random.randint(1, 2)
            x = random.randint(10, RESOLUTION_W - 10)
            y = random.randint(150, RESOLUTION_H - 200)
            # Create a new stone item
            new_stone = Item(x, y, type, "stone")
            # Check if the new stone item overlaps with existing items (gold or stones)
            if not new_stone.is_overlapping(self.golds + self.stones, 50):
                # Add the new stone item to the list of stone items
                self.stones.append(new_stone)
    
    def display(self):
        # Display the game elements on the screen
        image(self.backgroundImg, 0, 0)  
        self.hook1.display()
        self.hook2.display()
        self.rope1.display()
        self.rope2.display()
        for gold in self.golds:
            if not gold.end:
                gold.display()
        for stone in self.stones:
            if not stone.end:
                stone.display()
        self.miner1.display()
        self.miner2.display()
        self.bomb1.display()
        self.bomb2.display()
        # Display the remaining time and scores
        textSize(35)
        fill(0)
        textAlign(LEFT)
        text(str(timer - millis() / 1000) + "s", 50, 75)
        self.display_score()
    
    def display_score(self):
        # Display the scores of Player 1 and Player 2
        fill(255)
        textAlign(RIGHT)
        textSize(20)
        text("Player1: " + str(self.score1), 950, 63)
    
    def generateGolds(self):
    # Generate gold
        while len(self.golds) < 8:
            # Randomize
            size = random.randint(1, 3)
            x = random.randint(50, RESOLUTION_W - 100)
            y = random.randint(150, RESOLUTION_H - 200)
            # Create a new gold item
            new_gold = Item(x, y, size, "gold")
            # Check if the new gold item overlaps with existing items (gold or stones)
            if not new_gold.is_overlapping(self.golds + self.stones, 50):
                # Add the new gold item to the list of gold items
                self.golds.append(new_gold)

    def generateStones(self):
        # Generate stone
        while len(self.stones) < 5:
            # Randomize
            type = random.randint(1, 2)
            x = random.randint(10, RESOLUTION_W - 10)
            y = random.randint(150, RESOLUTION_H - 200)
            # Create a new stone item
            new_stone = Item(x, y, type, "stone")
            # Check if the new stone item overlaps with existing items (gold or stones)
            if not new_stone.is_overlapping(self.golds + self.stones, 50):
                # Add the new stone item to the list of stone items
                self.stones.append(new_stone)
    
    def display(self):
        # Display the game elements on the screen
        image(self.backgroundImg, 0, 0)  
        self.hook1.display()
        self.hook2.display()
        self.rope1.display()
        self.rope2.display()
        for gold in self.golds:
            if not gold.end:
                gold.display()
        for stone in self.stones:
            if not stone.end:
                stone.display()
        self.miner1.display()
        self.miner2.display()
        self.bomb1.display()
        self.bomb2.display()
        # Display the remaining time and scores
        textSize(35)
        fill(0)
        textAlign(LEFT)
        text(str(timer - millis() / 1000) + "s", 50, 75)
        self.display_score()
    
    def display_score(self):
        # Display the scores of Player 1 and Player 2
        fill(255)
        textAlign(RIGHT)
        textSize(20)
        text("Player1: " + str(self.score1), 950, 63)
        text("Player2: " + str(self.score2), 150, 676)
        
class Miner:
    def __init__(self, x, y, scale, img):
        # Initialize 
        self.x = x
        self.y = y
        self.scale = scale
        self.speed = 1
        self.min_x = 300
        self.max_x = 600
        self.img = img

    def move(self):
        # Move the miner back and forth within defined boundaries
        if self.x <= self.min_x or self.x >= self.max_x:
            self.speed *= -1
        self.x += self.speed

    def display(self):
        # Display image
        imgWidth = self.img.width * self.scale
        imgHeight = self.img.height * self.scale
        image(self.img, self.x, self.y, imgWidth, imgHeight)

class Bomb:
    def __init__(self, x, y, state, rope):
        self.x = x
        self.y = y
        self.state = state
        self.rope = rope

    def display(self):
        if self.state != "spare":
            noStroke()
            if millis()%1000<500:
                fill(255,0,0)
                ellipse(self.x, self.y,50,50)
            image(game.bombImg, self.x- game.bombImg.width / 4, self.y- game.bombImg.height / 4, game.bombImg.width / 2, game.bombImg.height / 2)
    def move_with_rope(self, x, y):
        if self.state == "placing":
            self.x = x
            self.y = y
        elif self.state == "placed":
            pass

class Item:
    def __init__(self, x, y, size, itemType):
        # Initialize
        self.x = x
        self.y = y
        self.size = size
        self.itemType = itemType
        self.hooked = False
        self.end = False
        self.spd = 2
        if itemType == "gold":
            if self.size == 1:
                self.spd = 2
            elif self.size == 2:
                self.spd = 1.4
            else:
                self.spd = 0.9
        else:
            self.spd = 0.6

    def is_overlapping(self, others, padding=10):
        # Check if the item is overlapping with other items
        for other in others:
            if abs(self.x - other.x) < padding and abs(self.y - other.y) < padding:
                return True
        return False

    def display(self):
        # Display the item based on its type and size
        if self.itemType == "gold":
            if self.size == 1:
                image(game.goldSmallImg, self.x - game.goldSmallImg.width / 2, self.y - game.goldSmallImg.height / 2)
            elif self.size == 2:
                image(game.goldMidImg, self.x - game.goldMidImg.width / 2, self.y - game.goldMidImg.height / 2)
            else:
                image(game.goldBigImg, self.x - game.goldBigImg.width / 2, self.y - game.goldBigImg.height / 2)
        elif self.itemType == "stone":
            if self.size == 1:
                image(game.stoneImg1, self.x - game.stoneImg1.width / 2, self.y - game.stoneImg1.height / 2)
            else:
                image(game.stoneImg2, self.x - game.stoneImg2.width / 2, self.y - game.stoneImg2.height / 2)

    def hook(self, hook_x, hook_y):
        # Hook the item at the specified coordinates
        self.hooked = True
        self.hook_x = hook_x
        self.hook_y = hook_y

    def release(self):
        # Release the item from being hooked
        self.hooked = False
        self.hook_x = 0
        self.hook_y = 0

    def update_position(self, x, y):
        # Update the position of the item
        self.hook_x = x
        self.hook_y = y

class Rope:
    def __init__(self, anchor_x, anchor_y, miner):
        # Initialize the rope with anchor coordinates and associated miner
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.end_x = anchor_x
        self.end_y = anchor_y
        self.miner = miner
        self.state = "normal"

    def display(self):
        # Display the rope as a line from the miner to the anchor point
        stroke(0)
        strokeWeight(2)
        line(self.miner.x + 20, self.anchor_y, self.end_x, self.end_y)

    def update(self, hook_x, hook_y):
        # Update the end point of the rope to the hook's position
        self.end_x = hook_x
        self.end_y = hook_y


class Hook:
    def __init__(self, x, y, miner, direction):
        # Initialize the hook with initial properties
        self.x = x
        self.y = y
        self.length = 100
        self.base_angle = 90
        self.swing_speed = 0.05
        self.max_swing = 45
        self.rotation_speed = 0.75
        self.orbital_angle = self.base_angle
        self.rotational_angle = 0
        self.min_rotational_angle = -45
        self.max_rotational_angle = 45
        self.rotation_direction = 1
        self.speed = {'x': 0, 'y': 0}
        self.hook_state = "spare"
        self.miner = miner
        self.direction = direction
        self.catch = False
        self.hooked_item = None 
        
    def update(self, frameCount, bombState):
        # Update the hook's position and behavior
        if self.hook_state != "down" and self.hook_state != "retract" and self.hook_state != "retract_after_place":
            swing = self.max_swing * math.sin(frameCount * self.swing_speed)
            new_angle = self.base_angle + swing
            self.orbital_angle = max(min(new_angle, self.base_angle + self.max_swing), self.base_angle - self.max_swing)
            
            self.rotational_angle += self.rotation_speed * self.rotation_direction
            if self.rotational_angle > self.max_rotational_angle or self.rotational_angle < self.min_rotational_angle:
                self.rotation_direction *= -1

        self.x = self.miner.x + (self.length * math.cos(math.radians(self.orbital_angle)))
        self.y = self.miner.y + (self.length * math.sin(math.radians(self.orbital_angle)) * self.direction)
        if (self.direction == 1 and self.y >= 640) or (self.direction == -1 and self.y <= 76):
            self.hook_state = 'retract'

        if not self.hooked_item and self.hook_state == "down" and not bombState == "placing":
            self.check_collision()
       
        if self.hooked_item:
            self.hooked_item.x = self.x
            self.hooked_item.y = self.y

    def check_collision(self):
        # Check collision with gold and stone items
        collided = False
        for gold in game.golds:
            if not gold.end:
                # Check collision with gold
                if gold.size == 1:
                    goldWid = game.goldSmallImg.width 
                elif gold.size == 2:
                    goldWid = game.goldMidImg.width
                elif gold.size == 3:
                    goldWid = game.goldBigImg.width 
                if abs(self.x - gold.x) < goldWid / 2 and abs(self.y - gold.y) < goldWid / 2:
                    if not collided:  
                        collided = True
                        self.hook_state = 'retract'
                        if self.direction == 1:
                            game.score1 += 200 if gold.size == 1 else 400 if gold.size == 2 else 600
                        else:
                            game.score2 += 200 if gold.size == 1 else 400 if gold.size == 2 else 600
                        self.hooked_item = gold  
                        break

        for stone in game.stones:
            if not stone.end:
                # Check collision with stone
                if abs(self.x - stone.x) < game.stoneImg1.width / 2 and abs(self.y - stone.y) < game.stoneImg1.height / 2:
                    if not collided:  
                        collided = True
                        self.hook_state = 'retract'
                        self.hooked_item = stone  
                        break

    def display(self):
        # Display the hook with appropriate rotation and scaling
        pushMatrix()
        translate(self.x, self.y)
        if self.direction == -1:  
            scale(1, -1)
        rotate(math.radians(self.rotational_angle))
        image(game.hookImg, -game.hookImg.width / 2, -game.hookImg.height / 2)
        popMatrix()

def keyPressed():
    if keyCode == DOWN and game.hook1.hook_state == 'spare':
        game.hook1.hook_state = 'down'

    if keyCode == LEFT :
        if game.bomb1.state == "spare"  and not game.hook1.hooked_item:
            game.bomb1.state = "placing"

    if keyCode == RIGHT:
        if game.bomb1.state == "placing":
            game.bomb1.state = "placed"
            game.hook1.hook_state = "retract"

    if keyCode == 87 and game.hook2.hook_state == 'spare':  # W
        game.hook2.hook_state = 'down'

    if keyCode == 65  and not game.hook2.hooked_item:  # A
        if game.bomb2.state == "spare":
            game.bomb2.state = "placing"

    if keyCode == 68:  # D
        if game.bomb2.state == "placing":
            game.bomb2.state = "placed"
            game.hook2.hook_state = "retract"


game = Game() 
