import pygame

class Monster:
	def __init__(self, kernel):
		self.mPath = []

		self.mSpeed = 1
		self.mDestination = None

		self.mKernel = kernel
		self.mMonsterSize = 20

		self.mSurface = pygame.Surface((self.mMonsterSize, self.mMonsterSize))
		self.mSurface.fill(pygame.Color(255, 0, 255))
		pygame.draw.circle(self.mSurface, pygame.Color(0, 0, 255), (self.mMonsterSize / 2, self.mMonsterSize / 2), (self.mMonsterSize / 2) - 1)
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
		self.mDestination = self.mPath.pop(0)


	###################################################################################
	# Update
	#
	# Moves the monster towards the next destination
	#
	# Parameters:
	#	delta - time delta between the last tick and this one
	###################################################################################
	def Update(self, delta):
		if (self.mDestination):
			x = self.mRect.left
			y = self.mRect.top

			moveVector = (0, 0)

			if (abs(self.mDestination[0] - x) < 0.001 and abs(self.mDestination[1] - y) < 0.001):
				self.mRect.topleft = self.mDestination

				if (len(self.mPath)):
					self.mDestination = self.mPath.pop(0)
				else:
					self.mDestination = None
					return

			if (self.mDestination[0] > x):
				moveVector = (1.0, 0.0)
			elif (self.mDestination[0] < x):
				moveVector = (-1.0, 0)
			elif (self.mDestination[1] > y):
				moveVector = (0, 1.0)
			elif (self.mDestination[1] < y):
				moveVector = (0, -1.0)

			self.mRect.move_ip(moveVector[0] * self.mSpeed, moveVector[1] * self.mSpeed)

	###################################################################################
	# Draw
	#
	# Draws the monster.  Ahh!!
	#
	###################################################################################
	def Draw(self):
		self.mKernel.DisplaySurface().blit(self.mSurface, self.mRect)