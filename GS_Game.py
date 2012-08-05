import pygame
import RoboPy
import os
import math

from pygame.locals import *

from Maze import *
from Monster import *

class GS_Game(RoboPy.GameState):
	def __init__(self, kernel, gsm):
		RoboPy.GameState.__init__(self, "Game", kernel, gsm)

		self.mMazeSize = (27, 39)
		self.mMaze = None
		self.mMonster = None

		# Scoring Stuff
		self.mScore = 0
		self.mLevel = 1
		self.mMoves = 0
		self.mMarkedScore = 0

		# Other Stuff
		self.mHoverTile = (0, 0)

	def Initialize(self):
		# Build maze
		self.mMaze = Maze(self.mKernel)
		self.mMaze.SetOffset((10, 10))
		self.mMaze.Generate(self.mMazeSize)
		#maze.Load(os.path.join("Data", "tutorial1.maze"))
		self.mMaze.BuildWalls()

		# Make Monster --- ahhh
		self.mMonster = Monster(self.mKernel)
		self.mMonster.SetOffset((10, 10))
		self.mMonster.SetPath(self.mMaze.Solve((0, 0)))
		self.mMonster.SetCage(self.mMaze.GetCage())


		return RoboPy.GameState.Initialize(self)

	def Destroy(self):
		return RoboPy.GameState.Destroy(self)

	def Pause(self):

		return RoboPy.GameState.Pause(self)

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
			self.mHoverTile = (int(math.floor((event.pos[1] - 10) / 20)), int(math.floor((event.pos[0] - 10) / 20)))

		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				self.mGameStateManager.SwitchState("MainMenu")
			if event.key == K_w:
				self.mMoves += self.mMaze.MoveWall(self.mHoverTile, "N")
				self.mMonster.SetPath(self.mMaze.Solve(self.mMonster.CurrentTile()))

			elif event.key == K_s:
				self.mMoves += self.mMaze.MoveWall(self.mHoverTile, "S")
				self.mMonster.SetPath(self.mMaze.Solve(self.mMonster.CurrentTile()))

			elif event.key == K_a:
				self.mMoves += self.mMaze.MoveWall(self.mHoverTile, "W")
				self.mMonster.SetPath(self.mMaze.Solve(self.mMonster.CurrentTile()))

			elif event.key == K_d:
				self.mMoves += self.mMaze.MoveWall(self.mHoverTile, "E")
				self.mMonster.SetPath(self.mMaze.Solve(self.mMonster.CurrentTile()))

		return RoboPy.GameState.HandleEvent(self, event)

	def Update(self, delta):
		self.mMonster.Update(delta)

		#check score
		if self.mMonster.IsCaught() and self.mMarkedScore == 0:
			self.mScore = self.mScore + self.CalcScore()
			self.mMarkedScore = 1

		self.mKernel.DisplaySurface().fill(Colors.BLACK)

		self.mMaze.Draw(self.mHoverTile)
		self.mMonster.Draw()

		if (self.mMonster.IsFinished()):
			self.mMaze.Generate(self.mMazeSize)
			self.mLevel += 1 
			self.mMoves = 0
			self.mMaze.BuildWalls()
			self.mMonster.Reset()
			self.mMarkedScore = 0
			self.mMonster.SetPath(self.mMaze.Solve(self.mMonster.CurrentTile()))

		return RoboPy.GameState.Update(self, delta)