import pygame
import Colors
import os

class Monster:
	def __init__(self, kernel):
		self.mPath = []

		self.mSpeed = 2
		self.mDestination = None
		self.mCurrentTile = (0, 0)

		self.mTicks = 0

		self.mNoPath = False
		self.mFinished = False

		self.mKernel = kernel
		self.mMonsterSize = 20

		fullpath = os.path.join("Data", "monster.bmp")
		self.mSurface = pygame.image.load(fullpath).convert()

		#self.mSurface.fill(Colors.TRANSPARENT)
		self.mSurface.set_colorkey(Colors.TRANSPARENT)

		#pygame.draw.circle(self.mSurface, Colors.MONSTER, (self.mMonsterSize / 2, self.mMonsterSize / 2), (self.mMonsterSize / 2) - 1)

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
			self.mNoPath = False
			self.mFinished = False
		else:
			self.mDestination = None
			self.mNoPath = True

	def CurrentTile(self):
		return self.mCurrentTile

	def IsFinished(self):
		return self.mFinished

	def HasNoPath(self):
		return self.mNoPath	

	def Reset(self):
		self.mPath = []
		self.mDestination = None
		self.mCurrentTile = (0, 0)

		self.mTicks = 0

		self.mNoPath = False
		self.mFinished = False

		self.mRect = pygame.Rect(0, 0, self.mMonsterSize, self.mMonsterSize)

	def SetSpeed(self, speed):
		self.mSpeed = speed
			
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
				if self.mCurrentTile == 

				if (len(self.mPath)):
					rawDest = self.mPath.pop(0)
					self.mCurrentTile = rawDest
					self.mDestination = (rawDest[1] * self.mMonsterSize, rawDest[0] * self.mMonsterSize)
				else:
					self.mDestination = None
					self.mFinished = True
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