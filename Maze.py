import pygame
import random
from collections import defaultdict

class Maze:
	def __init__(self, kernel):
		# Binary filled grid
		self.mGrid = []

		# Horizonal and Vertical Walls
		self.mTilesToHWall = defaultdict(list)
		self.mTilesToVWall = defaultdict(list)
		self.mHWalls = []
		self.mVWalls = []
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
	# BuildWalls
	#
	# Splits a grid into a series of horizonal and vertical walls
	#
	# There are a few main steps for this, but boils down to building both horizontal
	# and vertical walls, and then building the tile to wall array
	#
	###################################################################################
	def BuildWalls(self):
		self.MarkBoulders()

		for row in self.mGrid:
			currentWall = []

			for cell in self.mGrid:
				if (cell == 1 and cell not in self.mBoulders):
					currentWall.append(cell)
				else:
					for cell in currentWall:
						self.mTilesToHWall[cell].append(currentWall)

					self.mHWalls.append(currentWall)
					currentWall = []

		for col in range(self.mSize[1]):
			currentWall = []

			for row in range(self.mSize[0]):
				cell = self.mGrid[row][col]

				if (cell == 1 and cell not in self.mBoulders):
					currentWall.append(cell)
				else:
					for cell in currentWall:
						self.mTilesToVWall[cell].append(currentWall)

					self.mVWalls.append(currentWall)
					currentWall = []

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
	# MoveWall
	#
	# Given a tile and a direction, moves a wall to the farthest point it can go
	# in that direction
	#
	# Parameters:
	#	tile - coordinates of the tile we're trying to move
	#	direction - one of the compass points to move towards.  
	#		Can be 'N', 'S', 'E', or 'W'
	###################################################################################	
	def MoveWall(self, tile, direction):
		wall = []
		edge = (0, 0)
		rowModifier = 0
		colModifier = 0

		if (direction == 'N'):
			wall = self.mTilesToVWall[tile]
			colModifier = -1
			edge = wall[0]
		elif (direction == 'S'):
			wall = self.mTilesToVWall[tile]
			colModifier = 1
			edge = wall[-1]
		elif (direction == 'W'):
			wall = self.mTilesToHWall[tile]
			rowModifier = -1
			edge = wall[-1]
		elif (direction == 'E'):
			wall = self.mTilesToHWall[tile]
			rowModifier = 1
			edge = wall[0]

		if (len(wall) > 0):
			currentCell = (edge[0] + rowModifier, edge[1] + colModifier)
			count = 0

			while (self.mGrid[currentCell[0]][self.currentCell[1]] == 0):
				count += 1
				currentCell[0] = currentCell[0] + rowModifier
				currentCell[1] = currentCell[1] + colModifier

			if (count > 0):
				# reset to edge
				currentCell = (currentCell[0] - rowModifier, currentCell[1] - colModifier)

				reset = 0
				for i in range(count + len(wall)):
					if (reset > len(wall)):
						self.mGrid[currentCell[0]][currentCell[1]] = 0
					else:
						self.mGrid[currentCell[0]][currentCell[1]] = 1

					currentCell = (currentCell[0] + rowModifier, currentCell[1] + colModifier)


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