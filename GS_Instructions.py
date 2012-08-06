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

		self.mBackImage = pygame.image.load(os.path.join("Data", "back.bmp")).convert()
		self.mBackHover = pygame.image.load(os.path.join("Data", "back_hover.bmp")).convert()
		self.mBackButton = self.mBackImage
		self.mBackRect = self.mBackButton.get_rect()
		self.mBackRect.topleft = (630, 530)


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
		elif event.type == MOUSEMOTION:
			if (self.mBackRect.collidepoint(event.pos)):
				self.mBackButton = self.mBackHover
			else:
				self.mBackButton = self.mBackImage
		elif event.type == MOUSEBUTTONDOWN:
			if (self.mBackRect.collidepoint(event.pos)):
				self.mGameStateManager.SwitchState("MainMenu")


	def Update(self, delta):
		self.mKernel.DisplaySurface().blit(self.mBGSurface, self.mBGRect)
		self.mKernel.DisplaySurface().blit(self.mBackButton, self.mBackRect)

		return RoboPy.GameState.Update(self, delta)