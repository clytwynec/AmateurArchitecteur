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
import os
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

def CalcScore(level, moves):
	difficulty = level * 10
	if moves == 0: 
		moves = 1
	score = int(math.floor(difficulty * (100 * (1.0/moves))))
	print moves
	print level
	print score
	return score


#########################
# Start Main
#########################

#### Parse command line arguments
optionParser = OptionParser()

#### Kick off the graphics/window system
kernel = RoboPy.GameKernel()
screenSurface = kernel.InitializeDisplay((800, 600))
ticker = kernel.Ticker()

#### Stuff
mazeSize = (29, 39)
maze = Maze(kernel)
maze.Generate(mazeSize)
#maze.Load(os.path.join("Data", "tutorial1.maze"))
maze.BuildWalls()

monster = Monster(kernel)
monster.SetPath(maze.Solve((0, 0)))
monster.SetCage(maze.GetCage())

#### Initialize game states
gsm = RoboPy.GameStateManager()
gsm.RegisterState(GS_MainMenu(kernel))
gsm.RegisterState(GS_OptionsMenu(kernel))

gsm.SwitchState("MainMenu")

font = pygame.font.SysFont("Helvetica", 12)

hoverTile = (0, 0)

score = 0
moves = 0
level = 1
markedScore = 0

## Main Loop
while (1):

	delta = ticker.get_time()

	FPSSurf = font.render("FPS: " + str(int(ticker.get_fps())), True, (255, 255, 255))
	FPSRect = FPSSurf.get_rect()
	FPSRect.topright = screenSurface.get_rect().topright
	screenSurface.blit(FPSSurf, FPSRect)

	#gsm.Update(delta)
	monster.Update(delta)

	#check score
	if monster.IsCaught() and markedScore == 0:
		score = score + CalcScore(level, moves)
		markedScore = 1

	maze.Draw(hoverTile)
	monster.Draw()

	if (monster.IsFinished()):
		maze.Generate(mazeSize)
		level += 1 
		moves = 0
		maze.BuildWalls()
		monster.Reset()
		markedScore = 0
		monster.SetPath(maze.Solve(monster.CurrentTile()))

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
				moves += maze.MoveWall(hoverTile, "N")
				monster.SetPath(maze.Solve(monster.CurrentTile()))

			elif event.key == K_s:
				moves += maze.MoveWall(hoverTile, "S")
				monster.SetPath(maze.Solve(monster.CurrentTile()))

			elif event.key == K_a:
				moves += maze.MoveWall(hoverTile, "W")
				monster.SetPath(maze.Solve(monster.CurrentTile()))

			elif event.key == K_d:
				moves += maze.MoveWall(hoverTile, "E")
				monster.SetPath(maze.Solve(monster.CurrentTile()))

			elif event.key == K_SPACE:
				monster.SetSpeed(10)
		elif event.type == KEYUP:
			if event.key == K_SPACE:
				monster.SetSpeed(2)

	#kernel.ProcessSystemEvents()
	kernel.FlipDisplay()

	ticker.tick()
	