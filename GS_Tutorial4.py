import pygame
import RoboPy
import os
import math

from pygame.locals import *

from Maze import *
from Monster import *

class GS_Tutorial4(RoboPy.GameState):
	def __init__(self, kernel, gsm):
		RoboPy.GameState.__init__(self, "Tutorial4", kernel, gsm)

		self.mMaze = None
		self.mMonster = None

		self.mOffset = (250, 150)

		# Other Stuff
		self.mHoverTile = (0, 0)

	def Initialize(self):
		self.mTutorialText = pygame.image.load(os.path.join("Data", "tutorialText4.bmp")).convert()
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

		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				self.mGameStateManager.SwitchState("MainMenu")

			if event.key == K_w:
				self.mMaze.MoveWall(self.mHoverTile, "N")
				self.mMonster.SetPath(self.mMaze.Solve(self.mMonster.CurrentTile()))

			elif event.key == K_s:
				self.mMaze.MoveWall(self.mHoverTile, "S")
				self.mMonster.SetPath(self.mMaze.Solve(self.mMonster.CurrentTile()))

			# if event.key == K_a:
			# 	self.mMaze.MoveWall(self.mHoverTile, "W")
			# 	self.mMonster.SetPath(self.mMaze.Solve(self.mMonster.CurrentTile()))

			# elif event.key == K_d:
			# 	self.mMaze.MoveWall(self.mHoverTile, "E")
			# 	self.mMonster.SetPath(self.mMaze.Solve(self.mMonster.CurrentTile()))

		return RoboPy.GameState.HandleEvent(self, event)

	def Update(self, delta):
		self.mMonster.Update(delta)

		self.mKernel.DisplaySurface().fill(Colors.BLUE)

		self.mKernel.DisplaySurface().blit(self.mTutorialText, self.mTutorialRect)

		pygame.draw.rect(self.mKernel.DisplaySurface(), Colors.BLACK, pygame.Rect(self.mOffset[0] - 10, self.mOffset[1] - 10, 16 * 20, 8 * 20))

		self.mMaze.Draw(self.mHoverTile)
		self.mMonster.Draw()

		if (self.mMonster.IsFinished()):
			self.mGameStateManager.SwitchState("Tutorial5")

		return RoboPy.GameState.Update(self, delta)