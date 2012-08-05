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
from GS_Game import *

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

#### Initialize game states
gsm = RoboPy.GameStateManager()
gsm.RegisterState(GS_MainMenu(kernel, gsm))
gsm.RegisterState(GS_OptionsMenu(kernel, gsm))
gsm.RegisterState(GS_Game(kernel, gsm))

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

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		else:
			gsm.GetActiveState().HandleEvent(event)

	kernel.FlipDisplay()

	ticker.tick()
	