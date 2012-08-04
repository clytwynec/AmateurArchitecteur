##############################
# GameStateManager
#
# Manages GameState objects
###############################

class GameStateManager:
	###################################################################################
	# __init__
	#
	# Standard constructor.  Nulls out fields
	###################################################################################
	def __init__(self):
		self.mStates = {}
		self.mActiveStateName = ""
		self.mActiveState = None

	###################################################################################
	# RegisterState
	#
	# Registers a state with the manager.  You must register states before you can
	# switch or update them.  This should happen once per run at the beginning of the run
	# States are not initialized upon registration.
	#
	# Parameters:
	#	state - The GameState object to register.
	###################################################################################
	def RegisterState(self, state):
		assert state.Name() not in self.mStates, "Game State " + state.Name() + " is already registered."

		self.mStates[state.Name()] = state

	###################################################################################
	# DeregisterState
	#
	# Deregisters a state from the manager.
	# States are destroyed before deregistration if they have been previously initialized
	#
	# Parameters:
	#	stateName - The name of the state to deregister
	###################################################################################
	def DeregisterState(self, stateName):
		assert stateName in self.mStates, "Game State " + stateName + " is not already registered."

		if (self.mStates[stateName].IsInitialized()):
			self.mStates[stateName].Destroy()

		if (self.mActiveStateName == stateName):
			self.mActiveState = None
			self.mActiveStateName = ""

		del self.mStates[stateName]

	###################################################################################
	# SwitchState
	#
	# Switches into a state performing the following steps:
	#	1) Pause current active state
	#	2) Switch current state to new state
	#	3) Initialize (or unpause) new state
	#
	# Parameters:
	#	newStateName - the new state to switch to.  By name
	###################################################################################
	def SwitchState(self, newStateName):
		assert newStateName in self.mStates, "Game State " + newStateName + " has not been registered with this manager."

		if (self.mActiveState):
			if (self.mActiveState.Name() == newStateName):
				return

			if (self.mActiveState.IsInitialized()):
				self.mActiveState.Pause()

		self.mActiveState = self.mStates[newStateName]
		self.mActiveStateName = newStateName

		if (self.mActiveState.IsInitialized()):
			self.mActiveState.Unpause()
		else:
			self.mActiveState.Initialize()

	###################################################################################
	# GetActiveState
	#
	# Returns the current active GameState object
	###################################################################################
	def GetActiveState(self):
		return self.mActiveState

	###################################################################################
	# GetState
	#
	# Returns a state by name
	###################################################################################
	def GetState(self, name):
		if (name in self.mStates):
			return self.mStates[name]

	###################################################################################
	# GetActiveStateName
	#
	# Returns the name of the active GameState object
	###################################################################################
	def GetActiveStateName(self):
		return self.mActiveStateName

	###################################################################################
	# Update
	#
	# Updates the current GameState object
	#
	# Parameters:
	#	delta - a timestep delta (in ms) since the last update tick
	###################################################################################
	def Update(self, delta):
		if (self.mActiveState):
			self.mActiveState.Update(delta)