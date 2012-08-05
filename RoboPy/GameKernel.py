###################################################################################
# GameKernel
#
# Handles system level interfaces for the graphics, system event, 
# and input subsystems.  Provides the basic interface into pygame
#
###################################################################################
import pygame
import sys

from pygame.locals import *

class GameKernel:
	def __init__(self):
		pygame.init()

		print "Pygame Version: " + pygame.version.ver

		self.mDisplaySurface = None
		self.mTicker = pygame.time.Clock()

	#####################################################
	# InitializeDisplay
	#
	# Creates the display window.  If a display is already
	# initialized, this reinitializes the display.
	# If you do this, make sure to propogate the new surface
	# down through the various subsystems that need the
	# display surface
	#
	# Parameters:
	#	dimensions - a 2-tuple of the desired dimenions
	#	fullscreen - fullscreen toggle
	#
	# Returns:
	#	display - The display surface.  Required to allow
	#		other contexts to blit to the screen
	###################################################### 
	def InitializeDisplay(self, dimensions, fullscreen=False):
		flags = pygame.DOUBLEBUF

		if (fullscreen):
			flags = flags | pygame.FULLSCREEN 

		self.mDisplaySurface = pygame.display.set_mode(dimensions, flags)

		assert self.mDisplaySurface, "Display failed to intialize."

		return self.mDisplaySurface


	#####################################################
	# GetDisplaySurface
	#
	# Returns the current display surface
	#####################################################
	def DisplaySurface(self):
		return self.mDisplaySurface

	#####################################################
	# GetTicker
	#
	# Returns the system ticker.
	#####################################################
	def Ticker(self):
		return self.mTicker

	#####################################################
	# FlipDisplay
	#
	# Flips the display surface
	#####################################################
	def FlipDisplay(self):
		pygame.display.flip()
		
		#self.mDisplaySurface.fill(pygame.Color(0, 100, 100))

	#####################################################
	# ProcessSystemEvents
	# 
	# Processes system events and dispatches them to the
	# system or input subsystems as appropriate
	#####################################################
	def ProcessSystemEvents(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()