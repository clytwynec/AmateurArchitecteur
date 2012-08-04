import pygame

class Maze:
	def __init__(self, kernel):
		# Binary filled grid
		self.mGrid = []

		# Horizonal and Vertical Walls
		self.mHorizontalWalls = []
		self.mVertialWalls = []

		# Internal stuff, size and kernel
		self.mSize = (0, 0)
		self.mKernel = kernel
		self.mTileSize = 10

		# Pygame tomfoolery
		self.mSurface = None
		return

	###################################################################################
	# Generate
	#
	# Generates a starting maze, then splits it into different wall objects
	#
	# Parameters:
	#	size - a 2-tuple of horizontal and vertical dimensions
	###################################################################################
	def Generate(self, size):
		self.mSize = size
		self.mGrid = [[ 0 for col in range(size[1]) ] for row in range(size[0])]
		self.mSurface = pygame.Surface((size[0] * self.mTileSize, size[1] * self.mTileSize))

		return

	###################################################################################
	# WallSplit
	#
	# Splits a grid into a series of horizonal and vertical walls
	#
	###################################################################################
	def WallSplit(self):
		return

	###################################################################################	
	# Draw
	#
	# Puts the maze on the screen
	###################################################################################
	def Draw(self):
		for row in range(self.mSize[0]):
			for col in range(self.mSize[1]):
				rect = pygame.Rect(row * self.mTileSize, col * self.mTileSize, self.mTileSize, self.mTileSize)

				if (self.mGrid[row][col] == 1):
					pygame.draw.rect(self.mSurface, pygame.Color(0, 0, 0), rect)
				else:
					pygame.draw.rect(self.mSurface, pygame.Color(255, 255, 255), rect)

		self.mKernel.DisplaySurface().blit(self.mSurface, pygame.Rect(0, 0, self.mSize[0] * self.mTileSize, self.mSize[1] * self.mTileSize))