import pygame

class Monster:
	def __init__(self, kernel):
		self.mPath = []

		self.mSpeed = 20
		self.mDestination = None
		self.mCurrentTile = (0, 0)

		self.mTicks = 0

		self.mKernel = kernel
		self.mMonsterSize = 20

		self.mSurface = pygame.Surface((self.mMonsterSize, self.mMonsterSize))
		self.mSurface.fill((255, 0, 255))
		self.mSurface.set_colorkey((255, 0, 255))

		pygame.draw.circle(self.mSurface, pygame.Color(0, 0, 255, 100), (self.mMonsterSize / 2, self.mMonsterSize / 2), (self.mMonsterSize / 2) - 1)

		self.mRect = pygame.Rect(0, 0, self.mMonsterSize, self.mMonsterSize)

		return

	###################################################################################
	# SetPath
	#
	# Sets the given path for the monster to travel on
	# 
	# Parameters:
	# 	path - a list of coordinate tuples to queue up as moves
	###################################################################################
	def SetPath(self, path):
		self.mPath = path

		if (len(path)):
			rawDest = self.mPath.pop(0)
			self.mDestination = (rawDest[1] * self.mMonsterSize, rawDest[0] * self.mMonsterSize)
		else:
			self.mDestination = None

	def CurrentTile(self):
		return self.mCurrentTile


	###################################################################################
	# Update
	#
	# Moves the monster towards the next destination
	#
	# Parameters:
	#	delta - time delta between the last tick and this one
	###################################################################################
	def Update(self, delta):
		self.mTicks += delta

		if (self.mDestination and self.mTicks > 0):
			self.mTicks = 0
			x = self.mRect.left
			y = self.mRect.top

			moveVector = (0, 0)

			if (self.mDestination[0] == x and self.mDestination[1] == y):
				self.mRect.left = self.mDestination[0]
				self.mRect.top = self.mDestination[1]

				if (len(self.mPath)):
					rawDest = self.mPath.pop(0)
					self.mCurrentTile = rawDest
					self.mDestination = (rawDest[1] * self.mMonsterSize, rawDest[0] * self.mMonsterSize)
				else:
					self.mDestination = None
					return

			if (self.mDestination[0] > x):
				moveVector = (1, 0)
			elif (self.mDestination[0] < x):
				moveVector = (-1, 0)
			elif (self.mDestination[1] > y):
				moveVector = (0, 1)
			elif (self.mDestination[1] < y):
				moveVector = (0, -1)

			self.mRect.move_ip(moveVector[0] * self.mSpeed, moveVector[1] * self.mSpeed)

	###################################################################################
	# Draw
	#
	# Draws the monster.  Ahh!!
	#
	###################################################################################
	def Draw(self):
		self.mKernel.DisplaySurface().blit(self.mSurface, self.mRect)