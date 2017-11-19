import pygame, sys, random
from pygame.locals import *

SIZE = 20
WINDOWWIDTH = WINDOWHEIGHT = 20*SIZE
FPS = 10

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOUR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def terminate():
	pygame.quit()
	sys.exit()

def changeColour(x, y, colour):				#Changes the colour of an area 20x*20 square pixels
	for i in range(x*SIZE, (x+1)*SIZE):
		for j in range(y*SIZE, (y+1)*SIZE):
			pixArray[i][j] = colour
	return None

def getFoodLocation():						#the code responsible for spawning new food everytime the snake eats some
	x = random.randint(0, 19)
	y = random.randint(0, 19)
	while(pixArray[x*SIZE][y*SIZE] != windowSurface.map_rgb(WHITE)):
		x = random.randint(0, 19)
		y = random.randint(0, 19)
	changeColour (x, y, RED)
	return x, y

UP = "U"
DOWN = "D"
LEFT =  "L"
RIGHT =  "R"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (233, 86, 78)
GREEN = (0, 255, 0)
BLUE = (78, 174, 233)
TEXTCOLOUR = BLACK
font = pygame.font.SysFont(None, 48)

pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('S N A K E')

windowSurface.fill(WHITE)
drawText('S N A K E', font, windowSurface, (WINDOWWIDTH/3), (WINDOWHEIGHT/3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH/3) - 30, (WINDOWHEIGHT/3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

pygame.display.update()

topScore = 0
#overall game loop, for topscore purposes
while True:

	#reset the game 
	snake = [[2, 0, RIGHT], [1, 0, RIGHT], [0, 0, RIGHT]]
	score = 0
	swapper = ''
	windowSurface.fill(WHITE)
	for i in snake:
		changeColour(i[0], i[1], BLUE)
	x, y = getFoodLocation()
	pixArray = pygame.PixelArray(windowSurface)
	#game loop which runs every game
	while True:
		#gets the user input
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			if event.type == KEYDOWN:
				if event.key == K_LEFT or event.key == ord('a') :
					swapper = LEFT
				elif event.key == K_RIGHT or event.key == ord('d'):
					swapper = RIGHT
				elif event.key == K_DOWN or event.key == ord('s'):
					swapper = DOWN
				elif event.key == K_UP or event.key == ord('W'):
					swapper = UP
			orig = swapper
		
		#prevents the snake from reversing in any direction
		if ((snake[0][2] == UP and swapper == DOWN) or (snake[0][2] == DOWN and swapper == UP) or (snake[0][2] == RIGHT and swapper == LEFT) or (snake[0][2] == LEFT and swapper == RIGHT)):
			swapper = snake[0][2]
		
		#the block of code responsible for moving the snake
		for i in range(len(snake)):
			snake[i][2], swapper = swapper, snake[i][2]
			if snake[i][2] == RIGHT:
				snake[i][0] += 1
			elif snake[i][2] == LEFT:
				snake[i][0] -= 1
			elif snake[i][2] == DOWN:
				snake[i][1] += 1
			elif snake[i][2] == UP:
				snake[i][1] -= 1
		
		swapper = orig #very, very important line. removing this line breaks the movement of the snake
		

		#These two if blocks are responsible for ending the game
		if snake[0][0] > 19 or snake[0][0] < 0 or snake[0][1] < 0 or snake[0][1] > 19:
		 	break
		if [snake[0][0], snake[0][1], UP] in snake[1:] or [snake[0][0], snake[0][1], DOWN] in snake[1:] or [snake[0][0], snake[0][1], RIGHT] in snake[1:] or [snake[0][0], snake[0][1], LEFT] in snake[1:]: 
		 	break
		
		
		#The block of code below is responsible for adding a new square to the snake, and takes into account all the edge cases.
		if snake[0][0] == x and snake[0][1] == y:
			x, y = getFoodLocation()
			
			if snake[len(snake) - 1][2] == DOWN: #if the end of the snake was moving downwards
				if snake[len(snake) - 1][1] >= 1:
					snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1]-1, DOWN])
				else:
					if snake[len(snake) - 1][0] >= 1:
						snake.append([snake[len(snake)-1][0]-1, snake[len(snake)-1][1], RIGHT])
					else:
						snake.append([snake[len(snake)-1][0]+1, snake[len(snake)-1][1], LEFT])
			
			if snake[len(snake) - 1][2] == UP:#if the end of the snake was moving upwards
				if snake[len(snake) - 1][1] <= 18:
					snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1]+1, UP])
				else:
					if snake[len(snake) - 1][0] >= 1:
						snake.append([snake[len(snake)-1][0]-1, snake[len(snake)-1][1], RIGHT])
					else:
						snake.append([snake[len(snake)-1][0]+1, snake[len(snake)-1][1], LEFT])
			
			if snake[len(snake) - 1][2] == LEFT:#if the end of the snake was moving towards the left
				if snake[len(snake) - 1][0] <= 18:
					snake.append([snake[len(snake)-1][0]+1, snake[len(snake)-1][1], LEFT])
				else:
					if snake[len(snake) - 1][1] >= 1:
						snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1]-1, DOWN])
					else:
						snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1]+1, UP])
			
			if snake[len(snake) - 1][2] == RIGHT:#if the end of the snake was moving towards the right
				if snake[len(snake) - 1][0] >= 1:
					snake.append([snake[len(snake)-1][0]-1, snake[len(snake)-1][1], RIGHT])
				else:
					if snake[len(snake) - 1][0] >= 1:
						snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1]-1, DOWN])
					else:
						snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1]+1, UP])	
		
		windowSurface.fill(WHITE)
		for i in snake:
			changeColour(i[0], i[1], BLUE)
		changeColour(x, y, RED)
		pygame.display.update()
		mainClock.tick(FPS)