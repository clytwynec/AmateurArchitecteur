import pygame
import RoboPy

class GS_OptionsMenu(RoboPy.GameState):
	def __init__(self, kernel, gsm):
		RoboPy.GameState.__init__(self, "OptionsMenu", kernel, gsm)

		self.mHeaderFont = pygame.font.SysFont("Helvetica", 24, (255, 255, 255), True)
		self.mMenuFont = pygame.font.SysFont("Helvetica", 16, (255, 255, 255))
		self.mHeading = None
		self.mMenuItems = {}
		self.mMenuRects = {}

	def Initialize(self):
		self.mHeading = self.mHeaderFont.render("RoboPy Game Engine - Options Menu", True, (255, 255, 255))
		self.mHeadingRect = self.mHeading.get_rect()
		self.mHeadingRect.topleft = (100, 100)

		self.mMenuItems["MainMenu"] = self.mMenuFont.render("Main Menu", True, (255, 255, 255))
		self.mMenuRects["MainMenu"] = self.mMenuItems["MainMenu"].get_rect()
		self.mMenuRects["MainMenu"].topleft = (150, 200)


		return RoboPy.GameState.Initialize(self)

	def Destroy(self):
		return RoboPy.GameState.Destroy(self)

	def Pause(self):
		self.mMenuItems = {}
		self.mMenuRects = {}
		self.mHeading = None

		return RoboPy.GameState.Pause(self)

	def Unpause(self):
		self.Initialize()

		return RoboPy.GameState.Unpause(self)

	def Update(self, delta):
		self.mKernel.DisplaySurface().blit(self.mHeading, self.mHeadingRect)

		for item in self.mMenuItems:
			self.mKernel.DisplaySurface().blit(self.mMenuItems[item], self.mMenuRects[item])

		return RoboPy.GameState.Update(self, delta)