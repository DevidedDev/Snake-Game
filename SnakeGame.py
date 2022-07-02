#py -m pip install -U pygame --user
#TO DO:

#DONE
    #maake the score responsive
    #fix game over
    #make starting screen
    #make play again button
    #make the 2nd block of the snake at the start
    #GAME COMPLETE :D

from argparse import HelpFormatter
from cmath import rect
from turtle import fillcolor
import pygame, sys, time, random
from pygame.locals import *
import enum





pygame.init()
i  = 0
    
FPS= 30
fpsClock=pygame.time.Clock()


scale = 66


width= 16 * scale
height= 16 * scale

DISPLAYSURF=pygame.display.set_mode((width,height),0,32)


DEFAULT_BACKGROUND_SIZE = (16*scale, 16  * scale)
DEFAULT_CHARACTER_SIZE = (1*scale, 1  * scale)

#naslov okna
pygame.display.set_caption('Snake')
#slika za ozadje
background=pygame.image.load('background.png')
background = pygame.transform.scale(background, DEFAULT_BACKGROUND_SIZE)

#DEFINING THE ROTATION
UP='up'
LEFT='left'
RIGHT='right'
DOWN='down'
smer = RIGHT


#SPRITE SETUPS
sprite=pygame.image.load('snake.png') #zacetna slika
sprite = pygame.transform.scale(sprite, DEFAULT_CHARACTER_SIZE)

apple= pygame.image.load('apple.png') #jabolko
apple = pygame.transform.scale(apple, DEFAULT_CHARACTER_SIZE)

#SCORE settup
score = 0
highscore  = 0


#snake joints class
class characterClass:
    def __init__(self, sx, sy, snake_number):
        ssprite=pygame.image.load('snake.png') #zacetna slika
        self.sprite= pygame.transform.scale(ssprite, DEFAULT_CHARACTER_SIZE)
        self.spritex= sx
        self.spritey= sy
        self.snake_part=snake_number
        
    def display(self):
        DISPLAYSURF.blit(sprite,(spritex,spritey))
        spritex=1
        spritey=1

#HEAD OF SNAKE:
spritex = 2 * scale
spritey = 8 * scale
s1 = characterClass(spritex, spritey, 1)
s2 = characterClass((spritex), (spritey), 2)

snake_objects = [s1, s2] #append adds a single item to a list


#COLORS:
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
dark_green = (0, 102, 0)
light_green = (0, 179, 0)

#FONTS
font_score = pygame.font.Font('freesansbold.ttf', round(scale*0.7))
font_highscore = pygame.font.Font('freesansbold.ttf', round(scale*0.5))
font_button =  pygame.font.Font('freesansbold.ttf', round(scale*0.7))
font_title = pygame.font.Font("freesansbold.ttf", scale * 2)

#TEXT
class Text():
    def __init__(self, display_text, text_type):
        self.display_text = display_text
        self.text_type = text_type
        

        #SCORE COUNTER
        if (self.text_type == "Score"):
                
                self.text_position = (12*scale, 0.5*scale) #position of text            
                self.text_display = font_score.render(("Score: "+ str(score)), white, white) #the text that will be displayed

        #HIGHSCORE      
        if (self.text_type == "HighScore"):
            self.text_position = (12*scale, 1.2*scale) #position of text            
            self.text_display = font_highscore.render(("High Score: "+ str(highscore)), white, white) #the text that will be displayed
        #TYTLES             
        elif (self.text_type == "Title"):
            
            self.text_display = font_title.render(self.display_text, black, black)
            self.text_position = ((width/2 - self.text_display.get_rect().width/2 ),5*scale) #x coord: Middle of the screen, now getting the middle of the square surrounded by the text that I have rendered before, and taking that middle away from the whole screens middle so the text is nicely centered :D;     y cord: just on the 5th block
            

    def process(self):     
        if (self.text_type == "Score"):          
            self.text_display = font_score.render(("Score: "+ str(score)), white, white) #renders the score so (out of a built string that is a normal string + an int converted into a string)
        DISPLAYSURF.blit(self.text_display, (self.text_position)) 

        if (self.text_type == "HighScore"):          
            self.text_display = font_highscore.render(("High Score: "+ str(highscore)), white, white) #renders the score so (out of a built string that is a normal string + an int converted into a string)
        DISPLAYSURF.blit(self.text_display, (self.text_position)) 
        
#Making the text objects        
t_1 =Text("Snake", "Title")
t_2 =Text("Game over", "Title")
t_s =Text("Score:", "Score")
t_hs =Text("Higscore:", "HighScore")







#BUTTONS
class Button():
    def __init__(self, x_pos, y_pos, width, height,  display_text): #all of the variables need to create the button
        self.x_pos = x_pos*scale
        self.y_pos = y_pos*scale
        self.width = width*scale
        self.height = height*scale
        
        self.display_text = display_text
        self.button_text = font_button.render(self.display_text, black, black)
        

        self.buttonSurface = pygame.Surface((self.width , self.height))
        self.buttonRect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.buttonPressed = False

        self.buttonSurf = font_button.render(self.display_text, True, dark_green)

        self.fillColors = {
            'normal': '#265D00',
            'hover': '#9EE493',
            'pressed': '#009900',
        }

    def process(self):
        mousePos = pygame.mouse.get_pos() #gets the mouse position, saves it in a variable
        self.buttonSurface.fill(self.fillColors['normal']) #fills the button with a color
        if self.buttonRect.collidepoint(mousePos): #if mouse hovering on button, change color
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:#if the first mouse button out of the 3 is pressed (the first one is the left lcick)
                self.buttonSurface.fill(self.fillColors['pressed']) #changes the color
                if (self.buttonPressed == False):
                    self.buttonPressed = True 
                    self.onclickFunction()

        #setting the coordinates and blitting the button + the button text
        self.buttonSurface.blit(self.buttonSurf,(self.buttonRect.width, self.buttonRect.width)) 
        self.text_pos = ((self.x_pos + self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2) , (self.y_pos + self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2)) # goes to the top left corner of the square, then the text start goes to the middle of the square, the last width and scale are the text's I'm quite sure

        DISPLAYSURF.blit(self.buttonSurface, self.buttonRect)
        DISPLAYSURF.blit(self.button_text, self.text_pos) 

    def onclickFunction(self):
        if (self.display_text  == "Quit game"):
            print("bye")
            pygame.quit()
        
        elif (self.display_text == "Play again"):
            print("hi")
            global alive
            global restart
            alive = True
            restart = True
            self.buttonPressed = False

        elif (self.display_text == "Play"):
            print("Start game")
            self.buttonPressed = False
            global started
            started = True


                              

#creates a new button object  
b_1 = Button(5.5,8,5,1.5,   "Play again") #PLAY AGAIN BUTTON
b_2 = Button(11.2,14,4,1.2,   "Quit game") #QUIT GAME BUTTON
b_3 = Button(5.5,8,5,1.5,   "Play")

death_objects = (b_1, b_2, t_2, t_s, t_hs)
menu_objects = (b_3, b_2, t_1)

#BACKGROUND MUSIC
#pygame.mixer.music.load('bgm.mp3')
#pygame.mixer.music.play(-1, 0.0)

#SOUND EFFECTS
eat_sound =pygame.mixer.Sound("snake_eat.wav")
crash_sound =pygame.mixer.Sound("snake_crash.wav")

movement_count= 0
#APPLE SETUP
apple_timer= 0
apple_positionx = -100
apple_positiony = -100
apple_spawned = False


snake_parts_count = 1
clock_counter = 0

i = 0
count = 0
old_snake_object = characterClass(1,1, 1)
restart = False
started = False

distance = 1 * scale / 3 #za kolikšen del kocke (1 kocka = scale) se premakne block


#----------------------------------------- GAMEPLAY -----------------------------------------------


smer = "desno"
stara_smer= smer
alive = True

                         
while True:

    DISPLAYSURF.blit(background,(0,0))



    if ((started == True) & (alive == True)):
        
        if (restart == True):
            smer = "desno"
            stara_smer= smer
            score = 0
            restart = False

            spritex = 2 * scale
            spritey = 8 * scale
            s1 = characterClass(spritex, spritey, 1)
            s2 = characterClass((spritex), (spritey), 2)

            snake_objects.clear()
            snake_objects = [s1, s2] #append adds a single item to a list

        #displays all of your snake parts
        for i in snake_objects:
            DISPLAYSURF.blit(i.sprite,(i.spritex,i.spritey))

        



        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()


        if (apple_spawned == True):
            DISPLAYSURF.blit(apple,(apple_positionx, apple_positiony))
        
    
        #shows the score and highscore
        t_s.process()
        t_hs.process()

                
        keys_pressed = pygame.key.get_pressed()

         
        #premikanje input
        if (keys_pressed[pygame.K_LEFT] & (smer != "right")):
            smer = "left"

        if (keys_pressed[pygame.K_RIGHT] & (smer != "left")):
            smer = "right"

        if (keys_pressed[pygame.K_UP] & (smer != "down")):
            smer = "up"

        if (keys_pressed[pygame.K_DOWN]& (smer != "up")):
            smer = "down"

        


        #premikanje
        if (stara_smer == "left"):
            s1.spritex -= distance 
    
            
        elif (stara_smer == "right"):
            s1.spritex += distance
            
        elif (stara_smer == "up"):
            s1.spritey -= distance
            
        elif (stara_smer == "down"):
            s1.spritey += distance


        movement_count +=1
        if (movement_count == 3):
            movement_count = 0
            stara_smer = smer

            

        #GIVES THE ATRIBUTES OF THE OLD OBJECT TO THE NEW OBJECT
        if (len(snake_objects) >= 2): #checks if the snake has 2 parts
            snake_objects[1] = old_snake_object
        index = len(snake_objects) - 1 #da index na zadnji element (a list starts from 0)
        while  (index >= 1):
            snake_objects[index]= snake_objects[index-1] #give the atributes of the block infront to the block in the back all the way to 0
            index -= 1
            
            
        #APPLE SPAWNER      
        if (apple_spawned == False):
            apple_positionx = (random.randint(1, 15)) * scale
            apple_positiony = (random.randint(1, 15)) * scale
            print ("apple postition:", apple_positiony)
            print(apple_positiony)
            apple_timer = 0
            apple_spawned = True 
 
        
        #EAT APPLE
        if ((apple_positionx - scale + 1) < s1.spritex < (apple_positionx + scale -1)) and ((apple_positiony - scale +1) < s1.spritey < (apple_positiony + scale -1)):
            apple_spawned = False
            snake_parts_count += 1
            snake_objects.append(characterClass(-scale, -scale, snake_parts_count))
            score += 1
            pygame.mixer.Sound.play(eat_sound)


            print(i.sprite,(i.spritex,i.spritey, i.snake_part))
            #print("Parts: ", snake_parts_count)
            print(snake_objects)
            print("snake length: ",  len(snake_objects))
            print(s1.spritex)
            print(s1.spritey)



            


        old_snake_object = characterClass(s1.spritex, s1.spritey, 2)
            



        #END GAME
            #map borders 
        if (s1.spritex >= width ) or (s1.spritex < 0) or (s1.spritey >= height ) or (s1.spritey < 0):
            #pygame.quit()
            print("out of borders")
            alive = False
            pygame.mixer.Sound.play(crash_sound)
            if (highscore < score):
                highscore = score
            

        for i in (snake_objects[2:]):
            if ((i.spritex == s1.spritex) & (i.spritey == s1.spritey)):
                #pygame.quit()
                print("You tried eating yourself")
                alive = False
                pygame.mixer.Sound.play(crash_sound)
                if (highscore < score):
                    highscore = score    
            
            
    elif (alive == False):
        for object in death_objects:# cycles through the list of objects and starts the process in each of the object from the button class
            object.process() 
        pygame.event.get()
        
               

    elif (started == False):
        for object in menu_objects:# cycles through the list of objects and starts the process in each of the object from the button class
            object.process() 
        pygame.event.get() 


    pygame.display.update()
    fpsClock.tick(FPS)

    
    
