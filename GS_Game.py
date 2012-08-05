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

		self.mMazeSize = (11, 11)#(27, 39)
		self.mMaze = None
		self.mMonster = None

		# Scoring Stuff
		self.mScore = 0
		self.mLevel = 1
		self.mMoves = 0
		self.mMarkedScore = 0

		# Other Stuff
		self.mHoverTile = (0, 0)

		#images
		self.mScoreImage = None
		self.mMovesImage = None
		self.mLevelImage = None
		self.mScoreRect = None
		self.mMovesRect = None
		self.mLevelRect = None

		self.mFont = None

		self.mCountDown = 0

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

		self.mScoreImage = pygame.image.load(os.path.join("Data", "scoreText.bmp")).convert()
		self.mScoreImage.set_colorkey((0, 144, 247))
		self.mScoreRect = self.mScoreImage.get_rect()
		self.mScoreRect.topleft = (150, 570)

		self.mLosses = 0

		self.mMovesImage = pygame.image.load(os.path.join("Data", "movesText.bmp")).convert()
		self.mMovesImage.set_colorkey((0, 144, 247))
		self.mMovesRect = self.mMovesImage.get_rect()
		self.mMovesRect.topleft = (350, 570)

		self.mLevelImage = pygame.image.load(os.path.join("Data", "levelText.bmp")).convert()
		self.mLevelImage.set_colorkey((0, 144, 247))
		self.mLevelRect = self.mLevelImage.get_rect()
		self.mLevelRect.topleft = (550, 570)

		self.mLevelCompleteImage = pygame.image.load(os.path.join("Data", "levelComplete.bmp")).convert()
		self.mLevelCompleteRect = self.mLevelCompleteImage.get_rect()
		self.mLevelCompleteRect.topleft = (220, 150)

		self.mGameOverImage = pygame.image.load(os.path.join("Data", "gameOver.bmp")).convert()
		self.mGameOverRect = self.mLevelCompleteImage.get_rect()
		self.mGameOverRect.topleft = (220, 150)

		self.mFont = pygame.font.SysFont('Arial', 18, True)

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

			elif event.key == K_SPACE and self.mMarkedScore == 1:
				self.mMarkedScore = 0
				self.mMoves = 0
				self.mLevel += 1
				self.mLosses = 0 
				self.mMaze.Generate(self.mMazeSize)
				self.mMaze.BuildWalls()
				self.mMonster.Reset()
				self.mMonster.SetCage(self.mMaze.GetCage())
				self.mMonster.SetSpeed(self.mLevel)
				self.mMonster.SetPath(self.mMaze.Solve(self.mMonster.CurrentTile()))

		return RoboPy.GameState.HandleEvent(self, event)

	def Update(self, delta):
		self.mMonster.Update(delta)

		#check score
		if self.mMonster.IsCaught() and self.mMarkedScore == 0:
			self.mScore = self.mScore + self.CalcScore()
			self.mMonster.SetPath([])
			self.mMarkedScore = 1

		self.mKernel.DisplaySurface().fill(Colors.BLACK)

		scoreSurf = self.mFont.render(str(self.mScore), True, (0, 0, 0))
		scoreRect = scoreSurf.get_rect()
		scoreRect.topleft = self.mScoreRect.topleft
		scoreRect.left = scoreRect.left + self.mScoreRect.width + 10

		if (self.mMonster.IsFinished()):
			self.mMarkedScore = 0
			self.mMoves = 0
			self.mScore = max(self.mScore - 100, 0)
			self.mLosses += 1

			if (self.mLosses <=2):
				self.mMaze.Generate(self.mMazeSize)
				self.mMaze.BuildWalls()
				self.mMonster.Reset()
				self.mMonster.SetCage(self.mMaze.GetCage())
				self.mMonster.SetPath(self.mMaze.Solve(self.mMonster.CurrentTile()))

		if (self.mMarkedScore):
			self.mMaze.Draw((0, 0))
			pygame.draw.rect(self.mKernel.DisplaySurface(), (0, 0, 0), pygame.Rect(210, 140, 360, 260))
			self.mKernel.DisplaySurface().blit(self.mLevelCompleteImage, self.mLevelCompleteRect)
			self.mKernel.DisplaySurface().blit(scoreSurf, pygame.Rect(380 - int(math.floor(scoreRect.width / 2)), 300, scoreRect.width, scoreRect.height))
		elif (self.mLosses >= 3):
			self.mMaze.Draw((0, 0))
			self.mMonster.Draw()
			pygame.draw.rect(self.mKernel.DisplaySurface(), (0, 0, 0), pygame.Rect(210, 140, 380, 280))
			self.mKernel.DisplaySurface().blit(self.mGameOverImage, self.mGameOverRect)
			self.mKernel.DisplaySurface().blit(scoreSurf, pygame.Rect(380 - int(math.floor(scoreRect.width / 2)), 300, scoreRect.width, scoreRect.height))
		else:
			self.mMaze.Draw(self.mHoverTile)
			self.mMonster.Draw()


		pygame.draw.rect(self.mKernel.DisplaySurface(), Colors.BLUE, pygame.Rect(0, 560, 800, 40))
		self.mKernel.DisplaySurface().blit(self.mScoreImage, self.mScoreRect)
		self.mKernel.DisplaySurface().blit(self.mMovesImage, self.mMovesRect)
		self.mKernel.DisplaySurface().blit(self.mLevelImage, self.mLevelRect)

		self.mKernel.DisplaySurface().blit(scoreSurf, scoreRect)

		moveSurf = self.mFont.render(str(self.mMoves), True, (0, 0, 0))
		moveRect = moveSurf.get_rect()
		moveRect.topleft = self.mMovesRect.topleft
		moveRect.left = moveRect.left + self.mMovesRect.width + 10
		self.mKernel.DisplaySurface().blit(moveSurf, moveRect)

		levelSurf = self.mFont.render(str(self.mLevel), True, (0, 0, 0))
		levelRect = levelSurf.get_rect()
		levelRect.topleft = self.mLevelRect.topleft
		levelRect.left = levelRect.left + self.mLevelRect.width + 10
		self.mKernel.DisplaySurface().blit(levelSurf, levelRect)

		return RoboPy.GameState.Update(self, delta)