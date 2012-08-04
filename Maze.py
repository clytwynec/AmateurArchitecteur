# HI STEVE THIS IS NOT A MAZE YET
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

		for x in range(size[0]):
			for y in range(size[1]):
				print ((x * size[1]) + y) % 2
				self.mGrid[x][y] = (((x * size[1]) + y) + (x % 2)) % 2

		print self.mGrid

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
			linetext = ""

			for col in range(self.mSize[1]):
				if (self.mGrid[row][col] == 1):
					linetext += "X"
				else:
					linetext += " "

			print linetext