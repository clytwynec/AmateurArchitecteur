import pygame
import RoboPy
import sys
import os

import Colors

from pygame.locals import *

class GS_MainMenu(RoboPy.GameState):
	def __init__(self, kernel, gsm):
		RoboPy.GameState.__init__(self, "MainMenu", kernel, gsm)

		self.mHeading = None
		self.mHeadingRect = None
		self.mMenuItems = {}
		self.mMenuImages = {}
		self.mMenuImagesHover = {}
		self.mMenuRects = {}
		self.mBGSurface = None

	def Initialize(self):

		self.mBGSurface = pygame.Surface(self.mKernel.DisplaySurface().get_size())
		self.mBGSurface.fill(Colors.BLUE)

		self.mHeading = pygame.image.load(os.path.join("Data", "main_title.bmp")).convert()
		self.mHeading.set_colorkey(Colors.BLUE)
		self.mHeadingRect = self.mHeading.get_rect()
		self.mHeadingRect.topleft = (50, 20)

		self.mBigMonster = pygame.image.load(os.path.join("Data", "BigMonster.bmp")).convert()
		self.mBigMonster.set_colorkey(Colors.TRANSPARENT)
		self.mBigMonsterRect = self.mBigMonster.get_rect()
		self.mBigMonsterRect.top = 350
		self.mBigMonsterRect.left = -10

		vSpacing = 80
		vOffset = 75
		items = 1

		if (self.mGameStateManager.GetState("Game").IsInitialized()):
			self.mMenuImages["Game"] = pygame.image.load(os.path.join("Data", "resume_game.bmp")).convert()
			self.mMenuImagesHover["Game"] = pygame.image.load(os.path.join("Data", "resume_game_hover.bmp")).convert()
			self.mMenuImages["Game"].set_colorkey(Colors.BLUE)
			self.mMenuImagesHover["Game"].set_colorkey(Colors.BLUE)
			self.mMenuRects["Game"] = self.mMenuImages["Game"].get_rect()
			self.mMenuRects["Game"].topleft = (275, items * vSpacing + vOffset)
			self.mMenuItems["Game"] = self.mMenuImages["Game"]
			items += 1

		self.mMenuImages["NewGame"] = pygame.image.load(os.path.join("Data", "new_game.bmp")).convert()
		self.mMenuImagesHover["NewGame"] = pygame.image.load(os.path.join("Data", "new_game_hover.bmp")).convert()
		self.mMenuImages["NewGame"].set_colorkey(Colors.BLUE)
		self.mMenuImagesHover["NewGame"].set_colorkey(Colors.BLUE)
		self.mMenuRects["NewGame"] = self.mMenuImages["NewGame"].get_rect()
		self.mMenuRects["NewGame"].topleft = (275, items * vSpacing + vOffset)
		self.mMenuItems["NewGame"] = self.mMenuImages["NewGame"]
		items += 1

		self.mMenuImages["Tutorial1"] = pygame.image.load(os.path.join("Data", "tutorial.bmp")).convert()
		self.mMenuImagesHover["Tutorial1"] = pygame.image.load(os.path.join("Data", "tutorial_hover.bmp")).convert()
		self.mMenuImages["Tutorial1"].set_colorkey(Colors.BLUE)
		self.mMenuImagesHover["Tutorial1"].set_colorkey(Colors.BLUE)
		self.mMenuRects["Tutorial1"] = self.mMenuImages["Tutorial1"].get_rect()
		self.mMenuRects["Tutorial1"].topleft = (275, items * vSpacing + vOffset)
		self.mMenuItems["Tutorial1"] = self.mMenuImages["Tutorial1"]
		items += 1

		self.mMenuImages["Instructions"] = pygame.image.load(os.path.join("Data", "instructionsText.bmp")).convert()
		self.mMenuImagesHover["Instructions"] = pygame.image.load(os.path.join("Data", "instructionsText_hover.bmp")).convert()
		self.mMenuImages["Instructions"].set_colorkey(Colors.BLUE)
		self.mMenuImagesHover["Instructions"].set_colorkey(Colors.BLUE)
		self.mMenuRects["Instructions"] = self.mMenuImages["Instructions"].get_rect()
		self.mMenuRects["Instructions"].topleft = (275, items * vSpacing + vOffset)
		self.mMenuItems["Instructions"] = self.mMenuImages["Instructions"]
		items += 1


		self.mMenuImages["Exit"] = pygame.image.load(os.path.join("Data", "exit.bmp")).convert()
		self.mMenuImagesHover["Exit"] = pygame.image.load(os.path.join("Data", "exit_hover.bmp")).convert()
		self.mMenuImages["Exit"].set_colorkey(Colors.BLUE)
		self.mMenuImagesHover["Exit"].set_colorkey(Colors.BLUE)
		self.mMenuRects["Exit"] = self.mMenuImages["Exit"].get_rect()
		self.mMenuRects["Exit"].topleft = (275, items * vSpacing + vOffset)
		self.mMenuItems["Exit"] = self.mMenuImages["Exit"]
		items += 1

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
		if event.type == MOUSEMOTION:
			for item in self.mMenuRects:
				if (self.mMenuRects[item].collidepoint(event.pos)):
					self.mMenuItems[item] = self.mMenuImagesHover[item]
				else:
					self.mMenuItems[item] = self.mMenuImages[item]
		elif event.type == MOUSEBUTTONDOWN:
			for item in self.mMenuRects:
				if (self.mMenuRects[item].collidepoint(event.pos)):
					if (item == "Exit"):
						pygame.quit()
						sys.exit()
					elif (item == "NewGame"):
						if (self.mGameStateManager.GetState("Game").IsInitialized()):
							self.mGameStateManager.GetState("Game").Destroy()
						
						self.mGameStateManager.SwitchState("Game")
					else:
						self.mGameStateManager.SwitchState(item)


	def Update(self, delta):
		self.mKernel.DisplaySurface().blit(self.mBGSurface, self.mKernel.DisplaySurface().get_rect())
		self.mKernel.DisplaySurface().blit(self.mBigMonster, self.mBigMonsterRect)
		self.mKernel.DisplaySurface().blit(self.mHeading, self.mHeadingRect)

		for item in self.mMenuItems:
			self.mKernel.DisplaySurface().blit(self.mMenuItems[item], self.mMenuRects[item])

		return RoboPy.GameState.Update(self, delta)