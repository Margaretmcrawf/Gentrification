"""This is the agent class for our Gentrification/Creativity model."""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import scipy.special as sps

class Agent:

	def __init__(self, loc, education=False, avg_income = 50000, sub_housing_rate = 0.50):
		""" From NetLogo code: assign creativity (assume creatives have a little more income, but high creatives have much more)"""

		self.creativity = np.random.choice([1,5,10], p=[0.8, 0.1, 0.1]) # 1 is low, 5 is medium, 10 is high
		self.education = education # is the person educated? May be used to adjust income in future
		self.loc = tuple(loc)
		self.sub_housing_rate = sub_housing_rate

		#determine initial income, which is a random value in a gamma dist. 
		self.income = round(np.random.gamma(avg_income/10000)*10000)

		if self.creativity == 5:
			self.income *= 1.1
		elif self.creativity == 10:
			self.income *= 1.5

		self.is_subsidized = False

	def step(self, env, rent):
		# returns whether the agent is satisfied, based on whether it can afford rent,
		#and some other things. Rent is determined by the cell, and is passed in.
		#if the agent isn't satisfied, move.

		neighbs = env.get_residential_neighbors(self.loc)

		if self.is_subsidized: #rent is cheaper for subsidized agents.
			rent *= self.sub_housing_rate

		if rent > (self.income/4): #if rent is too high
			self.loc = tuple(neighbs[np.random.randint(len(neighbs))])
			return self.loc

		if env.creative_space[self.loc] == 0 and self.creativity >= 5: #if the patch isn't creative and the agent is m or h-creative, move
			self.loc = tuple(neighbs[np.random.randint(len(neighbs))])
			return self.loc

		return False

	def update_creativity(self, env): 
		#if there are lots of creative neighbors, increase creativity.
		pass


