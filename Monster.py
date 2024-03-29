import pygame
import Colors
import os

class Monster:
	def __init__(self, kernel):
		self.mPath = []

		self.mSpeed = 1
		self.mDestination = None
		self.mCurrentTile = (0, 0)
		self.mCage = (0, 0)

		# This represents the top left corner of the maze
		self.mOffset = (0, 0)

		self.mTicks = 0

		self.mNoPath = False
		self.mFinished = False
		self.mCaught = False

		self.mKernel = kernel
		self.mMonsterSize = 20

		fullpath = os.path.join("Data", "monster.bmp")
		self.mSurface = pygame.image.load(fullpath).convert()
		self.mSurface.set_colorkey(Colors.TRANSPARENT)

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
			self.mDestination = (rawDest[1] * self.mMonsterSize + self.mOffset[0], rawDest[0] * self.mMonsterSize + self.mOffset[1])
			self.mNoPath = False
			self.mFinished = False
		else:
			#self.mDestination = None
			self.mNoPath = True

	def CurrentTile(self):
		return self.mCurrentTile

	def IsFinished(self):
		return self.mFinished

	def IsCaught(self):
		return self.mCaught

	def HasNoPath(self):
		return self.mNoPath	

	def Reset(self):
		self.mPath = []
		self.mDestination = None
		self.mCurrentTile = (0, 0)

		self.mTicks = 0

		self.mNoPath = False
		self.mFinished = False
		self.mCaught = False 
		
		self.mRect = pygame.Rect(0, 0, self.mMonsterSize, self.mMonsterSize)
		self.mRect.topleft = (self.mRect.top + self.mOffset[0], self.mRect.left + self.mOffset[1])

	def SetSpeed(self, speed):
		self.mSpeed = speed

	def SetCage(self, cage):
		self.mCage = cage

	def SetOffset(self, offset):
		self.mOffset = offset
		self.mRect.topleft = (self.mRect.top + self.mOffset[0], self.mRect.left + self.mOffset[1])

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
			speed = self.mSpeed

			if (self.mDestination[0] > x):
				moveVector = (1, 0)
				speed = min(self.mSpeed, abs(self.mDestination[0] - x))
			elif (self.mDestination[0] < x):
				moveVector = (-1, 0)
				speed = min(self.mSpeed, abs(self.mDestination[0] - x))
			elif (self.mDestination[1] > y):
				moveVector = (0, 1)
				speed = min(self.mSpeed, abs(self.mDestination[1] - y))
			elif (self.mDestination[1] < y):
				moveVector = (0, -1)
				speed = min(self.mSpeed, abs(self.mDestination[1] - y))

			moveVector = (moveVector[0] * speed, moveVector[1] * speed)

			self.mRect.move_ip(moveVector[0], moveVector[1])

			if (abs(self.mDestination[0] - x) <= self.mSpeed and abs(self.mDestination[1] - y) <= self.mSpeed):
				self.mRect.left = self.mDestination[0]
				self.mRect.top = self.mDestination[1]

				if self.mCurrentTile == self.mCage:
					self.mCaught = True
				
				if (len(self.mPath)):
					rawDest = self.mPath.pop(0)
					self.mCurrentTile = rawDest
					self.mDestination = (rawDest[1] * self.mMonsterSize + self.mOffset[0], rawDest[0] * self.mMonsterSize + self.mOffset[1])
				else:
					self.mDestination = None
					self.mFinished = not self.mNoPath
					return

	###################################################################################
	# Draw
	#
	# Draws the monster.  Ahh!!
	#
	###################################################################################
	def Draw(self):
		self.mKernel.DisplaySurface().blit(self.mSurface, self.mRect)