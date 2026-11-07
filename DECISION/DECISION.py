#import libraries
import pygame
import random

#initialse pygame and set frame rate
pygame.init()
done = False
clock = pygame.time.Clock()
jumping = False

# -- colours ---------------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

#set variables
gravity = 1.5
jump_height = 15.75
score = 6
#m2 = "locked"
#jm3 = "locked"


#set text size and font
font = pygame.font.Font(None, 30)

# -- screen -----------------------------------------------------------------
WIDTH = 640
HEIGHT = 640
#set the size of the screen
size = (WIDTH, HEIGHT)
#apply size to screen
screen = pygame.display.set_mode(size)
#file name
pygame.display.set_caption("DECISION")

#set teleport collisions
teleport_id = random.randint(1, 2)
teleport_id2 = random.randint(1, 2)
teleport_id3 = random.randint(1, 4)

# -- images -----------------------------------------------------------------
#title screen background
Decision = pygame.image.load("title_screen.jpg")

#play button image
play = pygame.image.load("play_button.jpg")

#home button image
house = pygame.image.load("house.jpg")
house.set_colorkey(BLUE)

#character images
character_standing = pygame.image.load("character_standing.png")
character_left = pygame.image.load("character_left.png")
character_right = pygame.image.load("character_right.png")
character_jump_left = pygame.image.load("character_jump_left.png")
character_jump_right = pygame.image.load("character_jump_right.png")

#menue block image
menu_block = pygame.image.load("menublock.jpg")

#map button images
map1 = pygame.image.load("Map1button.jpg")
map2 = pygame.image.load("Map2button.jpg")
map3 = pygame.image.load("Map3button.jpg")

#map block button images
block1 = pygame.image.load("brownblock.jpg")

block2 = pygame.image.load("blueblock.jpg")

block3 = pygame.image.load("purpleblock.jpg")

#coin image
coin_image = pygame.image.load("coin.jpg")
coin_image.set_colorkey(GREEN)
coin_image = pygame.transform.scale(coin_image, (28, 28)).convert()

#killzone image
killzone_image = pygame.image.load("killzone.png")

#teleport image
teleport_image = pygame.image.load("teleport.png")

#menu background image
menubg = pygame.image.load("menubg.jpg")
menubg = pygame.transform.scale(menubg, (WIDTH, HEIGHT)).convert()

#map background images
bg1 = pygame.image.load("bg1.jpg")
bg1 = pygame.transform.scale(bg1, (WIDTH, HEIGHT)).convert()

bg2 = pygame.image.load("bg2.jpg")
bg2 = pygame.transform.scale(bg2, (WIDTH, HEIGHT)).convert()

bg3 = pygame.image.load("bg3.jpg")
bg3 = pygame.transform.scale(bg3, (WIDTH, HEIGHT)).convert()

# -- objects ----------------------------------------------------------------
class Player(object):

    def __init__(self):
        #attributes
        self.image = character_standing #set character image
        self.rect = self.image.get_rect() #create character box
        self.rect.center = (320, 602) #set character center on first map
        self.on_ground = False #variable to check if character is on the grouund
        self.y_speed = 0 #sets vertical speed to 0
        self.active = True #allows character to appear  on screen

    #move method
    def move(self, x_speed, y_speed):
        global score, current_level   # Declare score and current level as global to modify it
        #allows character to move according to its verticle and horizontal speed
        self.rect.x += x_speed 
        self.rect.y += y_speed
        self.on_ground = False

        #wall collision
        for wall in wall_group:
            #checks for collision with wall
            if self.rect.colliderect(wall.rect):
                #checks direction of movement by comparing the horizontal and vertical speed with 0
                if x_speed > 0: 
                    self.rect.right = wall.rect.left #aligns the right side of the character with the box left side of the wall box
                if x_speed < 0:
                    self.rect.left = wall.rect.right #aligns the left side of the character with the box right side of the wall box
                if y_speed > 0:
                    self.rect.bottom = wall.rect.top #aligns the bottom side of the character with the box top side of the wall box
                    self.on_ground = True
                    self.y_speed = 0
                if y_speed < 0:
                    self.rect.top = wall.rect.bottom #aligns the top side of the character with the box bottom side of the wall box

        #coin collision
        for coin in coin_group:
            #checks for collision with coin
            if self.rect.colliderect(coin.rect):
                score += 1 #adds one to the score
                coin_group.remove(coin) #removes coin from screen

        #killzone collision
        for killzone in killzone_group:
            #checks for collision with killzone
            if self.rect.colliderect(killzone.rect):
                #ckecks which map is being displayed and changes the position of the character according to the map
                if current_level == "Map2":
                    self.rect.center = (38, 602)
                elif current_level == "Map3":
                    self.rect.center = (376, 602)
            
        #teleport collision
        for teleport1 in teleport1_group:
            #checks for collision with teleport
            if self.rect.colliderect(teleport1.rect):

                if current_level == "Map1" and score >= 6: #checks which map is being displayed and what the score is
                    if teleport_id == 1: #checks which teleport the character is colliding with
                        right = font.render("That's correct!", True, WHITE) # sets the text for the correct teleport
                        screen.blit(right, (250, 320)) #blits the text on the screen
                        pygame.display.flip() #updates screen
                        pygame.time.wait(1000) #pauses frame changes 
                        current_level = "Map2" #changes current level variable
                        load_level(current_level) #loads current level
                        self.rect.center = (38, 602) #changes position of character
                        m2 = "unlocked"
                    elif teleport_id == 2:
                        self.rect.center = (320, 602)
                        wrong = font.render("Wrong teleport.", True, WHITE) #sets the text for the incorrect teleport
                        screen.blit(wrong, (250, 320))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                elif score < 6:
                    self.rect.center = (320, 602)
                    no_score = font.render("Not enough coins.", True, WHITE) #sets the text for not enough coins
                    screen.blit(no_score, (250, 300)) 
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    

                elif current_level == "Map2" and score >= 12:
                    if teleport_id2 == 1:
                        right = font.render("That's correct!", True, WHITE)
                        screen.blit(right, (250, 320))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        current_level = "Map3"
                        load_level(current_level)
                        self.rect.center = (376, 602)
                        m3 = "unlocked"
                    elif teleport_id2 == 2:
                        self.rect.center = (38, 602)
                        wrong = font.render("Wrong teleport.", True, WHITE)
                        screen.blit(wrong, (250, 320))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                elif score < 12:
                    self.rect.center = (38, 602)
                    no_score = font.render("Not enough coins.", True, WHITE)
                    screen.blit(no_score, (250, 300))
                    pygame.display.flip()
                    pygame.time.wait(1000)

                elif current_level == "Map3" and score >= 18:
                    if teleport_id3 == 1:
                        small_font = pygame.font.Font(None, 40)
                        pygame.draw.rect(screen, BLACK,[155, 310, 325, 70], 35) #draws a black rectangle on screen
                        finish = small_font.render("CONGRATULATIONS!!", True, WHITE) #sets text for completing the game
                        finish2 = font.render("You completed the game!", True, WHITE) #sets text for completing the game
                        screen.blit(finish, (165, 320))
                        screen.blit(finish2, (195, 350))
                        pygame.display.flip() 
                        pygame.time.wait(2000)  
                        done = True
                    elif teleport_id3 != 1:
                        self.rect.center = (376, 602)
                        wrong = font.render("Wrong teleport.", True, WHITE)
                        screen.blit(wrong, (250, 320))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                elif score < 18:
                    self.rect.center = (376, 602)
                    no_score = font.render("Not enough coins.", True, WHITE)
                    screen.blit(no_score, (250, 300))
                    pygame.display.flip()
                    pygame.time.wait(1000)
                          


        for teleport2 in teleport2_group:
            if self.rect.colliderect(teleport2.rect):

                if current_level == "Map1" and score >= 6:
                    if teleport_id == 2:
                        right = font.render("That's correct!", True, WHITE)
                        screen.blit(right, (250, 320))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        current_level = "Map2"
                        load_level(current_level)
                        self.rect.center = (38, 602)
                    elif teleport_id == 1:
                        self.rect.center = (320, 602)
                        wrong = font.render("Wrong teleport", True, WHITE)
                        screen.blit(wrong, (250, 320))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                elif score < 6:
                    self.rect.center = (320, 602)
                    no_score = font.render("Not enough coins.", True, WHITE)
                    screen.blit(no_score, (250, 300))
                    pygame.display.flip()
                    pygame.time.wait(1000)

                elif current_level == "Map2" and score >= 12:
                    if teleport_id2 == 2:
                        right = font.render("That's correct!", True, WHITE)
                        screen.blit(right, (250, 320))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        current_level = "Map3"
                        load_level(current_level)
                        self.rect.center = (376, 602)
                    elif teleport_id2 == 1:
                        self.rect.center = (38, 602)
                        wrong = font.render("Wrong teleport.", True, WHITE)
                        screen.blit(wrong, (250, 320))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                elif score < 12:
                    self.rect.center = (38, 602)
                    no_score = font.render("Not enough coins.", True, WHITE)
                    screen.blit(no_score, (250, 300))
                    pygame.display.flip()
                    pygame.time.wait(1000)

                elif current_level == "Map3" and score >= 18:
                    if teleport_id3 == 2:
                        small_font = pygame.font.Font(None, 40)
                        pygame.draw.rect(screen, BLACK,[155, 310, 325, 70], 35)
                        finish = small_font.render("CONGRATULATIONS!!", True, WHITE)
                        finish2 = font.render("You completed the game!", True, WHITE)
                        screen.blit(finish, (165, 320))
                        screen.blit(finish2, (195, 350))
                        pygame.display.flip() 
                        pygame.time.wait(2000)  
                        done = True
                    elif teleport_id3 != 2:
                        self.rect.center = (376, 602)
                        wrong = font.render("Wrong teleport.", True, WHITE)
                        screen.blit(wrong, (250, 320))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                elif score < 18:
                    self.rect.center = (376, 602)
                    no_score = font.render("Not enough coins.", True, WHITE)
                    screen.blit(no_score, (250, 300))
                    pygame.display.flip()
                    pygame.time.wait(1000)
                        


        for teleport3 in teleport3_group:
            if self.rect.colliderect(teleport3.rect):

                if score >= 18:
                    if teleport_id3 == 3:
                        small_font = pygame.font.Font(None, 40)
                        pygame.draw.rect(screen, BLACK,[155, 310, 325, 70], 35)
                        finish = small_font.render("CONGRATULATIONS!!", True, WHITE)
                        finish2 = font.render("You completed the game!", True, WHITE)
                        screen.blit(finish, (165, 320))
                        screen.blit(finish2, (195, 350))
                        pygame.display.flip() 
                        pygame.time.wait(2000)  
                        done = True

                    elif teleport_id3 != 3:
                        self.rect.center = (376, 602)
                        wrong = font.render("Wrong teleport.", True, WHITE)
                        screen.blit(wrong, (250, 320))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                elif score < 18:
                    self.rect.center = (376, 602)
                    no_score = font.render("Not enough coins.", True, WHITE)
                    screen.blit(no_score, (250, 300))
                    pygame.display.flip()
                    pygame.time.wait(1000)
                            




        for teleport4 in teleport4_group:
            if self.rect.colliderect(teleport4.rect):

                if score >= 18:
                    if teleport_id3 == 4:
                        small_font = pygame.font.Font(None, 40)
                        pygame.draw.rect(screen, BLACK,[155, 310, 325, 70], 35)
                        finish = small_font.render("CONGRATULATIONS!!", True, WHITE)
                        finish2 = font.render("You completed the game!", True, WHITE)
                        screen.blit(finish, (165, 320))
                        screen.blit(finish2, (195, 350))
                        pygame.display.flip()  
                        pygame.time.wait(2000)  
                        done = True

                    elif teleport_id3 != 4:
                        self.rect.center = (376, 602)
                        wrong = font.render("Wrong teleport.", True, WHITE)
                        screen.blit(wrong, (250, 320))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                elif score < 18:
                    self.rect.center = (376, 602)
                    no_score = font.render("Not enough coins.", True, WHITE)
                    screen.blit(no_score, (250, 300))
                    pygame.display.flip()
                    pygame.time.wait(1000)
                            
               

    #gravity method
    def apply_gravity(self):
        if not self.on_ground: #checks if player is on ground
            self.y_speed += gravity #adds the gravity to the vertical velocity
            #terminal velocity
            if self.y_speed > 10: #checks if the speed is greater than 10
                self.y_speed = 10 #prevents the vertical velocity from exceding 10

    #remove method
    def remove(self):
        self.active = False
    

class GameButton:
    def __init__(self, x, y, image, scale):
        #attributes
        width = image.get_width() #gets the wdth of the image 
        height = image.get_height() #gets the height of the image
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale))) #tranforms image to fit screen sizings
        self.rect = self.image.get_rect(topleft=(x, y)) #allows the position of the 
        self.clicked = False #variable to checks if button has been clicked

    #draw method
    def draw(self, surface):
        #tracks if button's been clicked
        action = False

        #gets mouse position
        mouse_pos = pygame.mouse.get_pos()

        #check if mouse is hovering over button
        if self.rect.collidepoint(mouse_pos):
            #checks for a mouse click and prevent multiple clicks
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        # reset the click set when button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on suface
        surface.blit(self.image, self.rect.topleft)

        #return action if true
        return action

class Wall(pygame.sprite.Sprite):
    #attributes
    def __init__(self, x, y, block_image):
        super().__init__()
        self.image = block_image #gets the image for the wall
        self.rect = self.image.get_rect() #creats the box for the wall sprite
        #sets the position for the wall blocks
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    #attributes
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Killzone(pygame.sprite.Sprite):
    #attributes
    def __init__(self, x, y):
        super().__init__()
        self.image = killzone_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Teleport1(pygame.sprite.Sprite):
    #attributes
    def __init__(self, x, y):
        super().__init__()
        self.image = teleport_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Teleport2(pygame.sprite.Sprite):
    #attributes
    def __init__(self, x, y):
        super().__init__()
        self.image = teleport_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Teleport3(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = teleport_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Teleport4(pygame.sprite.Sprite):
    #attributes
    def __init__(self, x, y):
        super().__init__()
        self.image = teleport_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# -- create groups ----------------------------------------------------------
wall_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
killzone_group = pygame.sprite.Group()
teleport1_group = pygame.sprite.Group()
teleport2_group = pygame.sprite.Group()
teleport3_group = pygame.sprite.Group()
teleport4_group = pygame.sprite.Group()

# -- define level grids -----------------------------------------------------

Title_screen = [
    " "
    ]

Menu = [
    "wwwwwwwwwwwwwwwwwwwwwww",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "w                     w",
    "wwwwwwwwwwwwwwwwwwwwwww"
]

Map1 = [
    "wwwwwwwwwwwwwwwwwwwwwww",
    "w        t w        y w",
    "w          w          w",
    "w      wwwww      wwwww",
    "w   ww     w          w",
    "w          w    wwww cw",
    "wwwwwww    w          w",
    "wc         w  wwwww   w",
    "www    wwwwww         w",
    "w          w          w",
    "w  wwww    w  w       w",
    "w          w          w",
    "w      wwwww    w     w",
    "w          wc         w",
    "wc  wwwwwwwwwwwwwwww  w",
    "ww        cw         ww",
    "www        w          w",
    "wwww       w       wwww",
    "w       ww            w",
    "w wwwwwww        wwwwww",
    "w              w wwwwww",
    "wwwwwwwwww   w wcwwwwww",
    "wwwwwwwwwwwwwwwwwwwwwww",
]

Map2 = [
    "wwwwwwwwwwwwwwwwwwwwwww",
    "w t        w y        w",
    "w          w      c   w",
    "wwwww      wwwww  k   w",
    "w     www  w     www  w",
    "w         ww          w",
    "w         cw    wwwwwww",
    "w        wwwkk        w",
    "w          wwww       w",
    "wc  wwwwk  w          w",
    "wk         w c  ww    w",
    "www        wkk        w",
    "w          wwww       w",
    "w   www    w          w",
    "w        k w    ww    w",
    "w  c    w  w          w",
    "w  k  w            wwww",
    "w www                cw",
    "w              kwwwwwww",
    "wwwwww     kwwwwwwwwwww",
    "w       wwwwwwwwwwwwwww",
    "w   wwwwwwwwwwwwwwwwwww",
    "wwwwwwwwwwwwwwwwwwwwwww",
]

Map3 = [
    "wwwwwwwwwwwwwwwwwwwwwww",
    "w t   w y  w u  w   i w",
    "w     w    w    w     w",
    "wwww  www  www  w  wwww",
    "w    cw   wwc   ww   cw",
    "w   wkw   kw  www    kw",
    "wk    w  wwwk   w wwwww",
    "www       cwwww   k   w",
    "w  ww   wwww     w    w",
    "w          w   ww     w",
    "w     ww   w  w       w",
    "w      k  cw  k       w",
    "wk   wwwwwww w        w",
    "w   k      w          w",
    "w  w       wwww      ww",
    "w          w   wwwww cw",
    "ww                   ww",
    "ww w                  w",
    "ww w w             kwww",
    "ww w w w          wwwww",
    "ww w w w w     kwwwwwww",
    "wwkwkwkwkwkwk wwwwwwwww",
    "wwwwwwwwwwwwwwwwwwwwwww",
]

# -- load level data --------------------------------------------------------
def load_level(level):
    #empties each group 
    wall_group.empty()
    coin_group.empty()
    killzone_group.empty()
    teleport1_group.empty()
    teleport2_group.empty()
    teleport3_group.empty()
    teleport4_group.empty()

    x = 0
    y = 0

    #sets the wall image depending on the map being displayed
    if level == "Title_screen":
        current_map = Title_screen
        block = menu_block
    elif level == "Menu":
        current_map = Menu
        block = menu_block
    elif level == "Map1":
        current_map = Map1
        block = block1
    elif level == "Map2":
        current_map = Map2
        block = block2
    elif level == "Map3":
        current_map = Map3
        block = block3

    for row in current_map:
        for col in row:
            if col == "w": #checks which letter, if any, is in the 28x28 pixels  area
                wall = Wall(x, y, block) #sets the variable for the wall with the x and y position and the spirte using the wall class
                wall_group.add(wall) #adds the wall variable to the game window so that the sprite is diplayed.
            elif col == "c":
                coin = Coin(x, y)
                coin_group.add(coin)
            elif col == "k":
                killzone = Killzone(x, y + 14)
                killzone_group.add(killzone)
            elif col == "t":
                teleport = Teleport1(x, y)
                teleport1_group.add(teleport)
            elif col == "y":
                teleport = Teleport2(x, y)
                teleport2_group.add(teleport)
            elif col == "u":
                teleport = Teleport3(x, y)
                teleport3_group.add(teleport)
            elif col == "i":
                teleport = Teleport4(x, y)
                teleport4_group.add(teleport)
        #the space for each spirte
            x += 28 
        y += 28
        x = 0 #display starts from top corner

# -- create player and load initial level -----------------------------------

player = Player() #creats the player
current_level = "Title_screen" #determines the first GUI screen
load_level(current_level) 

# -- create button instances ------------------------------------------------

#creats each button with the position, sprite and scale using the game button class
play_button = GameButton(250, 350, play, 1)
home_button = GameButton(620, 5, house, 1)
map1_button = GameButton(150, 300, map1, 1)
map2_button = GameButton(288, 300, map2, 1)
map3_button = GameButton(420, 300, map3, 1)

# -- main loop --------------------------------------------------------------
while not done:
    clock.tick(60) #determins the amount of frames appear per second

    for event in pygame.event.get(): #goes through all the retrieved events one by one
        if event.type == pygame.QUIT: #checks if the event is to quit the game
            done = True

    #keyboard controls
    keys_pressed = pygame.key.get_pressed() #sets variable for the function to check what keys have been pressed

    #jumping
    if keys_pressed[pygame.K_w] and player.on_ground: #checks if W has been pressed and the player is on the ground
        player.y_speed = -jump_height #sets the vertical velocity to the negative jump height so player returns to the ground
        player.on_ground = False
        #checks if A or D has been pressed and changes the character sprite accordingly
        if keys_pressed[pygame.K_a]: 
            player.image = character_jump_left
        elif keys_pressed[pygame.K_d]:
            player.image = character_jump_right
        
    if keys_pressed[pygame.K_a]: #checks if A has been pressed
        player.move(-2, 0) #moves the player 2 positions to the left each frame
        player.image = character_left #changes the chracter sprite
    if keys_pressed[pygame.K_d]: #checks if D has been pressed
        player.move(2, 0) #moves the player 2 positions to the right with each frame
        player.image = character_right

    if keys_pressed[pygame.K_w] and keys_pressed[pygame.K_a]:
        player.image = character_jump_left
     
    if keys_pressed[pygame.K_w] and keys_pressed[pygame.K_d]:
        player.image = character_jump_right

    #same function as WAD but with the arrow keys
    if keys_pressed[pygame.K_UP] and player.on_ground:
        player.y_speed = -jump_height
        player.on_ground = False
        if keys_pressed[pygame.K_LEFT]:
            player.image = character_jump_left
        elif keys_pressed[pygame.K_RIGHT]:
            player.image = character_jump_right
            
    if keys_pressed[pygame.K_LEFT]:
        player.move(-2, 0)
        player.image = character_left
    if keys_pressed[pygame.K_RIGHT]:
        player.move(2, 0)
        player.image = character_right

    if keys_pressed[pygame.K_UP] and keys_pressed[pygame.K_LEFT]:
        player.image = character_jump_left
     
    if keys_pressed[pygame.K_UP] and keys_pressed[pygame.K_RIGHT]:
        player.image = character_jump_right

    player.apply_gravity()   # Apply gravity
    player.move(0, player.y_speed)  # Move player vertically (gravity + jumping)

    #checks which GUI screen is being displaed then blits the corresponding background sprite
    if current_level == "Title_screen":
        screen.blit(Decision, (0, 0))
    elif current_level == "Menu":
        screen.blit(menubg, (0, 0))
    elif current_level == "Map1":
        screen.blit(bg1, (0, 0))
    elif current_level == "Map2":
        screen.blit(bg2, (0, 0))
    elif current_level == "Map3":
        screen.blit(bg3, (0, 0))

    if player.active == True: #checks if player.active is equal to true and is 
        screen.blit(player.image, [player.rect.x, player.rect.y]) #blits the player with the sprite and position

    #blits each sprite from each group with the image and position
    for wall in wall_group:
        screen.blit(wall.image, [wall.rect.x, wall.rect.y])

    for coin in coin_group:
        screen.blit(coin.image, [coin.rect.x, coin.rect.y])

    for killzone in killzone_group:
        screen.blit(killzone.image, [killzone.rect.x, killzone.rect.y])

    for teleport in teleport1_group:
        screen.blit(teleport.image, [teleport.rect.x, teleport.rect.y])

    for teleport in teleport2_group:
        screen.blit(teleport.image, [teleport.rect.x, teleport.rect.y])

    for teleport in teleport3_group:
        screen.blit(teleport.image, [teleport.rect.x, teleport.rect.y])

    for teleport in teleport4_group:
        screen.blit(teleport.image, [teleport.rect.x, teleport.rect.y])


    #score
    if current_level != "Title_screen" and current_level != "Menu": #checks if the GUI screen being displayed is not the title screen or menu
        font = pygame.font.Font(None, 30)
        score_text = font.render(f"Score: {score}", True, WHITE) #sets the text for the score
        screen.blit(score_text, (5, 5)) #blits text onto game window

    #button actions
        # home button function
        if home_button.draw(screen): #checks if the home button is being drawn and calls draw function         
            current_level = "Menu" #sets current level to the menu
            load_level(current_level)
            player.remove() #removes player from screen

    if current_level == "Title_screen": #checks if title screen is being displayed on the screen
        player.remove() 
        if play_button.draw(screen): #checks if the play button is being drawn and calls draw function  
            current_level = "Menu"
            load_level(current_level)

    
    if current_level == "Menu": #checks if menu  is being displayed on the screen
        #reloads map 1
        if map1_button.draw(screen): #checks if the map 1 button is being drawn and calls draw function         
            current_level = "Map1" #sets current level to map 1
            load_level(current_level)
            player.active = True #blits player back onto screen
            player.rect.center = (320, 602) #changes poistion of the character

        #reloads map 2
        if map2_button.draw(screen): #checks if the map 2 button is being drawn and calls draw function
            if score >= 6:
                current_level = "Map2" #sets current level to map 2
                load_level(current_level)
                player.active = True #displays the player on the screen again
                player.rect.center = (38, 602)
            elif score < 6:
                map3_button.draw(screen)
                locked = font.render("Map is Locked.", True, WHITE)
                screen.blit(locked, (250, 400))
                pygame.display.flip()
                pygame.time.wait(1000)

        #reloads map 3
        if map3_button.draw(screen): #checks if the map 3 button is being drawn and calls draw function
            if score >= 12:
                current_level = "Map3" #sets current level to map 3
                load_level(current_level)
                player.active = True
                player.rect.center = (376, 602)
            elif score < 12:
                locked = font.render("Map is Locked.", True, WHITE)
                screen.blit(locked, (250, 400))
                pygame.display.flip()
                pygame.time.wait(1000)


        
        
    pygame.display.flip()

pygame.quit() #event is to quit the game
