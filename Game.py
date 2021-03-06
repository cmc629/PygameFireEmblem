import pygame, sys
from pygame.locals import *
from time import *
from SacaeMap import *

# Turn Debug mode on and off
DEBUG = True
WHITE = [255, 255, 255]
BLACK = [0  , 0  , 0  ]

# Initialize Player and Position
Lord = pygame.image.load('lyn.png')
playerPos1 = [MAPWIDTH-1,MAPHEIGHT-1]
Mage = pygame.image.load('mage.png')
playerPos2 = [MAPWIDTH-2,MAPHEIGHT-1]
Archer = pygame.image.load('archer.png')
playerPos3 = [MAPWIDTH-3,MAPHEIGHT-1]
Bard = pygame.image.load('bard.png')
playerPos4 = [MAPWIDTH-4,MAPHEIGHT-1]

PLAYERS = [Lord, Mage, Archer, Bard]
PLAYER_NAMES = ['Lord', 'Mage', 'Archer', 'Bard']

player_pos_coords = [playerPos1, playerPos2, playerPos3, playerPos4]

PLAYER = PLAYERS[0]
PLAYER_NAME = PLAYER_NAMES[0]
playerPos = player_pos_coords[0]

# Initialize Cursor
Cursor = pygame.image.load('cursor.png')
cursorPos = [playerPos[0],playerPos[1]]

new_coord = []
walk_delay = 1
walk_cd = 0
step_delay = 1
step_cd = 0
clock = pygame.time.Clock()
clock2 = pygame.time.Clock()

# Set up the Display
pygame.init()
if DEBUG:
	const = 200
	INVFONT = pygame.font.SysFont('FreeSans.tff',18)
	
else:
	const = 0

DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE+const))

while True:

	cursor_coord = [pygame.mouse.get_pos()[0]/TILESIZE, pygame.mouse.get_pos()[1]/TILESIZE]

	# Movement Cooldown Clock
	turn_clock = clock.tick() / 1000.0
	walk_cd -= turn_clock

	step_clock = clock2.tick() / 1000.0
	step_cd -= step_clock

	if walk_cd <= 0:
		walk_cd = 0
	if step_cd <= 0:
		step_cd = 0
	
	cursorPos = playerPos

	# Get all user events
	for event in pygame.event.get():
		# If user wants to quit, end game and and close window
		if (event.type == QUIT):
			pygame.quit()
			sys.exit()

		elif pygame.mouse.get_pressed()[0]:
			for i in range(len(player_pos_coords)):
				if player_pos_coords[i][0] == cursor_coord[0] and player_pos_coords[i][1] == cursor_coord[1]:
					PLAYER = PLAYERS[i]
					PLAYER_NAME = PLAYER_NAMES[i]
					playerPos = player_pos_coords[i]

		# Keyboard Inputs (Can remove later on)
		elif (event.type == KEYDOWN):
			if (event.key == K_RIGHT) and (playerPos[0] < MAPWIDTH - 1):
				playerPos[0] += 1
			if (event.key == K_LEFT) and (playerPos[0] > 0):
				playerPos[0] -= 1
			if (event.key == K_UP) and (playerPos[1] > 0):
				playerPos[1] -= 1
			if (event.key == K_DOWN) and (playerPos[1] < MAPHEIGHT - 1):
				playerPos[1] += 1

		# Mouse inputs
		elif pygame.mouse.get_pressed()[2]: 
			new_coord = [pygame.mouse.get_pos()[0]/TILESIZE, pygame.mouse.get_pos()[1]/TILESIZE]
			if walk_cd <= 0:
				for i in range(len(new_coord)):
					while playerPos[i] != new_coord[i]:
						if new_coord[i] > playerPos[i]:
							playerPos[i] += 1
						if new_coord[i] < playerPos[i]:
							playerPos[i] -= 1
					walk_cd = walk_delay

	# Loop through each row
	for row in range(MAPHEIGHT):
		# Loop through each column in the row
		for column in range(MAPWIDTH):
		# Draw the resource at that position in the tilemap
			DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TILESIZE, row*TILESIZE))

	# Display player at current position
	DISPLAYSURF.blit(Lord,(playerPos1[0]*TILESIZE,playerPos1[1]*TILESIZE))
	DISPLAYSURF.blit(Mage,(playerPos2[0]*TILESIZE,playerPos2[1]*TILESIZE))
	DISPLAYSURF.blit(Archer,(playerPos3[0]*TILESIZE,playerPos3[1]*TILESIZE))
	DISPLAYSURF.blit(Bard,(playerPos4[0]*TILESIZE,playerPos4[1]*TILESIZE))
	DISPLAYSURF.blit(Cursor,(cursorPos[0]*TILESIZE,cursorPos[1]*TILESIZE))

	# Display DEBUG Information
	if DEBUG:
		placePosition = 5
		Text_Char_Pos = INVFONT.render('Character Position: ' + str(playerPos) + '  ', True, WHITE, BLACK)
		DISPLAYSURF.blit(Text_Char_Pos,(placePosition,MAPHEIGHT*TILESIZE))

		cursor_coord = [pygame.mouse.get_pos()[0]/TILESIZE, pygame.mouse.get_pos()[1]/TILESIZE]
		Text_Cursor_Pos = INVFONT.render('Cursor Position: ' + str(cursor_coord) + '  ', True, WHITE, BLACK)
		DISPLAYSURF.blit(Text_Cursor_Pos,(placePosition,MAPHEIGHT*TILESIZE+15))

		Text_Button_Statuses = INVFONT.render('Mouse Buttons: ' + str(pygame.mouse.get_pressed()) + '  ', True, WHITE, BLACK)
		DISPLAYSURF.blit(Text_Button_Statuses,(placePosition,MAPHEIGHT*TILESIZE+30))

		Text_New_Coords = INVFONT.render('Final Coordinates: ' + str(new_coord) + '  ', True, WHITE, BLACK)
		DISPLAYSURF.blit(Text_New_Coords,(placePosition, MAPHEIGHT*TILESIZE + 45))

		Text_Char_Selected = INVFONT.render('Currently Selected: ' + PLAYER_NAME + '        ', True, WHITE, BLACK)
		DISPLAYSURF.blit(Text_Char_Selected,(placePosition, MAPHEIGHT*TILESIZE + 60))

		Text_Walk_Cooldown = INVFONT.render('Movement Cooldown: ' + str(walk_cd) + (9*'       '), True, WHITE, BLACK)
		DISPLAYSURF.blit(Text_Walk_Cooldown,(placePosition + 175, MAPHEIGHT*TILESIZE))

		Text_Step_Cooldown = INVFONT.render('Step Cooldown: ' + str(step_cd) + (9*'         '), True, WHITE, BLACK)
		DISPLAYSURF.blit(Text_Step_Cooldown,(placePosition + 175, MAPHEIGHT*TILESIZE + 15))
	pygame.display.update()
