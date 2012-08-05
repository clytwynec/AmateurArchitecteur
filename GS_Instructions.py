import pygame
import RoboPy
import sys
import os

import Colors

from pygame.locals import *

class GS_Instructions(RoboPy.GameState):
	def __init__(self, kernel, gsm):
		RoboPy.GameState.__init__(self, "Instructions", kernel, gsm)

		self.mBGRect = None
		self.mBGSurface = None

	def Initialize(self):

		self.mBGSurface = pygame.image.load(os.path.join("Data", "instructions.bmp")).convert()
		self.mBGRect = self.mBGSurface.get_rect()

		return RoboPy.GameState.Initialize(self)

	def Destroy(self):
		return RoboPy.GameState.Destroy(self)

	def Pause(self):
		self.mMenuItems = {}
		self.mHeading = None

		return RoboPy.GameState.Pause(self)

	def Unpause(self):
		self.Initialize()

		return RoboPy.GameState.Unpause(self)

	def HandleEvent(self, event):
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				self.mGameStateManager.SwitchState("MainMenu")


	def Update(self, delta):
		self.mKernel.DisplaySurface().blit(self.mBGSurface, self.mBGRect)

		return RoboPy.GameState.Update(self, delta)