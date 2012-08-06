import pygame
import RoboPy
import os
import math

from pygame.locals import *

from Maze import *
from Monster import *

class GS_Tutorial2(RoboPy.GameState):
	def __init__(self, kernel, gsm):
		RoboPy.GameState.__init__(self, "Tutorial2", kernel, gsm)

		self.mMaze = None
		self.mMonster = None

		self.mOffset = (250, 150)

		# Other Stuff
		self.mHoverTile = (0, 0)

	def Initialize(self):
		self.mTutorialText = pygame.image.load(os.path.join("Data", "tutorialText2.bmp")).convert()
		self.mTutorialRect = self.mTutorialText.get_rect()

		# Build maze
		self.mMaze = Maze(self.mKernel)
		self.mMaze.SetOffset(self.mOffset)
		self.mMaze.Load(os.path.join("Data", "tutorial2.maze"))
		self.mMaze.BuildWalls()

		# Make Monster --- ahhh
		self.mMonster = Monster(self.mKernel)
		self.mMonster.SetOffset(self.mOffset)
		self.mMonster.SetPath(self.mMaze.Solve((0, 0)))
		self.mMonster.SetCage(self.mMaze.GetCage())

		self.mBackImage = pygame.image.load(os.path.join("Data", "back.bmp")).convert()
		self.mBackHover = pygame.image.load(os.path.join("Data", "back_hover.bmp")).convert()
		self.mBackButton = self.mBackImage
		self.mBackRect = self.mBackButton.get_rect()
		self.mBackRect.topleft = (20, 530)

		self.mNextImage = pygame.image.load(os.path.join("Data", "next.bmp")).convert()
		self.mNextHover = pygame.image.load(os.path.join("Data", "next_hover.bmp")).convert()
		self.mNextButton = self.mNextImage
		self.mNextRect = self.mNextButton.get_rect()
		self.mNextRect.topleft = (630, 530)

		return RoboPy.GameState.Initialize(self)

	def Destroy(self):
		return RoboPy.GameState.Destroy(self)

	def Pause(self):
		RoboPy.GameState.Pause(self)

		return RoboPy.GameState.Destroy(self) 

	def Unpause(self):
		return RoboPy.GameState.Unpause(self)

	def CalcScore(self):
		difficulty = self.mLevel * 10
		moves = self.mMoves

		if moves == 0: 
			moves = 1

		score = int(math.floor(difficulty * (100 * (1.0 / moves))))

		return score

	def HandleEvent(self, event):
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		elif event.type == MOUSEMOTION:
		 	self.mHoverTile = (int(math.floor((event.pos[1] - self.mOffset[1]) / 20)), int(math.floor((event.pos[0] - self.mOffset[0]) / 20)))

			if (self.mBackRect.collidepoint(event.pos)):
				self.mBackButton = self.mBackHover
			else:
				self.mBackButton = self.mBackImage

			if (self.mNextRect.collidepoint(event.pos)):
				self.mNextButton = self.mNextHover
			else:
				self.mNextButton = self.mNextImage
		elif event.type == MOUSEBUTTONDOWN:
			if (self.mBackRect.collidepoint(event.pos)):
				self.mGameStateManager.SwitchState("Tutorial1")
			elif (self.mNextRect.collidepoint(event.pos)):
				self.mGameStateManager.SwitchState("Tutorial3")


		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				self.mGameStateManager.SwitchState("MainMenu")

		return RoboPy.GameState.HandleEvent(self, event)

	def Update(self, delta):
		self.mMonster.Update(delta)

		self.mKernel.DisplaySurface().fill(Colors.BLUE)

		self.mKernel.DisplaySurface().blit(self.mTutorialText, self.mTutorialRect)

		pygame.draw.rect(self.mKernel.DisplaySurface(), Colors.BLACK, pygame.Rect(self.mOffset[0] - 10, self.mOffset[1] - 10, 16 * 20, 8 * 20))

		self.mMaze.Draw(self.mHoverTile)
		self.mMonster.Draw()

		self.mKernel.DisplaySurface().blit(self.mNextButton, self.mNextRect)
		self.mKernel.DisplaySurface().blit(self.mBackButton, self.mBackRect)

		return RoboPy.GameState.Update(self, delta)