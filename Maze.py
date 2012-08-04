import pygame
import random

class Maze:
	def __init__(self, kernel):
		# Binary filled grid
		self.mGrid = []

		# Horizonal and Vertical Walls
		self.mTilesToWall = {}
		self.mWalls = []
		self.mBoulders = []

		# Internal stuff, size and kernel
		self.mSize = (0, 0)
		self.mKernel = kernel
		self.mTileSize = 20

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
		self.mGrid = [[ 1 for col in range(size[1]) ] for row in range(size[0])]
		self.mSurface = pygame.Surface((size[1] * self.mTileSize, size[0] * self.mTileSize))

		cellStack = []
		totalCells = self.mSize[0]*self.mSize[1]

		currentCell = (0,0)
		self.mGrid[0][0] = 0
		visitedCells = []

		while len(visitedCells) < totalCells:
			visitedCells.append(currentCell)
			neighbors = [(currentCell[0],currentCell[1]+2),
				(currentCell[0],currentCell[1]-2),
				(currentCell[0]+2,currentCell[1]),
				(currentCell[0]-2,currentCell[1])]
			random.shuffle(neighbors)	
			foundNeighbor = 0

			for i in range(0, len(neighbors)):	
				if neighbors[i][0]>=0 and neighbors[i][0]<self.mSize[0]:
					if neighbors[i][1]>=0 and neighbors[i][1]<self.mSize[1]:
						if self.mGrid[neighbors[i][0]][neighbors[i][1]] == 1:
							self.mGrid[neighbors[i][0]][neighbors[i][1]] = 0

							if neighbors[i][0]<currentCell[0]:
								self.mGrid[neighbors[i][0]+1][neighbors[i][1]] = 0
							if neighbors[i][0]>currentCell[0]:
								self.mGrid[neighbors[i][0]-1][neighbors[i][1]] = 0
							if neighbors[i][1]<currentCell[1]:
								self.mGrid[neighbors[i][0]][neighbors[i][1]+1] = 0	
							if neighbors[i][1]>currentCell[1]:
								self.mGrid[neighbors[i][0]][neighbors[i][1]-1] = 0	

							cellStack.append(neighbors[i])
							foundNeighbor = 1
							currentCell = neighbors[i]

							break
											
			if foundNeighbor == 0:
				if len(cellStack)==0:
					break
				currentCell = cellStack.pop()							
		return

	###################################################################################
	# Solve
	#
	# Sovles a maze, given a starting point
	#
	# Parameters:
	#	start - a 2-tuple of the tile to start with
	###################################################################################
	def Solve(self, start):
		cellStack = []
		totalCells = self.mSize[0] * self.mSize[1]

		end = (self.mSize[0] - 1, self.mSize[1] - 1)
		currentCell = start
		visitedCells = []

		while len(visitedCells) < totalCells:
			visitedCells.append(currentCell)

			if (currentCell == end):
				return cellStack

			neighbors = [
				(currentCell[0], currentCell[1] + 1),
				(currentCell[0], currentCell[1] - 1),
				(currentCell[0] + 1, currentCell[1]),
				(currentCell[0] - 1, currentCell[1])
			]

			foundNeighbor = 0

			for i in range(0, len(neighbors)):	
				if neighbors[i][0] >= 0 and neighbors[i][0] < self.mSize[0]:
					if neighbors[i][1] >= 0 and neighbors[i][1] < self.mSize[1]:
						if neighbors[i] not in visitedCells and self.mGrid[neighbors[i][0]][neighbors[i][1]] == 0:
							cellStack.append(currentCell)
							cellStack.append(neighbors[i])
							foundNeighbor = 1
							currentCell = neighbors[i]

							break
											
			if foundNeighbor == 0:
				if len(cellStack)==0:
					break

				currentCell = cellStack.pop()

		return []

	###################################################################################
	# SplitWalls
	#
	# Splits a grid into a series of horizonal and vertical walls
	#
	###################################################################################
	def SplitWalls(self):
		return

	###################################################################################
	# MarkBoulders
	#
	# Marks the boulder in a maze.  A boulder is defined as a wall piece which is
	# connected to 3 or more other wall pieces
	#
	###################################################################################
	def MarkBoulders(self):
		return

	###################################################################################
	# ToggleGridPoint
	#
	# Helper Function - Toggles a grid point from marked to unmarked and back
	#
	# Parameters:
	#	point - the point to toggle
	###################################################################################
	def ToggleGridPoint(self, point):
		self.mGrid[point[0]][point[1]] = ((self.mGrid[point[0]][point[1]] + 1) % 2)

	###################################################################################	
	# Draw
	#
	# Puts the maze on the screen
	###################################################################################
	def Draw(self):
		for row in range(self.mSize[0]):
			for col in range(self.mSize[1]):
				rect = pygame.Rect(col * self.mTileSize, row * self.mTileSize, self.mTileSize, self.mTileSize)

				if (row == 0 and col == 0):
					pygame.draw.rect(self.mSurface, pygame.Color(0, 255, 0), rect)
				elif (row == self.mSize[0] - 1 and col == self.mSize[1] - 1):
					pygame.draw.rect(self.mSurface, pygame.Color(255, 0, 0), rect)
				elif (self.mGrid[row][col] == 1):
					pygame.draw.rect(self.mSurface, pygame.Color(90, 90, 90), rect)
				else:
					pygame.draw.rect(self.mSurface, pygame.Color(255, 255, 255), rect)

		self.mKernel.DisplaySurface().blit(self.mSurface, pygame.Rect(0, 0, self.mSize[0] * self.mTileSize, self.mSize[1] * self.mTileSize))