"""This is the agent class for our Gentrification/Creativity model."""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import scipy.special as sps

class Agent:

	def __init__(self, education=False):
		self.creativity = np.random.choice([1,5,10]) # 1 is low, 5 is medium, 10 is high
		self.education = education # is the person educated

		#determine initial income, which is a random value in a gamma dist. 
		shape = 5 #centered at 50,000 subject to change
		self.income = round(np.random.gamma(shape)*10000)

	def is_satisfied(self, rent):
		# returns whether the agent is satisfied, based on whether it can afford rent,
		#and some other things. Rent is determined by the cell, and is passed in.
		if rent > self.income/4:
			return False
		else:
			return True

a = Agent(education=True)
print(a.income)

# shape, scale = 5, 1
# s = np.random.gamma(shape, scale, 1000)*10000

# count, bins, ignored = plt.hist(s, 50, normed=True)
# y = bins**(shape-1)*(np.exp(-bins/scale) / (sps.gamma(shape)*scale**shape))
# plt.plot(bins, y, linewidth=2, color='r')
# plt.show()
