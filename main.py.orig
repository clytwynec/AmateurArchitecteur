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
import pygame

from pygame.locals import *

# App level imports
import RoboPy
from GS_MainMenu import *
from GS_OptionsMenu import *
from Maze import *
from Monster import *

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
maze.Generate((71, 59))
maze.Draw()

monster = Monster(kernel)
monster.SetPath([(10, 0), (10, 10), (20, 10), (30, 10), (40, 10)])

#### Initialize game states
gsm = RoboPy.GameStateManager()
gsm.RegisterState(GS_MainMenu(kernel))
gsm.RegisterState(GS_OptionsMenu(kernel))

gsm.SwitchState("MainMenu")

font = pygame.font.SysFont("Helvetica", 12)

## Main Loop
while (1):

	delta = ticker.get_time()

	FPSSurf = font.render("FPS: " + str(int(ticker.get_fps())), True, (255, 255, 255))
	FPSRect = FPSSurf.get_rect()
	FPSRect.topright = screenSurface.get_rect().topright
	screenSurface.blit(FPSSurf, FPSRect)

	gsm.Update(delta)
	monster.Update(delta)

	maze.Draw()
	monster.Draw()

	kernel.ProcessSystemEvents()
	kernel.FlipDisplay()

	ticker.tick()