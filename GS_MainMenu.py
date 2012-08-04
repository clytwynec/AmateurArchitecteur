import pygame
import RoboPy

class GS_MainMenu(RoboPy.GameState):
	def __init__(self, kernel):
		RoboPy.GameState.__init__(self, "MainMenu", kernel)

		self.mHeaderFont = pygame.font.SysFont("Helvetica", 24, (255, 255, 255), True)
		self.mMenuFont = pygame.font.SysFont("Helvetica", 16, (255, 255, 255))
		self.mHeading = None
		self.mMenuItems = {}
		self.mMenuRects = {}

	def Initialize(self):
		self.mHeading = self.mHeaderFont.render("RoboPy Game Engine - Main Menu", True, (255, 255, 255))
		self.mHeadingRect = self.mHeading.get_rect()
		self.mHeadingRect.topleft = (100, 100)

		self.mMenuItems["Game"] = self.mMenuFont.render("New Game", True, (255, 255, 255))
		self.mMenuRects["Game"] = self.mMenuItems["Game"].get_rect()
		self.mMenuRects["Game"].topleft = (150, 200)

		self.mMenuItems["LoadGame"] = self.mMenuFont.render("Load Game", True, (255, 255, 255))
		self.mMenuRects["LoadGame"] = self.mMenuItems["LoadGame"].get_rect()
		self.mMenuRects["LoadGame"].topleft = (150, 250)

		self.mMenuItems["Options"] = self.mMenuFont.render("Options", True, (255, 255, 255))
		self.mMenuRects["Options"] = self.mMenuItems["Options"].get_rect()
		self.mMenuRects["Options"].topleft = (150, 300)

		self.mMenuItems["Exit"] = self.mMenuFont.render("Exit", True, (255, 255, 255))
		self.mMenuRects["Exit"] = self.mMenuItems["Exit"].get_rect()
		self.mMenuRects["Exit"].topleft = (150, 350)


		return RoboPy.GameState.Initialize(self)

	def Destroy(self):
		return RoboPy.GameState.Destroy(self)

	def Pause(self):
		del self.mMenuItems
		del self.mHeading

		return RoboPy.GameState.Pause(self)

	def Unpause(self):
		self.Initialize()

		return RoboPy.GameState.Unpause(self)

	def Update(self, delta):
		self.mKernel.DisplaySurface().blit(self.mHeading, self.mHeadingRect)

		for item in self.mMenuItems:
			self.mKernel.DisplaySurface().blit(self.mMenuItems[item], self.mMenuRects[item])

		return RoboPy.GameState.Update(self, delta)