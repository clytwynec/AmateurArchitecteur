###################################################################################
# GameState
#
# A GameState represents a single screen of the game, be it
# a menu, the game screen itself, or other UI element.
#
# This is an abstract class that requires the following definitions
# in order to be useful:
#
# 	Initialize(self) -- set up the initial state
# 	Destroy(self) -- destroy any elements the state has
# 	Pause(self) -- freeze the state if necessary
# 	Unpause(self) -- unfreeze the state as required
# 	Update(self, delta) -- tick method that dispatches to subelements 
###################################################################################
class GameState:
	def __init__(self, name, kernel, gsm):
		self.mName = name
		self.mInitialized = False
		self.mActive = False
		self.mKernel = kernel
		self.mGameStateManager = gsm

	def Name(self):
		return self.mName

	def IsInitialized(self):
		return self.mInitialized

	def IsActive(self):
		return self.mActive

	def Initialize(self):
		self.mInitialized = True
		self.mActive = True
		
		return True

	def Destroy(self):
		self.mActive = False
		self.mInitialized = False

		return True

	def Pause(self):
		self.mActive = False

		return True

	def Unpause(self):
		self.mActive = True

		return True

	def HandleEvent(self, event):
		return True

	def Update(self, delta):
		return True