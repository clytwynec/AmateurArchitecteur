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
maze.Generate((10, 10))
maze.Draw()

#### Initialize game states
gsm = RoboPy.GameStateManager()
gsm.RegisterState(GS_MainMenu(kernel))
gsm.RegisterState(GS_OptionsMenu(kernel))

gsm.SwitchState("MainMenu")

font = pygame.font.SysFont("Helvetica", 12)

ticks = 0

### Main Loop
# while (1):

# 	delta = ticker.get_time()

# 	if (ticks > 100):
# 		gsm.SwitchState("OptionsMenu")
# 	elif (ticks < 101):
# 		ticks += 1

# 	FPSSurf = font.render("FPS: " + str(int(ticker.get_fps())), True, (255, 255, 255))
# 	FPSRect = FPSSurf.get_rect()
# 	FPSRect.topright = screenSurface.get_rect().topright
# 	screenSurface.blit(FPSSurf, FPSRect)

# 	gsm.Update(delta)

# 	kernel.ProcessSystemEvents()
# 	kernel.FlipDisplay()

# 	ticker.tick()