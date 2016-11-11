"""This is the agent class for our Gentrification/Creativity model."""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import scipy.special as sps

class Agent:

	def __init__(self, loc, education=False):
		""" From NetLogo code: assign creativity (assume creatives have a little more income, but high creatives have much more)"""

		self.creativity = np.random.choice([1,5,10], p=[0.8, 0.1, 0.1]) # 1 is low, 5 is medium, 10 is high
		self.education = education # is the person educated? May be used to adjust income in future
		self.loc = tuple(loc)

		#determine initial income, which is a random value in a gamma dist. 
		shape = 5 #centered at 50,000 subject to change
		self.income = round(np.random.gamma(shape)*10000)

		if self.creativity == 5:
			self.income *= 1.1
		elif self.creativity == 10:
			self.income *= 1.5

	def step(self, env, rent):
		# returns whether the agent is satisfied, based on whether it can afford rent,
		#and some other things. Rent is determined by the cell, and is passed in.
		#if the agent isn't satisfied, move.
		# neighbors = env.get_neighbors(self.loc) #TODO: make get_neighbors function for the environment

		neighbs = env.get_residential_neighbors(self.loc)

		if rent > self.income/4:
			return False

	def update_creativity(self, env):
		#if there are lots of creative neighbors, increase creativity.
		pass


