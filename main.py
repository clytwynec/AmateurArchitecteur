###################################################################################
# main.py
#
# The kickoff script/main loop.  Sets up the different game systems, and then
# enters the main loop.  Runs until we receive a system event to quit the game
#
# Command Line Arguments
###################################################################################

# System level imports
from optparse import OptionParser
import sys
import math
import pygame
import random

from pygame.locals import *

# App level imports
import RoboPy
from GS_MainMenu import *
from GS_OptionsMenu import *
from Maze import *
from Monster import *

#random.seed(0)

#########################
# Start Main
#########################

#### Parse command line arguments
optionParser = OptionParser()

#### Kick off the graphics/window system
kernel = RoboPy.GameKernel()
screenSurface = kernel.InitializeDisplay((800, 600))
ticker = kernel.Ticker()

maze = Maze(kernel)
maze.Generate((29, 35))
maze.BuildWalls()

monster = Monster(kernel)
monster.SetPath(maze.Solve((0, 0)))

#### Initialize game states
gsm = RoboPy.GameStateManager()
gsm.RegisterState(GS_MainMenu(kernel))
gsm.RegisterState(GS_OptionsMenu(kernel))

gsm.SwitchState("MainMenu")

font = pygame.font.SysFont("Helvetica", 12)

hoverTile = (0, 0)

## Main Loop
while (1):

	delta = ticker.get_time()

	FPSSurf = font.render("FPS: " + str(int(ticker.get_fps())), True, (255, 255, 255))
	FPSRect = FPSSurf.get_rect()
	FPSRect.topright = screenSurface.get_rect().topright
	screenSurface.blit(FPSSurf, FPSRect)

	#gsm.Update(delta)
	monster.Update(delta)

	maze.Draw(hoverTile)
	monster.Draw()

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEMOTION:
			hoverTile = (int(math.floor(event.pos[1] / 20)), int(math.floor(event.pos[0] / 20)))

		elif event.type == MOUSEBUTTONDOWN:
			tile = (int(math.floor(event.pos[1] / 20)), int(math.floor(event.pos[0] / 20)))

			maze.ToggleGridPoint(tile)
			newPath = maze.Solve(monster.CurrentTile())
			monster.SetPath(newPath)
		elif event.type == KEYDOWN:
			if event.key == K_w:
				maze.MoveWall(hoverTile, "N")
				monster.SetPath(maze.Solve(monster.CurrentTile()))

			elif event.key == K_s:
				maze.MoveWall(hoverTile, "S")
				monster.SetPath(maze.Solve(monster.CurrentTile()))

			elif event.key == K_a:
				maze.MoveWall(hoverTile, "W")
				monster.SetPath(maze.Solve(monster.CurrentTile()))

			elif event.key == K_d:
				maze.MoveWall(hoverTile, "E")
				monster.SetPath(maze.Solve(monster.CurrentTile()))

	#kernel.ProcessSystemEvents()
	kernel.FlipDisplay()

	ticker.tick()
	